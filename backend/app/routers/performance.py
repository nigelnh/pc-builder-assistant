from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional

from app.services.performance_calculator import calculate_overall_performance

router = APIRouter(
    prefix="/performance",
    tags=["performance"],
)

@router.post("/")
def calculate_performance(components: Dict[str, Any], 
                         use_case: Optional[str] = "gaming",
                         mentioned_games: Optional[List[str]] = None):
    """
    Calculate performance scores for a PC build
    
    Args:
        components: Dictionary of PC components
        use_case: Primary use case ("gaming", "productivity", "content_creation")
        mentioned_games: List of specific games mentioned by the user
    
    Returns:
        Dictionary with performance scores for different categories
    """
    try:
        # Normalize use case value
        if use_case is None:
            use_case = "gaming"
        elif use_case.lower() in ["gaming", "game", "games"]:
            use_case = "gaming"
        elif use_case.lower() in ["productivity", "work", "office"]:
            use_case = "productivity"
        elif use_case.lower() in ["content creation", "content_creation", "video editing", "rendering"]:
            use_case = "content_creation"
        else:
            use_case = "gaming"  # Default fallback
            
        # Calculate performance scores
        performance_scores = calculate_overall_performance(
            components=components,
            use_case=use_case,
            mentioned_games=mentioned_games
        )
        
        return performance_scores
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating performance: {str(e)}"
        ) 