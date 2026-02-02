import torch
from ml.models.image_cnn import DeepfakeCNN

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = DeepfakeCNN().to(device)
model.load_state_dict(
    torch.load("ml/checkpoints/image_model.pth", map_location=device)
)
model.eval()
