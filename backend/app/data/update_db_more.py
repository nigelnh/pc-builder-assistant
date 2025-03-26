import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, GPU, Motherboard, RAM, PowerSupply
from sqlalchemy.orm import Session

def update_database_with_more_components():
    db = SessionLocal()
    try:
        # Add more CPUs
        new_cpus = [
            # Intel 12th Gen
            CPU(name="Intel Core i5-12400", brand="Intel", model="i5-12400", socket="LGA1700", 
                cores=6, threads=12, base_clock=2.5, boost_clock=4.4, tdp=65, price=179.99),
            CPU(name="Intel Core i5-12400F", brand="Intel", model="i5-12400F", socket="LGA1700", 
                cores=6, threads=12, base_clock=2.5, boost_clock=4.4, tdp=65, price=159.99),
            CPU(name="Intel Core i3-12100", brand="Intel", model="i3-12100", socket="LGA1700", 
                cores=4, threads=8, base_clock=3.3, boost_clock=4.3, tdp=60, price=129.99),
            CPU(name="Intel Core i3-12100F", brand="Intel", model="i3-12100F", socket="LGA1700", 
                cores=4, threads=8, base_clock=3.3, boost_clock=4.3, tdp=60, price=109.99),
            
            # Intel 13th Gen
            CPU(name="Intel Core i5-13400", brand="Intel", model="i5-13400", socket="LGA1700", 
                cores=10, threads=16, base_clock=2.5, boost_clock=4.6, tdp=65, price=219.99),
            CPU(name="Intel Core i5-13400F", brand="Intel", model="i5-13400F", socket="LGA1700", 
                cores=10, threads=16, base_clock=2.5, boost_clock=4.6, tdp=65, price=199.99),
            
            # AMD Ryzen 5000 Series
            CPU(name="AMD Ryzen 5 5600", brand="AMD", model="Ryzen 5 5600", socket="AM4", 
                cores=6, threads=12, base_clock=3.5, boost_clock=4.4, tdp=65, price=149.99),
            CPU(name="AMD Ryzen 5 5500", brand="AMD", model="Ryzen 5 5500", socket="AM4", 
                cores=6, threads=12, base_clock=3.6, boost_clock=4.2, tdp=65, price=129.99),
            
            # AMD Ryzen 7000 Series
            CPU(name="AMD Ryzen 5 7600", brand="AMD", model="Ryzen 5 7600", socket="AM5", 
                cores=6, threads=12, base_clock=3.8, boost_clock=5.1, tdp=65, price=229.99),
        ]
        
        # Add more GPUs
        new_gpus = [
            # NVIDIA RTX 3000 Series
            GPU(name="NVIDIA GeForce RTX 3060", brand="NVIDIA", model="RTX 3060", 
                vram=12, memory_type="GDDR6", tdp=170, length=242, price=329.99),
            GPU(name="NVIDIA GeForce RTX 3060 Ti", brand="NVIDIA", model="RTX 3060 Ti", 
                vram=8, memory_type="GDDR6", tdp=200, length=242, price=399.99),
            GPU(name="NVIDIA GeForce RTX 3070", brand="NVIDIA", model="RTX 3070", 
                vram=8, memory_type="GDDR6", tdp=220, length=242, price=499.99),
            
            # AMD RX 6000 Series
            GPU(name="AMD Radeon RX 6600", brand="AMD", model="Radeon RX 6600", 
                vram=8, memory_type="GDDR6", tdp=132, length=223, price=249.99),
            GPU(name="AMD Radeon RX 6650 XT", brand="AMD", model="Radeon RX 6650 XT", 
                vram=8, memory_type="GDDR6", tdp=180, length=240, price=299.99),
        ]
        
        # Add more Motherboards
        new_motherboards = [
            # B660 Boards (LGA1700)
            Motherboard(name="MSI PRO B660M-A DDR4", brand="MSI", model="PRO B660M-A DDR4", 
                        socket="LGA1700", form_factor="Micro-ATX", memory_slots=4, max_memory=128, price=119.99),
            Motherboard(name="ASUS Prime B660-PLUS", brand="ASUS", model="Prime B660-PLUS", 
                        socket="LGA1700", form_factor="ATX", memory_slots=4, max_memory=128, price=139.99),
            
            # B550 Boards (AM4)
            Motherboard(name="MSI B550-A PRO", brand="MSI", model="B550-A PRO", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=129.99),
            Motherboard(name="Gigabyte B550 AORUS ELITE", brand="Gigabyte", model="B550 AORUS ELITE", 
                        socket="AM4", form_factor="ATX", memory_slots=4, max_memory=128, price=159.99),
        ]
        
        # Add more RAM
        new_rams = [
            RAM(name="Corsair Vengeance LPX 16GB", brand="Corsair", model="Vengeance LPX", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=54.99),
            RAM(name="G.Skill Ripjaws V 32GB", brand="G.Skill", model="Ripjaws V", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=89.99),
            RAM(name="Kingston FURY Beast 16GB", brand="Kingston", model="FURY Beast", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=49.99),
            RAM(name="Corsair Vengeance RGB Pro 32GB", brand="Corsair", model="Vengeance RGB Pro", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=109.99),
        ]
        
        # Add more Power Supplies
        new_psus = [
            PowerSupply(name="Corsair RM650", brand="Corsair", model="RM650", 
                        wattage=650, efficiency="80+ Gold", modular=True, price=89.99),
            PowerSupply(name="EVGA 600W", brand="EVGA", model="600 BQ", 
                        wattage=600, efficiency="80+ Bronze", modular=True, price=59.99),
            PowerSupply(name="be quiet! Pure Power 11 600W", brand="be quiet!", model="Pure Power 11", 
                        wattage=600, efficiency="80+ Gold", modular=True, price=79.99),
            PowerSupply(name="Seasonic FOCUS GM-650", brand="Seasonic", model="FOCUS GM-650", 
                        wattage=650, efficiency="80+ Gold", modular=True, price=84.99),
        ]
        
        # Add all new components to DB
        db.add_all(new_cpus)
        db.add_all(new_gpus)
        db.add_all(new_motherboards)
        db.add_all(new_rams)
        db.add_all(new_psus)
        
        # Set up compatibility relationships between the new CPUs and Motherboards
        for cpu in new_cpus:
            for mb in new_motherboards:
                if (cpu.socket == "LGA1700" and mb.socket == "LGA1700") or \
                   (cpu.socket == "AM4" and mb.socket == "AM4") or \
                   (cpu.socket == "AM5" and mb.socket == "AM5"):
                    cpu.compatible_motherboards.append(mb)
        
        db.commit()
        
        # Return counts for verification
        return {
            'cpus': len(new_cpus),
            'gpus': len(new_gpus),
            'motherboards': len(new_motherboards),
            'rams': len(new_rams),
            'psus': len(new_psus)
        }
    finally:
        db.close()

if __name__ == "__main__":
    print("Updating database with additional component data...")
    result = update_database_with_more_components()
    print(f"Database updated successfully! Added:")
    print(f"- {result['cpus']} new CPUs")
    print(f"- {result['gpus']} new GPUs")
    print(f"- {result['motherboards']} new motherboards")
    print(f"- {result['rams']} new RAM modules")
    print(f"- {result['psus']} new power supplies") 