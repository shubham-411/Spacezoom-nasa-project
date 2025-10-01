from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

# Import database session and models
from backend.db import get_db
from backend.models import Image, Annotation, User

app = FastAPI()

# CORS setup: allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update if your frontend port differs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Endpoint: list all images
# -------------------------
@app.get("/images")
def list_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return {"images": [img.filename for img in images]}


# -----------------------------------
# Endpoint: serve an image by filename
# -----------------------------------
@app.get("/images/{image_name}")
def get_image(image_name: str, db: Session = Depends(get_db)):
    # Check DB if image exists
    image = db.query(Image).filter(Image.filename == image_name).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found in DB")

    # Serve the actual file
    image_path = os.path.join("images", image_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")

    return FileResponse(image_path)


@app.get("/")
def read_root():
    return {"message": "Server is running!"}


# -------------------------
# Placeholder for annotations
# -------------------------
@app.get("/annotations/{image_name}")
def get_annotations(image_name: str, db: Session = Depends(get_db)):
    annotations = db.query(Annotation).filter(Annotation.image_filename == image_name).all()
    return {"annotations": [{"x": a.x, "y": a.y, "label": a.label} for a in annotations]}
