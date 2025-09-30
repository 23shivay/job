# db/init_db.py
from .database import engine, Base
from . import models

def init():
    print("📦 Creating tables in database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    init()
