from .db import engine
from .models import Base

# Create all tables
Base.metadata.create_all(bind=engine)
print("Database and tables created successfully!")
