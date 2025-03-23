from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel

from app.models.database import get_db
from app.models.components import CPU, GPU, Motherboard, RAM, PowerSupply
from app.services.compatibility import CompatibilityChecker

# Add the Pydantic model here
class BuildCompatibilityRequest(BaseModel):
    cpu_id: Optional[int] = None
    gpu_id: Optional[int] = None
    motherboard_id: Optional[int] = None
    ram_ids: Optional[List[int]] = None
    psu_id: Optional[int] = None

router = APIRouter(
    prefix="/compatibility",
    tags=["compatibility"],
    responses={404: {"description": "Component not found"}},
)

# Initialize compatibility checker
compatibility_checker = CompatibilityChecker()

@router.get("/cpu-motherboard/")
def check_cpu_motherboard_compatibility(
    cpu_id: int, 
    motherboard_id: int, 
    db: Session = Depends(get_db)
):
    """Check compatibility between a CPU and motherboard"""
    cpu = db.query(CPU).filter(CPU.id == cpu_id).first()
    motherboard = db.query(Motherboard).filter(Motherboard.id == motherboard_id).first()
    
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU not found")
    if not motherboard:
        raise HTTPException(status_code=404, detail="Motherboard not found")
    
    result = compatibility_checker.check_cpu_motherboard_compatibility(cpu, motherboard)
    return result

@router.get("/power-requirements/")
def check_power_requirements(
    cpu_id: int, 
    gpu_id: int, 
    psu_id: int,
    db: Session = Depends(get_db)
):
    """Check if power supply is adequate for the system"""
    cpu = db.query(CPU).filter(CPU.id == cpu_id).first()
    gpu = db.query(GPU).filter(GPU.id == gpu_id).first()
    psu = db.query(PowerSupply).filter(PowerSupply.id == psu_id).first()
    
    if not cpu:
        raise HTTPException(status_code=404, detail="CPU not found")
    if not gpu:
        raise HTTPException(status_code=404, detail="GPU not found")
    if not psu:
        raise HTTPException(status_code=404, detail="Power supply not found")
    
    components = {
        "cpu": cpu,
        "gpu": gpu,
        "power_supply": psu
    }
    
    result = compatibility_checker.check_power_requirements(components)
    return result

@router.get("/compatible-components/")
def get_compatible_components(
    component_type: str,
    component_id: int,
    db: Session = Depends(get_db)
):
    """Get all compatible components for a specific component"""
    valid_types = ["cpu", "motherboard"]
    if component_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid component type. Valid types: {', '.join(valid_types)}")
    
    compatible_components = compatibility_checker.get_compatible_components(db, component_type, component_id)
    return compatible_components

@router.post("/check-build/")
def check_build_compatibility(
    components: BuildCompatibilityRequest,
    db: Session = Depends(get_db)
):
    """Check compatibility of a complete build"""
    # Validate and get components from database
    build_components = {}
    
    if components.cpu_id:
        cpu = db.query(CPU).filter(CPU.id == components.cpu_id).first()
        if not cpu:
            raise HTTPException(status_code=404, detail="CPU not found")
        build_components["cpu"] = cpu
    
    if components.gpu_id:
        gpu = db.query(GPU).filter(GPU.id == components.gpu_id).first()
        if not gpu:
            raise HTTPException(status_code=404, detail="GPU not found")
        build_components["gpu"] = gpu
    
    if components.motherboard_id:
        motherboard = db.query(Motherboard).filter(Motherboard.id == components.motherboard_id).first()
        if not motherboard:
            raise HTTPException(status_code=404, detail="Motherboard not found")
        build_components["motherboard"] = motherboard
    
    if components.ram_ids:
        ram_list = []
        for ram_id in components.ram_ids:
            ram = db.query(RAM).filter(RAM.id == ram_id).first()
            if not ram:
                raise HTTPException(status_code=404, detail=f"RAM with ID {ram_id} not found")
            ram_list.append(ram)
        if ram_list:
            build_components["ram"] = ram_list
    
    if components.psu_id:
        psu = db.query(PowerSupply).filter(PowerSupply.id == components.psu_id).first()
        if not psu:
            raise HTTPException(status_code=404, detail="Power supply not found")
        build_components["power_supply"] = psu
    
    # Check compatibility
    result = compatibility_checker.check_system_compatibility(build_components)
    
    # Add component details to response
    result["components"] = {
        "cpu": {"id": build_components["cpu"].id, "name": build_components["cpu"].name} if "cpu" in build_components else None,
        "gpu": {"id": build_components["gpu"].id, "name": build_components["gpu"].name} if "gpu" in build_components else None,
        "motherboard": {"id": build_components["motherboard"].id, "name": build_components["motherboard"].name} if "motherboard" in build_components else None,
        "ram": [{"id": r.id, "name": r.name} for r in build_components["ram"]] if "ram" in build_components else None,
        "power_supply": {"id": build_components["power_supply"].id, "name": build_components["power_supply"].name} if "power_supply" in build_components else None
    }
    
    return result