import cv2
import tempfile
import torch
from PIL import Image
import torchvision.transforms as transforms
# from app.core.model_loader import model, device
from backend.app.core.model_loader import model, device


transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict_video(file):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(file.file.read())

    cap = cv2.VideoCapture(temp.name)
    scores = []

    while len(scores) < 15:
        ret, frame = cap.read()
        if not ret:
            break

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            score = torch.sigmoid(model(tensor)).item()
            scores.append(score)

    cap.release()

    avg = sum(scores) / len(scores)
    label = "AI Generated" if avg > 0.5 else "Real"

    return {
        "label": label,
        "confidence": round(avg, 3)
    }
