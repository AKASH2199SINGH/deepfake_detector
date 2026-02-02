import os
import shutil
import random

BASE_DIR = "ml/datasets/image"
OUT_DIR = "ml/datasets/split"
TRAIN_RATIO = 0.8

for cls in ["real", "fake"]:
    src = os.path.join(BASE_DIR, cls)
    images = os.listdir(src)
    random.shuffle(images)

    limit = 5000  # balance
    images = images[:limit]

    train_cut = int(len(images) * TRAIN_RATIO)

    train_imgs = images[:train_cut]
    val_imgs = images[train_cut:]

    for phase, imgs in [("train", train_imgs), ("val", val_imgs)]:
        dst = os.path.join(OUT_DIR, phase, cls)
        os.makedirs(dst, exist_ok=True)
        for img in imgs:
            shutil.copy(os.path.join(src, img), os.path.join(dst, img))

    print(f"{cls}: train={len(train_imgs)}, val={len(val_imgs)}")
