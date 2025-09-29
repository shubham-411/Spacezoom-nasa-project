from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# CORS setup to allow frontend (adjust port as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server if it's using vite or else update it
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder where images are stored
IMAGES_DIR = "images"

# API: this will fetch the frontend with the list of images
@app.get('/images')
def list_images():
    try:
        files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg','.png','.jpeg','.tif','.tiff','.bmp','.gif'))]
        return {"images": files}
    except FileNotFoundError:
        return {"images": []}

# API: this will return the exact  image requested
@app.get('/images/{image_name}')
def get_image(image_name: str):
    image_path = os.path.join(IMAGES_DIR, image_name)
    if not os.path.isfile(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
#i havent added the database extension yet will do it later