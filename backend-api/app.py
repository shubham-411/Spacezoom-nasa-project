from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

# Import database session manager and ORM models
from database.db import get_db
from database.models import Image, Annotation, User

app = FastAPI()

@app.get("/tiles/{image_name}/{x}/{y}")
def get_tile(image_name: str, x: int, y: int, tile_size: int = 256):
    # Construct expected path: tiles/{image_name}/{image_name}_tile_{x}_{y}.jpg
    img_dir = os.path.splitext(image_name)[0]
    tile_filename = f"{img_dir}_tile_{x}_{y}.jpg"
    tile_path = os.path.join("tiles", img_dir, tile_filename)
    if not os.path.isfile(tile_path):
        raise HTTPException(status_code=404, detail="Tile not found")
    return FileResponse(tile_path)

# CORS setup: allow frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for status check
@app.get("/")
def read_root():
    return {"message": "Server is running!"}

# List all image metadata from DB
@app.get("/images")
def list_images(db: Session = Depends(get_db)):
    images = db.query(Image).all()
    return {"images": [
        {
            "filename": img.filename,
            "title": img.title,
            "description": img.description,
            "width": img.width,
            "height": img.height
        } for img in images
    ]}

# Serve a specific image file by filename
@app.get("/images/{image_name}")
def get_image(image_name: str, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.filename == image_name).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found in DB")
    image_path = os.path.join("images", image_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image file not found")
    return FileResponse(image_path)

# Get all annotations for a specific image
@app.get("/annotations/{image_name}")
def get_annotations(image_name: str, db: Session = Depends(get_db)):
    annotations = db.query(Annotation).filter(
        Annotation.image_filename == image_name
    ).all()
    return {"annotations": [
        {"x": a.x, "y": a.y, "label": a.label, "user_id": a.user_id}
        for a in annotations
    ]}

# Add a new annotation to an image
class AnnotationIn(BaseModel):
    x: float
    y: float
    label: str
    image_filename: str
    user_id: int

@app.post("/annotations")
def add_annotation(annotation: AnnotationIn, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.filename == annotation.image_filename).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found in DB")
    new_annot = Annotation(
        x=annotation.x,
        y=annotation.y,
        label=annotation.label,
        image_filename=annotation.image_filename,
        user_id=annotation.user_id
    )
    db.add(new_annot)
    db.commit()
    db.refresh(new_annot)
    return {
        "message": "Annotation added",
        "annotation": {
            "x": new_annot.x,
            "y": new_annot.y,
            "label": new_annot.label
        }
    }
