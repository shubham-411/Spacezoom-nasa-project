# backend/create_tables.py
from backend.db import Base, engine
from backend.models import Image  # import all models here

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
