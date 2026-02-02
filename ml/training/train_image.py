import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from ml.models.image_cnn import DeepfakeCNN

# -------------------------
# DEVICE
# -------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# -------------------------
# TRANSFORMS
# -------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# -------------------------
# DATASETS
# -------------------------
train_ds = datasets.ImageFolder(
    root="ml/datasets/split/train",
    transform=transform
)

val_ds = datasets.ImageFolder(
    root="ml/datasets/split/val",
    transform=transform
)

# -------------------------
# DATALOADERS (GPU OPTIMIZED)
# -------------------------
train_loader = DataLoader(
    train_ds,
    batch_size=32,
    shuffle=True,
    num_workers=0,   # 🔥 FIX
    pin_memory=True
)

val_loader = DataLoader(
    val_ds,
    batch_size=32,
    shuffle=False,
    num_workers=0,   # 🔥 FIX
    pin_memory=True
)


# -------------------------
# MODEL
# -------------------------
model = DeepfakeCNN().to(device)

criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

# -------------------------
# MIXED PRECISION (GPU SPEED BOOST)
# -------------------------
scaler = torch.cuda.amp.GradScaler(enabled=device.type == "cuda")

# -------------------------
# TRAINING LOOP
# -------------------------
EPOCHS = 3

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0

    for imgs, labels in train_loader:
        imgs = imgs.to(device, non_blocking=True)
        labels = labels.float().to(device, non_blocking=True)

        optimizer.zero_grad()

        with torch.cuda.amp.autocast(enabled=device.type == "cuda"):
            outputs = model(imgs).squeeze()
            loss = criterion(outputs, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        running_loss += loss.item()

    # -------------------------
    # VALIDATION
    # -------------------------
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs = imgs.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)

            outputs = model(imgs).squeeze()
            preds = (torch.sigmoid(outputs) > 0.5).long()

            correct += (preds == labels).sum().item()
            total += labels.size(0)

    acc = correct / total
    avg_loss = running_loss / len(train_loader)

    print(
        f"Epoch [{epoch+1}/{EPOCHS}] "
        f"Loss: {avg_loss:.4f} "
        f"Val Accuracy: {acc:.4f}"
    )

# -------------------------
# SAVE MODEL
# -------------------------
torch.save(model.state_dict(), "ml/checkpoints/image_model.pth")
print("✅ Model saved to ml/checkpoints/image_model.pth")
