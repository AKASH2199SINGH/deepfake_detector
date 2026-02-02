import torch.nn as nn
from torchvision import models

class DeepfakeCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = models.efficientnet_b0(pretrained=True)
        self.model.classifier[1] = nn.Linear(1280, 1)

    def forward(self, x):
        return self.model(x)
