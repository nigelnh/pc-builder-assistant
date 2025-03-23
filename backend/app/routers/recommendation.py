from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional

from app.models.database import get_db
from app.services.nlp_processor import NLPProcessor
from app.services.recommendation import RecommendationEngine

router = APIRouter(
    prefix="/recommendation",
    tags=["recommendation"],
)

# Initialize services
nlp_processor = NLPProcessor()
recommendation_engine = RecommendationEngine()

@router.post("/from-text")
def recommend_from_text(
    request: Dict[str, str],
    db: Session = Depends(get_db)
):
    """Generate PC build recommendations from natural language input"""
    if "text" not in request:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    # Process the text with NLP
    nlp_result = nlp_processor.process_query(request["text"])
    
    # Generate recommendations based on NLP analysis
    recommendations = recommendation_engine.generate_recommendations(db, nlp_result)
    
    # Include the NLP processing results for reference
    recommendations["nlp_analysis"] = nlp_result
    
    return recommendations

@router.get("/by-criteria")
def recommend_by_criteria(
    use_case: str = "gaming",
    budget: Optional[float] = None,
    tier: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate PC build recommendations based on specific criteria"""
    # Validate use case
    valid_use_cases = ["gaming", "productivity", "content_creation"]
    if use_case not in valid_use_cases:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid use case. Valid values: {', '.join(valid_use_cases)}"
        )
    
    # Validate tier if provided
    if tier:
        valid_tiers = ["budget", "mid_range", "high_end"]
        if tier not in valid_tiers:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid tier. Valid values: {', '.join(valid_tiers)}"
            )
    
    # Prepare NLP-like data structure
    nlp_data = {
        "use_case": {use_case: 1.0},
        "budget": budget
    }
    
    # Override tier if specifically requested
    if tier:
        # The engine will determine tier based on budget, but we'll force it
        original_determine_tier = recommendation_engine.determine_tier
        recommendation_engine.determine_tier = lambda b, uc: tier
        
        # Generate recommendations
        recommendations = recommendation_engine.generate_recommendations(db, nlp_data)
        
        # Restore original method
        recommendation_engine.determine_tier = original_determine_tier
    else:
        # Generate recommendations normally
        recommendations = recommendation_engine.generate_recommendations(db, nlp_data)
    
    return recommendations