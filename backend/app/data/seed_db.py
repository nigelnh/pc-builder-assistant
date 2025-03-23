import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, GPU, Motherboard, RAM, PowerSupply

# Create all tables
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        # Add CPUs
        cpus = [
            CPU(name="Intel Core i5-12600K", brand="Intel", model="i5-12600K", socket="LGA1700", 
                cores=10, threads=16, base_clock=3.7, boost_clock=4.9, tdp=125, price=279.99),
            CPU(name="AMD Ryzen 5 5600X", brand="AMD", model="Ryzen 5 5600X", socket="AM4", 
                cores=6, threads=12, base_clock=3.7, boost_clock=4.6, tdp=65, price=199.99),
            CPU(name="Intel Core i7-12700K", brand="Intel", model="i7-12700K", socket="LGA1700", 
                cores=12, threads=20, base_clock=3.6, boost_clock=5.0, tdp=125, price=379.99),
            CPU(name="AMD Ryzen 7 5800X", brand="AMD", model="Ryzen 7 5800X", socket="AM4", 
                cores=8, threads=16, base_clock=3.8, boost_clock=4.7, tdp=105, price=299.99),
            CPU(name="Intel Core i9-12900K", brand="Intel", model="i9-12900K", socket="LGA1700", 
                cores=16, threads=24, base_clock=3.2, boost_clock=5.2, tdp=125, price=589.99),
        ]
        db.add_all(cpus)
        
        # Add GPUs
        gpus = [
            GPU(name="NVIDIA GeForce RTX 3060", brand="NVIDIA", model="RTX 3060", 
                vram=12, memory_type="GDDR6", tdp=170, length=242, price=329.99),
            GPU(name="AMD Radeon RX 6600 XT", brand="AMD", model="RX 6600 XT", 
                vram=8, memory_type="GDDR6", tdp=160, length=240, price=379.99),
            GPU(name="NVIDIA GeForce RTX 3070", brand="NVIDIA", model="RTX 3070", 
                vram=8, memory_type="GDDR6", tdp=220, length=242, price=499.99),
            GPU(name="AMD Radeon RX 6700 XT", brand="AMD", model="RX 6700 XT", 
                vram=12, memory_type="GDDR6", tdp=230, length=267, price=479.99),
            GPU(name="NVIDIA GeForce RTX 3080", brand="NVIDIA", model="RTX 3080", 
                vram=10, memory_type="GDDR6X", tdp=320, length=285, price=699.99),
        ]
        db.add_all(gpus)
        
        # Add Motherboards
        motherboards = [
            Motherboard(name="ASUS ROG STRIX Z690-A", brand="ASUS", model="ROG STRIX Z690-A", 
                        socket="LGA1700", form_factor="ATX", memory_slots=4, max_memory=128, price=279.99),
            Motherboard(name="MSI MPG B550 GAMING EDGE", brand="MSI", model="MPG B550 GAMING EDGE", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=179.99),
            Motherboard(name="Gigabyte Z690 AORUS ELITE", brand="Gigabyte", model="Z690 AORUS ELITE", 
                        socket="LGA1700", form_factor="ATX", memory_slots=4, max_memory=128, price=269.99),
            Motherboard(name="ASRock B550 Phantom Gaming", brand="ASRock", model="B550 Phantom Gaming", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=159.99),
            Motherboard(name="ASUS TUF GAMING B550-PLUS", brand="ASUS", model="TUF GAMING B550-PLUS", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=149.99),
        ]
        db.add_all(motherboards)
        
        # Add RAM
        rams = [
            RAM(name="Corsair Vengeance LPX 16GB", brand="Corsair", model="Vengeance LPX", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=69.99),
            RAM(name="G.Skill Ripjaws V 32GB", brand="G.Skill", model="Ripjaws V", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=109.99),
            RAM(name="Crucial Ballistix 16GB", brand="Crucial", model="Ballistix", 
                capacity=16, type="DDR4", speed=3600, modules=2, price=74.99),
            RAM(name="Kingston FURY Beast 32GB", brand="Kingston", model="FURY Beast", 
                capacity=32, type="DDR4", speed=3200, modules=2, price=119.99),
            RAM(name="G.Skill Trident Z RGB 32GB", brand="G.Skill", model="Trident Z RGB", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=139.99),
        ]
        db.add_all(rams)
        
        # Add Power Supplies
        power_supplies = [
            PowerSupply(name="Corsair RM750", brand="Corsair", model="RM750", 
                       wattage=750, efficiency="80+ Gold", modular=True, price=109.99),
            PowerSupply(name="EVGA SuperNOVA 650 G5", brand="EVGA", model="SuperNOVA 650 G5", 
                       wattage=650, efficiency="80+ Gold", modular=True, price=89.99),
            PowerSupply(name="Seasonic FOCUS GX-850", brand="Seasonic", model="FOCUS GX-850", 
                       wattage=850, efficiency="80+ Gold", modular=True, price=139.99),
            PowerSupply(name="Thermaltake Toughpower GF1 750W", brand="Thermaltake", model="Toughpower GF1", 
                       wattage=750, efficiency="80+ Gold", modular=True, price=119.99),
            PowerSupply(name="be quiet! Straight Power 11 750W", brand="be quiet!", model="Straight Power 11", 
                       wattage=750, efficiency="80+ Gold", modular=True, price=129.99),
        ]
        db.add_all(power_supplies)
        
        # Set up compatibility between CPUs and Motherboards
        # Intel CPUs are compatible with LGA1700 motherboards
        for cpu in cpus:
            for mb in motherboards:
                if (cpu.socket == "LGA1700" and mb.socket == "LGA1700") or \
                   (cpu.socket == "AM4" and mb.socket == "AM4"):
                    cpu.compatible_motherboards.append(mb)
        
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    print("Seeding database with initial component data...")
    seed_data()
    print("Database seeded successfully!")