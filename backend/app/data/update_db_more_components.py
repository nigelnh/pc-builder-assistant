import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, RAM, PowerSupply
from sqlalchemy.orm import Session

def add_additional_components():
    db = SessionLocal()
    try:
        # Define RAM options with various price points
        additional_ram = [
            # Budget RAM
            RAM(name="Crucial 16GB DDR4", brand="Crucial", model="DDR4", 
                capacity=16, type="DDR4", speed=3200, modules=2, price=49.99),
            RAM(name="G.Skill Ripjaws V 16GB", brand="G.Skill", model="Ripjaws V", 
                capacity=16, type="DDR4", speed=3600, modules=2, price=59.99),
            RAM(name="Corsair Vengeance LPX 16GB", brand="Corsair", model="Vengeance LPX", 
                capacity=16, type="DDR4", speed=3600, modules=2, price=64.99),
                
            # Mid-range RAM
            RAM(name="G.Skill Trident Z RGB 32GB DDR4", brand="G.Skill", model="Trident Z RGB", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=129.99),
            RAM(name="Corsair Vengeance RGB PRO 32GB", brand="Corsair", model="Vengeance RGB PRO", 
                capacity=32, type="DDR4", speed=3600, modules=2, price=139.99),
            RAM(name="Crucial 32GB DDR5", brand="Crucial", model="DDR5", 
                capacity=32, type="DDR5", speed=4800, modules=2, price=119.99),
                
            # High-end RAM
            RAM(name="G.Skill Trident Z5 RGB 64GB", brand="G.Skill", model="Trident Z5 RGB", 
                capacity=64, type="DDR5", speed=6000, modules=2, price=299.99),
            RAM(name="Corsair Dominator Platinum RGB 64GB", brand="Corsair", model="Dominator Platinum RGB", 
                capacity=64, type="DDR5", speed=6400, modules=2, price=339.99),
        ]
        
        # Define power supplies with various price points
        additional_psus = [
            # Budget PSUs
            PowerSupply(name="EVGA 500 W1", brand="EVGA", model="500 W1", 
                        wattage=500, efficiency="80+ White", modular=False, price=44.99),
            PowerSupply(name="Corsair CV550", brand="Corsair", model="CV550", 
                        wattage=550, efficiency="80+ Bronze", modular=False, price=54.99),
            PowerSupply(name="Thermaltake Smart 600W", brand="Thermaltake", model="Smart 600W", 
                        wattage=600, efficiency="80+ White", modular=False, price=49.99),
                        
            # Mid-range PSUs
            PowerSupply(name="Corsair RM650", brand="Corsair", model="RM650", 
                        wattage=650, efficiency="80+ Gold", modular=True, price=109.99),
            PowerSupply(name="EVGA SuperNOVA 750 G6", brand="EVGA", model="SuperNOVA 750 G6", 
                        wattage=750, efficiency="80+ Gold", modular=True, price=119.99),
            PowerSupply(name="Seasonic FOCUS GX-750", brand="Seasonic", model="FOCUS GX-750", 
                        wattage=750, efficiency="80+ Gold", modular=True, price=129.99),
                        
            # High-end PSUs
            PowerSupply(name="Corsair HX1000", brand="Corsair", model="HX1000", 
                        wattage=1000, efficiency="80+ Platinum", modular=True, price=219.99),
            PowerSupply(name="Seasonic PRIME TX-1000", brand="Seasonic", model="PRIME TX-1000", 
                        wattage=1000, efficiency="80+ Titanium", modular=True, price=299.99),
            PowerSupply(name="EVGA SuperNOVA 1300 T2", brand="EVGA", model="SuperNOVA 1300 T2", 
                        wattage=1300, efficiency="80+ Titanium", modular=True, price=349.99),
        ]
        
        # Add all components to the database
        db.add_all(additional_ram)
        db.add_all(additional_psus)
        db.commit()
        
        return {
            'ram': len(additional_ram),
            'psus': len(additional_psus)
        }
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding additional RAM and power supply options to the database...")
    result = add_additional_components()
    print(f"Successfully added {result['ram']} RAM modules and {result['psus']} power supplies!") 