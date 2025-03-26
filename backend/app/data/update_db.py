import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, GPU, Motherboard, RAM, PowerSupply
from sqlalchemy.orm import Session

def update_database():
    db = SessionLocal()
    try:
        # Add newer CPUs
        new_cpus = [
            CPU(name="AMD Ryzen 5 7600X", brand="AMD", model="Ryzen 5 7600X", socket="AM5", 
                cores=6, threads=12, base_clock=4.7, boost_clock=5.3, tdp=105, price=299.99),
            CPU(name="AMD Ryzen 7 7700X", brand="AMD", model="Ryzen 7 7700X", socket="AM5", 
                cores=8, threads=16, base_clock=4.5, boost_clock=5.4, tdp=105, price=399.99),
            CPU(name="AMD Ryzen 9 7900X", brand="AMD", model="Ryzen 9 7900X", socket="AM5", 
                cores=12, threads=24, base_clock=4.7, boost_clock=5.6, tdp=170, price=549.99),
            CPU(name="AMD Ryzen 9 7950X", brand="AMD", model="Ryzen 9 7950X", socket="AM5", 
                cores=16, threads=32, base_clock=4.5, boost_clock=5.7, tdp=170, price=699.99),
            CPU(name="Intel Core i5-14600K", brand="Intel", model="i5-14600K", socket="LGA1700", 
                cores=14, threads=20, base_clock=3.5, boost_clock=5.3, tdp=125, price=329.99),
            CPU(name="Intel Core i7-14700K", brand="Intel", model="i7-14700K", socket="LGA1700", 
                cores=20, threads=28, base_clock=3.4, boost_clock=5.6, tdp=125, price=419.99),
            CPU(name="Intel Core i9-14900K", brand="Intel", model="i9-14900K", socket="LGA1700", 
                cores=24, threads=32, base_clock=3.2, boost_clock=6.0, tdp=125, price=589.99),
        ]
        
        # Add newer GPUs
        new_gpus = [
            GPU(name="NVIDIA GeForce RTX 4060", brand="NVIDIA", model="RTX 4060", 
                vram=8, memory_type="GDDR6", tdp=115, length=240, price=299.99),
            GPU(name="NVIDIA GeForce RTX 4070", brand="NVIDIA", model="RTX 4070", 
                vram=12, memory_type="GDDR6X", tdp=200, length=244, price=599.99),
            GPU(name="NVIDIA GeForce RTX 4080 Super", brand="NVIDIA", model="RTX 4080 Super", 
                vram=16, memory_type="GDDR6X", tdp=320, length=280, price=999.99),
            GPU(name="AMD Radeon RX 7600", brand="AMD", model="Radeon RX 7600", 
                vram=8, memory_type="GDDR6", tdp=165, length=230, price=269.99),
            GPU(name="AMD Radeon RX 7700 XT", brand="AMD", model="Radeon RX 7700 XT", 
                vram=12, memory_type="GDDR6", tdp=245, length=267, price=449.99),
            GPU(name="AMD Radeon RX 7800 XT", brand="AMD", model="Radeon RX 7800 XT", 
                vram=16, memory_type="GDDR6", tdp=263, length=269, price=499.99),
            GPU(name="AMD Radeon RX 7900 XTX", brand="AMD", model="Radeon RX 7900 XTX", 
                vram=24, memory_type="GDDR6", tdp=355, length=287, price=949.99),
        ]
        
        # Add newer Motherboards
        new_motherboards = [
            Motherboard(name="ASUS ROG STRIX X670E-E GAMING WIFI", brand="ASUS", model="ROG STRIX X670E-E GAMING WIFI", 
                        socket="AM5", form_factor="ATX", memory_slots=4, max_memory=128, price=449.99),
            Motherboard(name="MSI MPG X670E CARBON WIFI", brand="MSI", model="MPG X670E CARBON WIFI", 
                        socket="AM5", form_factor="ATX", memory_slots=4, max_memory=128, price=399.99),
            Motherboard(name="Gigabyte B650 AORUS ELITE AX", brand="Gigabyte", model="B650 AORUS ELITE AX", 
                        socket="AM5", form_factor="ATX", memory_slots=4, max_memory=128, price=229.99),
            Motherboard(name="MSI MPG Z790 EDGE WIFI", brand="MSI", model="MPG Z790 EDGE WIFI", 
                        socket="LGA1700", form_factor="ATX", memory_slots=4, max_memory=128, price=369.99),
            Motherboard(name="ASUS ROG STRIX Z790-A GAMING WIFI", brand="ASUS", model="ROG STRIX Z790-A GAMING WIFI", 
                        socket="LGA1700", form_factor="ATX", memory_slots=4, max_memory=128, price=399.99),
            Motherboard(name="ASRock B760M PRO RS/D4", brand="ASRock", model="B760M PRO RS/D4", 
                        socket="LGA1700", form_factor="Micro-ATX", memory_slots=4, max_memory=128, price=119.99),
        ]
        
        # Add newer RAM
        new_rams = [
            RAM(name="Corsair Vengeance DDR5 32GB", brand="Corsair", model="Vengeance DDR5", 
                capacity=32, type="DDR5", speed=5600, modules=2, price=134.99),
            RAM(name="G.Skill Trident Z5 RGB 32GB", brand="G.Skill", model="Trident Z5 RGB", 
                capacity=32, type="DDR5", speed=6000, modules=2, price=149.99),
            RAM(name="Kingston FURY Beast DDR5 32GB", brand="Kingston", model="FURY Beast DDR5", 
                capacity=32, type="DDR5", speed=5200, modules=2, price=129.99),
            RAM(name="Crucial 48GB DDR5", brand="Crucial", model="CT2K24G56C46U5", 
                capacity=48, type="DDR5", speed=5600, modules=2, price=179.99),
        ]
        
        # Add all new components to DB
        db.add_all(new_cpus)
        db.add_all(new_gpus)
        db.add_all(new_motherboards)
        db.add_all(new_rams)
        
        # Set up compatibility relationships between the new CPUs and Motherboards
        for cpu in new_cpus:
            for mb in new_motherboards:
                if (cpu.socket == "LGA1700" and mb.socket == "LGA1700") or \
                   (cpu.socket == "AM5" and mb.socket == "AM5"):
                    cpu.compatible_motherboards.append(mb)
        
        db.commit()
        
        # Return counts for verification
        return {
            'cpus': len(new_cpus),
            'gpus': len(new_gpus),
            'motherboards': len(new_motherboards),
            'rams': len(new_rams)
        }
    finally:
        db.close()

if __name__ == "__main__":
    print("Updating database with newer component data...")
    result = update_database()
    print(f"Database updated successfully! Added:")
    print(f"- {result['cpus']} new CPUs")
    print(f"- {result['gpus']} new GPUs")
    print(f"- {result['motherboards']} new motherboards")
    print(f"- {result['rams']} new RAM modules") 