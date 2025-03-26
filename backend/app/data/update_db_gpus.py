import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, GPU
from sqlalchemy.orm import Session

def add_additional_gpus():
    db = SessionLocal()
    try:
        # Define GPUs with various price points
        additional_gpus = [
            # Budget GPUs
            GPU(name="NVIDIA GeForce RTX 3050", brand="NVIDIA", model="RTX 3050", 
                vram=8, memory_type="GDDR6", tdp=130, length=200, price=229.99),
            GPU(name="AMD Radeon RX 6600", brand="AMD", model="Radeon RX 6600", 
                vram=8, memory_type="GDDR6", tdp=132, length=190, price=239.99),
            GPU(name="NVIDIA GeForce GTX 1660 Super", brand="NVIDIA", model="GTX 1660 Super", 
                vram=6, memory_type="GDDR6", tdp=125, length=230, price=199.99),
            GPU(name="AMD Radeon RX 6500 XT", brand="AMD", model="Radeon RX 6500 XT", 
                vram=4, memory_type="GDDR6", tdp=107, length=165, price=169.99),
                
            # Mid-range GPUs
            GPU(name="NVIDIA GeForce RTX 3060 Ti", brand="NVIDIA", model="RTX 3060 Ti", 
                vram=8, memory_type="GDDR6", tdp=200, length=232, price=399.99),
            GPU(name="AMD Radeon RX 6650 XT", brand="AMD", model="Radeon RX 6650 XT", 
                vram=8, memory_type="GDDR6", tdp=180, length=240, price=329.99),
            GPU(name="NVIDIA GeForce RTX 4060 Ti", brand="NVIDIA", model="RTX 4060 Ti", 
                vram=8, memory_type="GDDR6", tdp=160, length=246, price=449.99),
            GPU(name="AMD Radeon RX 6750 XT", brand="AMD", model="Radeon RX 6750 XT", 
                vram=12, memory_type="GDDR6", tdp=250, length=267, price=469.99),
                
            # High-end GPUs
            GPU(name="NVIDIA GeForce RTX 4070 Ti", brand="NVIDIA", model="RTX 4070 Ti", 
                vram=12, memory_type="GDDR6X", tdp=285, length=285, price=799.99),
            GPU(name="AMD Radeon RX 7900 XT", brand="AMD", model="Radeon RX 7900 XT", 
                vram=20, memory_type="GDDR6", tdp=300, length=280, price=849.99),
            GPU(name="NVIDIA GeForce RTX 4090", brand="NVIDIA", model="RTX 4090", 
                vram=24, memory_type="GDDR6X", tdp=450, length=336, price=1599.99),
            GPU(name="AMD Radeon RX 7900 XTX SE", brand="AMD", model="Radeon RX 7900 XTX SE", 
                vram=24, memory_type="GDDR6", tdp=355, length=287, price=999.99),
        ]
        
        # Add all GPUs to the database
        db.add_all(additional_gpus)
        db.commit()
        
        return len(additional_gpus)
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding additional GPUs to the database...")
    count = add_additional_gpus()
    print(f"Successfully added {count} additional GPUs!") 