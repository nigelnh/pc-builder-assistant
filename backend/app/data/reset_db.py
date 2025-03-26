import sys
import os
import shutil

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.database import engine
from app.models.components import Base
import app.data.seed_db as seed_db

def reset_database():
    """Reset the database by dropping all tables and recreating them"""
    # Path to the database file
    db_path = os.path.join(os.path.dirname(__file__), 'components.db')
    
    # Delete the database file if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database file: {db_path}")
        try:
            # Close any connections to the database
            engine.dispose()
            # Remove the file
            os.remove(db_path)
        except Exception as e:
            print(f"Failed to remove database file: {e}")
            return False
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Seed the database with initial data
    print("Seeding database with initial data...")
    seed_db.seed_data()
    
    print("Database reset successfully!")
    return True

if __name__ == "__main__":
    print("WARNING: This will reset the database and all existing data will be lost.")
    confirm = input("Are you sure you want to continue? (y/n): ")
    
    if confirm.lower() == 'y':
        reset_database()
    else:
        print("Database reset cancelled.") 