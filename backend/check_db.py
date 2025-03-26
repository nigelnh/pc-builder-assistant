from app.models.database import SessionLocal
from app.models.components import CPU, GPU, Motherboard, RAM, PowerSupply

def check_database():
    db = SessionLocal()
    try:
        # Check CPUs
        cpus = db.query(CPU).all()
        print(f"Number of CPUs in database: {len(cpus)}")
        print("\nCPU Models:")
        for cpu in cpus:
            print(f"- {cpu.brand} {cpu.model} (Socket: {cpu.socket})")
        
        # Check for AM5 socket CPUs (like Ryzen 7600X)
        am5_cpus = db.query(CPU).filter(CPU.socket == "AM5").all()
        print(f"\nNumber of AM5 socket CPUs: {len(am5_cpus)}")
        if am5_cpus:
            for cpu in am5_cpus:
                print(f"- {cpu.brand} {cpu.model}")
        
        # Check GPUs
        gpus = db.query(GPU).all()
        print(f"\nNumber of GPUs in database: {len(gpus)}")
        
        # Check Motherboards
        motherboards = db.query(Motherboard).all()
        print(f"Number of Motherboards in database: {len(motherboards)}")
        
        # Check RAM
        rams = db.query(RAM).all()
        print(f"Number of RAM modules in database: {len(rams)}")
        
        # Check Power Supplies
        power_supplies = db.query(PowerSupply).all()
        print(f"Number of Power Supplies in database: {len(power_supplies)}")
        
    finally:
        db.close()

if __name__ == "__main__":
    check_database() 