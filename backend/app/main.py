from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.image_routes import router as image_router
from backend.app.api.video_routes import router as video_router

app = FastAPI(title="Deepfake Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # chrome-extension allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Deepfake Detector API running"}

app.include_router(image_router, prefix="/image", tags=["Image"])
app.include_router(video_router, prefix="/video", tags=["Video"])
