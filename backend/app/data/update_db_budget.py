import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, GPU, Motherboard, RAM, PowerSupply

def add_budget_components():
    db = SessionLocal()
    try:
        # Add budget-friendly CPUs
        budget_cpus = [
            CPU(name="Intel Core i5-13400F", brand="Intel", model="i5-13400F", socket="LGA1700", 
                cores=10, threads=16, base_clock=2.5, boost_clock=4.6, tdp=65, price=199.99),
            CPU(name="AMD Ryzen 5 5600", brand="AMD", model="Ryzen 5 5600", socket="AM4", 
                cores=6, threads=12, base_clock=3.5, boost_clock=4.4, tdp=65, price=139.99),
            CPU(name="Intel Core i3-13100F", brand="Intel", model="i3-13100F", socket="LGA1700", 
                cores=4, threads=8, base_clock=3.4, boost_clock=4.5, tdp=58, price=109.99),
            CPU(name="AMD Ryzen 5 5500", brand="AMD", model="Ryzen 5 5500", socket="AM4", 
                cores=6, threads=12, base_clock=3.6, boost_clock=4.2, tdp=65, price=129.99),
            CPU(name="Intel Core i5-12400F", brand="Intel", model="i5-12400F", socket="LGA1700", 
                cores=6, threads=12, base_clock=2.5, boost_clock=4.4, tdp=65, price=174.99),
        ]
        db.add_all(budget_cpus)
        
        # Add budget-friendly GPUs
        budget_gpus = [
            GPU(name="NVIDIA GeForce RTX 3060 Ti", brand="NVIDIA", model="RTX 3060 Ti", 
                vram=8, memory_type="GDDR6", tdp=200, length=242, price=399.99),
            GPU(name="AMD Radeon RX 6650 XT", brand="AMD", model="RX 6650 XT", 
                vram=8, memory_type="GDDR6", tdp=180, length=240, price=349.99),
            GPU(name="NVIDIA GeForce RTX 4060", brand="NVIDIA", model="RTX 4060", 
                vram=8, memory_type="GDDR6", tdp=115, length=240, price=299.99),
            GPU(name="AMD Radeon RX 6600", brand="AMD", model="RX 6600", 
                vram=8, memory_type="GDDR6", tdp=132, length=235, price=259.99),
            GPU(name="NVIDIA GeForce RTX 2060", brand="NVIDIA", model="RTX 2060", 
                vram=6, memory_type="GDDR6", tdp=160, length=229, price=239.99),
        ]
        db.add_all(budget_gpus)
        
        # Add budget-friendly Motherboards
        budget_motherboards = [
            Motherboard(name="MSI PRO B660M-A", brand="MSI", model="PRO B660M-A", 
                        socket="LGA1700", form_factor="mATX", memory_slots=4, max_memory=128, price=129.99),
            Motherboard(name="Gigabyte B550M DS3H", brand="Gigabyte", model="B550M DS3H", 
                        socket="AM4", form_factor="mATX", memory_slots=4, max_memory=128, price=99.99),
            Motherboard(name="ASRock B660M Pro RS", brand="ASRock", model="B660M Pro RS", 
                        socket="LGA1700", form_factor="mATX", memory_slots=4, max_memory=128, price=119.99),
            Motherboard(name="ASUS PRIME B550M-A", brand="ASUS", model="PRIME B550M-A", 
                        socket="AM4", form_factor="mATX", memory_slots=4, max_memory=128, price=109.99),
            Motherboard(name="MSI B550M PRO-VDH WIFI", brand="MSI", model="B550M PRO-VDH WIFI", 
                        socket="AM4", form_factor="mATX", memory_slots=4, max_memory=128, price=124.99),
        ]
        db.add_all(budget_motherboards)
        
        # Add budget-friendly RAM
        budget_rams = [
            RAM(name="Corsair Vengeance LPX 16GB (2x8GB)", brand="Corsair", model="Vengeance LPX", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=49.99),
            RAM(name="G.Skill Aegis 16GB (2x8GB)", brand="G.Skill", model="Aegis", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=44.99),
            RAM(name="Crucial Ballistix 8GB", brand="Crucial", model="Ballistix", 
                capacity=8, type="DDR4", speed=3200, modules=1, price=34.99),
            RAM(name="TeamGroup T-FORCE VULCAN Z 16GB", brand="TeamGroup", model="T-FORCE VULCAN Z", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=47.99),
            RAM(name="Kingston FURY Beast 16GB", brand="Kingston", model="FURY Beast", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=52.99),
        ]
        db.add_all(budget_rams)
        
        # Add budget-friendly Power Supplies
        budget_power_supplies = [
            PowerSupply(name="EVGA 600 BQ", brand="EVGA", model="600 BQ", 
                       wattage=600, efficiency="80+ Bronze", modular=True, price=64.99),
            PowerSupply(name="Corsair CV650", brand="Corsair", model="CV650", 
                       wattage=650, efficiency="80+ Bronze", modular=False, price=59.99),
            PowerSupply(name="SeaSonic S12III 500W", brand="SeaSonic", model="S12III", 
                       wattage=500, efficiency="80+ Bronze", modular=False, price=54.99),
            PowerSupply(name="Thermaltake Smart 600W", brand="Thermaltake", model="Smart", 
                       wattage=600, efficiency="80+ White", modular=False, price=49.99),
            PowerSupply(name="EVGA 500 W1", brand="EVGA", model="500 W1", 
                       wattage=500, efficiency="80+ White", modular=False, price=44.99),
        ]
        db.add_all(budget_power_supplies)
        
        # Set up compatibility between CPUs and Motherboards
        for cpu in budget_cpus:
            for mb in budget_motherboards:
                if (cpu.socket == "LGA1700" and mb.socket == "LGA1700") or \
                   (cpu.socket == "AM4" and mb.socket == "AM4"):
                    cpu.compatible_motherboards.append(mb)
        
        db.commit()
        print("Added budget-friendly components to the database!")
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding budget-friendly components to database...")
    add_budget_components()
    print("Budget components added successfully!") 