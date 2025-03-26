from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.database import get_db
from app.models.builds import SavedBuild
from app.schemas.builds import BuildCreate, BuildResponse

router = APIRouter(
    prefix="/builds",
    tags=["builds"],
)

@router.post("/", response_model=BuildResponse)
def save_build(build: BuildCreate, db: Session = Depends(get_db)):
    """Save a PC build configuration"""
    db_build = SavedBuild(**build.dict())
    db.add(db_build)
    db.commit()
    db.refresh(db_build)
    return db_build

@router.get("/", response_model=List[BuildResponse])
def get_saved_builds(db: Session = Depends(get_db)):
    """Get all saved PC build configurations"""
    return db.query(SavedBuild).order_by(SavedBuild.created_at.desc()).all()

@router.get("/{build_id}", response_model=BuildResponse)
def get_build(build_id: int, db: Session = Depends(get_db)):
    """Get a specific PC build configuration by ID"""
    build = db.query(SavedBuild).filter(SavedBuild.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    return build

@router.put("/{build_id}", response_model=BuildResponse)
def update_build(build_id: int, build_data: BuildCreate, db: Session = Depends(get_db)):
    """Update a PC build configuration"""
    build = db.query(SavedBuild).filter(SavedBuild.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    # Update build fields
    for key, value in build_data.dict().items():
        setattr(build, key, value)
    
    db.commit()
    db.refresh(build)
    return build

@router.delete("/{build_id}", response_model=Dict)
def delete_build(build_id: int, db: Session = Depends(get_db)):
    """Delete a PC build configuration"""
    build = db.query(SavedBuild).filter(SavedBuild.id == build_id).first()
    if not build:
        raise HTTPException(status_code=404, detail="Build not found")
    
    db.delete(build)
    db.commit()
    return {"message": "Build deleted successfully"} 