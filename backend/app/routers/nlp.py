from fastapi import APIRouter, HTTPException
from typing import Dict

from app.services.nlp_processor import NLPProcessor

router = APIRouter(
    prefix="/nlp",
    tags=["natural language processing"],
)

# Initialize NLP processor
nlp_processor = NLPProcessor()

@router.post("/process")
def process_text(request: Dict[str, str]):
    """Process natural language input and extract PC building information"""
    if "text" not in request:
        raise HTTPException(status_code=400, detail="Text field is required")
    
    text = request["text"]
    result = nlp_processor.process_query(text)
    
    return result