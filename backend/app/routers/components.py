from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.database import get_db
from app.models.components import CPU, GPU, Motherboard, RAM, PowerSupply

router = APIRouter(
    prefix="/components",
    tags=["components"],
    responses={404: {"description": "Component not found"}},
)

@router.get("/cpus/", response_model=List[dict])
def get_cpus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all CPUs"""
    cpus = db.query(CPU).offset(skip).limit(limit).all()
    return [
        {
            "id": cpu.id,
            "name": cpu.name,
            "brand": cpu.brand,
            "model": cpu.model,
            "socket": cpu.socket,
            "cores": cpu.cores,
            "threads": cpu.threads,
            "base_clock": cpu.base_clock,
            "boost_clock": cpu.boost_clock,
            "tdp": cpu.tdp,
            "price": cpu.price
        } for cpu in cpus
    ]

@router.get("/cpus/{cpu_id}", response_model=dict)
def get_cpu(cpu_id: int, db: Session = Depends(get_db)):
    """Get a specific CPU by ID"""
    cpu = db.query(CPU).filter(CPU.id == cpu_id).first()
    if cpu is None:
        raise HTTPException(status_code=404, detail="CPU not found")
    
    return {
        "id": cpu.id,
        "name": cpu.name,
        "brand": cpu.brand,
        "model": cpu.model,
        "socket": cpu.socket,
        "cores": cpu.cores,
        "threads": cpu.threads,
        "base_clock": cpu.base_clock,
        "boost_clock": cpu.boost_clock,
        "tdp": cpu.tdp,
        "price": cpu.price
    }

@router.get("/gpus/", response_model=List[dict])
def get_gpus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all GPUs"""
    gpus = db.query(GPU).offset(skip).limit(limit).all()
    return [
        {
            "id": gpu.id,
            "name": gpu.name,
            "brand": gpu.brand,
            "model": gpu.model,
            "vram": gpu.vram,
            "memory_type": gpu.memory_type,
            "tdp": gpu.tdp,
            "length": gpu.length,
            "price": gpu.price
        } for gpu in gpus
    ]

@router.get("/gpus/{gpu_id}", response_model=dict)
def get_gpu(gpu_id: int, db: Session = Depends(get_db)):
    """Get a specific GPU by ID"""
    gpu = db.query(GPU).filter(GPU.id == gpu_id).first()
    if gpu is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    
    return {
        "id": gpu.id,
        "name": gpu.name,
        "brand": gpu.brand,
        "model": gpu.model,
        "vram": gpu.vram,
        "memory_type": gpu.memory_type,
        "tdp": gpu.tdp,
        "length": gpu.length,
        "price": gpu.price
    }

@router.get("/motherboards/", response_model=List[dict])
def get_motherboards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all motherboards"""
    motherboards = db.query(Motherboard).offset(skip).limit(limit).all()
    return [
        {
            "id": mb.id,
            "name": mb.name,
            "brand": mb.brand,
            "model": mb.model,
            "socket": mb.socket,
            "form_factor": mb.form_factor,
            "memory_slots": mb.memory_slots,
            "max_memory": mb.max_memory,
            "price": mb.price
        } for mb in motherboards
    ]

@router.get("/motherboards/{mb_id}", response_model=dict)
def get_motherboard(mb_id: int, db: Session = Depends(get_db)):
    """Get a specific motherboard by ID"""
    mb = db.query(Motherboard).filter(Motherboard.id == mb_id).first()
    if mb is None:
        raise HTTPException(status_code=404, detail="Motherboard not found")
    
    return {
        "id": mb.id,
        "name": mb.name,
        "brand": mb.brand,
        "model": mb.model,
        "socket": mb.socket,
        "form_factor": mb.form_factor,
        "memory_slots": mb.memory_slots,
        "max_memory": mb.max_memory,
        "price": mb.price
    }

@router.get("/ram/", response_model=List[dict])
def get_rams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all RAM modules"""
    rams = db.query(RAM).offset(skip).limit(limit).all()
    return [
        {
            "id": ram.id,
            "name": ram.name,
            "brand": ram.brand,
            "model": ram.model,
            "capacity": ram.capacity,
            "type": ram.type,
            "speed": ram.speed,
            "modules": ram.modules,
            "price": ram.price
        } for ram in rams
    ]

@router.get("/ram/{ram_id}", response_model=dict)
def get_ram(ram_id: int, db: Session = Depends(get_db)):
    """Get a specific RAM module by ID"""
    ram = db.query(RAM).filter(RAM.id == ram_id).first()
    if ram is None:
        raise HTTPException(status_code=404, detail="RAM not found")
    
    return {
        "id": ram.id,
        "name": ram.name,
        "brand": ram.brand,
        "model": ram.model,
        "capacity": ram.capacity,
        "type": ram.type,
        "speed": ram.speed,
        "modules": ram.modules,
        "price": ram.price
    }

@router.get("/power-supplies/", response_model=List[dict])
def get_power_supplies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all power supplies"""
    psus = db.query(PowerSupply).offset(skip).limit(limit).all()
    return [
        {
            "id": psu.id,
            "name": psu.name,
            "brand": psu.brand,
            "model": psu.model,
            "wattage": psu.wattage,
            "efficiency": psu.efficiency,
            "modular": psu.modular,
            "price": psu.price
        } for psu in psus
    ]

@router.get("/power-supplies/{psu_id}", response_model=dict)
def get_power_supply(psu_id: int, db: Session = Depends(get_db)):
    """Get a specific power supply by ID"""
    psu = db.query(PowerSupply).filter(PowerSupply.id == psu_id).first()
    if psu is None:
        raise HTTPException(status_code=404, detail="Power supply not found")
    
    return {
        "id": psu.id,
        "name": psu.name,
        "brand": psu.brand,
        "model": psu.model,
        "wattage": psu.wattage,
        "efficiency": psu.efficiency,
        "modular": psu.modular,
        "price": psu.price
    }

@router.get("/compatibility/cpu-motherboard/{cpu_id}", response_model=List[dict])
def get_compatible_motherboards(cpu_id: int, db: Session = Depends(get_db)):
    """Get all motherboards compatible with a specific CPU"""
    cpu = db.query(CPU).filter(CPU.id == cpu_id).first()
    if cpu is None:
        raise HTTPException(status_code=404, detail="CPU not found")
    
    return [
        {
            "id": mb.id,
            "name": mb.name,
            "brand": mb.brand,
            "model": mb.model,
            "socket": mb.socket,
            "form_factor": mb.form_factor,
            "memory_slots": mb.memory_slots,
            "max_memory": mb.max_memory,
            "price": mb.price
        } for mb in cpu.compatible_motherboards
    ]

@router.get("/compatibility/motherboard-cpu/{motherboard_id}", response_model=List[dict])
def get_compatible_cpus(motherboard_id: int, db: Session = Depends(get_db)):
    """Get all CPUs compatible with a specific motherboard"""
    mb = db.query(Motherboard).filter(Motherboard.id == motherboard_id).first()
    if mb is None:
        raise HTTPException(status_code=404, detail="Motherboard not found")
    
    return [
        {
            "id": cpu.id,
            "name": cpu.name,
            "brand": cpu.brand,
            "model": cpu.model,
            "socket": cpu.socket,
            "cores": cpu.cores,
            "threads": cpu.threads,
            "base_clock": cpu.base_clock,
            "boost_clock": cpu.boost_clock,
            "tdp": cpu.tdp,
            "price": cpu.price
        } for cpu in mb.compatible_cpus
    ]