import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine, SessionLocal
from app.models.components import Base, CPU, Motherboard
from sqlalchemy.orm import Session

def add_additional_cpus():
    db = SessionLocal()
    try:
        # Define additional CPUs with various price points
        additional_cpus = [
            # Budget AMD CPUs
            CPU(name="AMD Ryzen 3 4100", brand="AMD", model="Ryzen 3 4100", socket="AM4", 
                cores=4, threads=8, base_clock=3.8, boost_clock=4.0, tdp=65, price=89.99),
            CPU(name="AMD Ryzen 5 5500", brand="AMD", model="Ryzen 5 5500", socket="AM4", 
                cores=6, threads=12, base_clock=3.6, boost_clock=4.2, tdp=65, price=119.99),
            CPU(name="AMD Ryzen 5 5600", brand="AMD", model="Ryzen 5 5600", socket="AM4", 
                cores=6, threads=12, base_clock=3.5, boost_clock=4.4, tdp=65, price=149.99),
            CPU(name="AMD Ryzen 5 5600X", brand="AMD", model="Ryzen 5 5600X", socket="AM4", 
                cores=6, threads=12, base_clock=3.7, boost_clock=4.6, tdp=65, price=179.99),
                
            # Budget Intel CPUs
            CPU(name="Intel Core i3-12100F", brand="Intel", model="i3-12100F", socket="LGA1700", 
                cores=4, threads=8, base_clock=3.3, boost_clock=4.3, tdp=58, price=99.99),
            CPU(name="Intel Core i5-12400F", brand="Intel", model="i5-12400F", socket="LGA1700", 
                cores=6, threads=12, base_clock=2.5, boost_clock=4.4, tdp=65, price=159.99),
            CPU(name="Intel Core i5-13400F", brand="Intel", model="i5-13400F", socket="LGA1700", 
                cores=10, threads=16, base_clock=2.5, boost_clock=4.6, tdp=65, price=219.99),
            
            # Mid-range AMD CPUs
            CPU(name="AMD Ryzen 5 7600", brand="AMD", model="Ryzen 5 7600", socket="AM5", 
                cores=6, threads=12, base_clock=3.8, boost_clock=5.1, tdp=65, price=229.99),
            CPU(name="AMD Ryzen 7 5800X3D", brand="AMD", model="Ryzen 7 5800X3D", socket="AM4", 
                cores=8, threads=16, base_clock=3.4, boost_clock=4.5, tdp=105, price=349.99),
            CPU(name="AMD Ryzen 7 7800X3D", brand="AMD", model="Ryzen 7 7800X3D", socket="AM5", 
                cores=8, threads=16, base_clock=4.2, boost_clock=5.0, tdp=120, price=449.99),
            
            # Mid-range Intel CPUs
            CPU(name="Intel Core i5-14400F", brand="Intel", model="i5-14400F", socket="LGA1700", 
                cores=10, threads=16, base_clock=2.5, boost_clock=4.7, tdp=65, price=249.99),
            CPU(name="Intel Core i5-13600KF", brand="Intel", model="i5-13600KF", socket="LGA1700", 
                cores=14, threads=20, base_clock=3.5, boost_clock=5.1, tdp=125, price=299.99),
            CPU(name="Intel Core i7-13700F", brand="Intel", model="i7-13700F", socket="LGA1700", 
                cores=16, threads=24, base_clock=2.1, boost_clock=5.2, tdp=65, price=369.99),
            
            # High-end AMD CPUs
            CPU(name="AMD Ryzen 9 5950X", brand="AMD", model="Ryzen 9 5950X", socket="AM4", 
                cores=16, threads=32, base_clock=3.4, boost_clock=4.9, tdp=105, price=499.99),
            CPU(name="AMD Ryzen 9 7900X3D", brand="AMD", model="Ryzen 9 7900X3D", socket="AM5", 
                cores=12, threads=24, base_clock=4.4, boost_clock=5.6, tdp=120, price=599.99),
            
            # High-end Intel CPUs
            CPU(name="Intel Core i7-14700KF", brand="Intel", model="i7-14700KF", socket="LGA1700", 
                cores=20, threads=28, base_clock=3.4, boost_clock=5.5, tdp=125, price=399.99),
            CPU(name="Intel Core i9-13900KF", brand="Intel", model="i9-13900KF", socket="LGA1700", 
                cores=24, threads=32, base_clock=3.0, boost_clock=5.8, tdp=125, price=569.99),
            CPU(name="Intel Core i9-14900KS", brand="Intel", model="i9-14900KS", socket="LGA1700", 
                cores=24, threads=32, base_clock=3.2, boost_clock=6.2, tdp=150, price=699.99),
        ]
        
        # Add all CPUs to the database
        db.add_all(additional_cpus)
        
        # Set compatibility with existing motherboards
        # Get all motherboards
        am4_motherboards = db.query(Motherboard).filter(Motherboard.socket == "AM4").all()
        am5_motherboards = db.query(Motherboard).filter(Motherboard.socket == "AM5").all()
        lga1700_motherboards = db.query(Motherboard).filter(Motherboard.socket == "LGA1700").all()
        
        # Set compatibility relationships
        for cpu in additional_cpus:
            if cpu.socket == "AM4":
                for mb in am4_motherboards:
                    cpu.compatible_motherboards.append(mb)
            elif cpu.socket == "AM5":
                for mb in am5_motherboards:
                    cpu.compatible_motherboards.append(mb)
            elif cpu.socket == "LGA1700":
                for mb in lga1700_motherboards:
                    cpu.compatible_motherboards.append(mb)
        
        db.commit()
        return len(additional_cpus)
    
    finally:
        db.close()

if __name__ == "__main__":
    print("Adding additional CPUs to the database...")
    count = add_additional_cpus()
    print(f"Successfully added {count} additional CPUs!") 