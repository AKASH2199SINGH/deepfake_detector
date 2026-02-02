import torch
from PIL import Image
import torchvision.transforms as transforms

from backend.app.core.model_loader import model, device

# -------------------------
# TRANSFORM (MUST MATCH TRAINING)
# -------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -------------------------
# THRESHOLDS (CALIBRATED)
# -------------------------
AI_THRESHOLD = 0.75
REAL_THRESHOLD = 0.45

# -------------------------
# CORE INFERENCE
# -------------------------
def _run_inference(image: Image.Image):
    # 🔹 Size guard (VERY IMPORTANT for web images)
    w, h = image.size
    if w < 160 or h < 160:
        return {
            "label": "Uncertain",
            "confidence": 0,
            "reason": "Image too small"
        }

    tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        logits = model(tensor)
        score = torch.sigmoid(logits).item()  # probability of AI

    # 🔹 Decision logic
    if score >= AI_THRESHOLD:
        label = "AI Generated"
    elif score <= REAL_THRESHOLD:
        label = "Real"
    else:
        label = "Uncertain"

    ai_prob = score
    real_prob = 1 - score
    confidence = max(ai_prob, real_prob)

    return {
        "label": label,
        "confidence": round(confidence * 100, 1),
        "ai_probability": round(ai_prob * 100, 1)
    }

# -------------------------
# FILE UPLOAD (Swagger / API)
# -------------------------
def predict_image(file):
    image = Image.open(file.file).convert("RGB")
    return _run_inference(image)
