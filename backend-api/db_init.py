from backend.db import engine, Base
from backend.models import *  # Import all your models

# This will create all tables in your SQLite DB
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
