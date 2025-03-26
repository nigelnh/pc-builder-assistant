from app.models.database import engine
from app.models.components import Base as ComponentBase
from app.models.builds import Base as BuildBase

def create_tables():
    print("Creating database tables...")
    
    # Create component tables
    ComponentBase.metadata.create_all(bind=engine)
    print("Component tables created successfully")
    
    # Create build tables
    BuildBase.metadata.create_all(bind=engine)
    print("Build tables created successfully")
    
    print("All tables created successfully")

if __name__ == "__main__":
    create_tables() 