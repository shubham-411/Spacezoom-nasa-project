from .db import SessionLocal
from .models import User, Image
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

# Add demo user
demo_user = User(
    username="demo",
    email="demo@spacezoom.local",
    # password_hash=pwd_context.hash("demo123")
    password_hash="demo123"
)

demo_image = Image(
    filename="demo.jpg",
    title="Demo Image",
    description="This is a demo",
    width=800,
    height=600
)


db.add(demo_image)
db.commit()
db.close()
print("Seeded demo image.")

db.add(demo_user)

# Add a sample image (replace with actual filename in images/)
sample_image = Image(filename="example.jpg", title="Test Image", description="NASA sample")
db.add(sample_image)

db.commit()
db.close()
print("Demo user and image added to DB!")

for img in db.query(Image).all():
    print(img.filename, img.title)