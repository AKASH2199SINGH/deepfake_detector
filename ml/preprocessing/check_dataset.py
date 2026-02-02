import os

real_dir = "ml/datasets/image/real"
fake_dir = "ml/datasets/image/fake"

real_count = len(os.listdir(real_dir))
fake_count = len(os.listdir(fake_dir))

print("Real images:", real_count)
print("Fake images:", fake_count)

print("Using for training:")
print("Real:", min(real_count, fake_count))
print("Fake:", min(real_count, fake_count))
