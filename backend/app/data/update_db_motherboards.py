import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, Motherboard
from sqlalchemy.orm import Session

def add_am4_motherboards():
    db = SessionLocal()
    try:
        # Define AM4 motherboards for AMD 5000 series CPUs
        am4_motherboards = [
            Motherboard(name="MSI B450 TOMAHAWK MAX II", brand="MSI", model="B450 TOMAHAWK MAX II", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=99.99),
            Motherboard(name="ASUS ROG STRIX B550-F GAMING", brand="ASUS", model="ROG STRIX B550-F GAMING", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=179.99),
            Motherboard(name="Gigabyte X570 AORUS ELITE", brand="Gigabyte", model="X570 AORUS ELITE", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=199.99),
            Motherboard(name="ASRock B550M PRO4", brand="ASRock", model="B550M PRO4", 
                        socket="AM4", form_factor="Micro-ATX", memory_slots=4, max_memory=128, price=109.99),
            Motherboard(name="ASUS TUF GAMING X570-PLUS", brand="ASUS", model="TUF GAMING X570-PLUS", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=189.99),
            Motherboard(name="MSI MPG B550 GAMING PLUS", brand="MSI", model="MPG B550 GAMING PLUS", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=149.99),
        ]
        
        # Add motherboards to the database
        db.add_all(am4_motherboards)
        
        # Set compatibility with existing AM4 CPUs
        am4_cpus = db.query(CPU).filter(CPU.socket == "AM4").all()
        
        for mb in am4_motherboards:
            for cpu in am4_cpus:
                mb.compatible_cpus.append(cpu)
                
        db.commit()
        return len(am4_motherboards)
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding AM4 motherboards to the database...")
    count = add_am4_motherboards()
    print(f"Successfully added {count} AM4 motherboards!") 