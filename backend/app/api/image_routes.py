from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from fastapi import APIRouter, UploadFile, File
from backend.app.services.image_infer import predict_image

router = APIRouter()

# 🔹 IMAGE BYTES ONLY (Chrome Extension + Swagger)
@router.post("/predict/image-bytes")
async def predict_image_bytes(file: UploadFile = File(...)):
    return predict_image(file)
