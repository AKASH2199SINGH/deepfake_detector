from fastapi import APIRouter, UploadFile, File
# from app.services.video_infer import predict_video
from backend.app.services.video_infer import predict_video


router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    return predict_video(file)
