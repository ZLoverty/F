import glob
import os

folder = r"F:\F\05282025\exp7_stack"

l = glob.glob(os.path.join(folder, "*.jpg"))

for i, item in enumerate(l):
    os.rename(item, os.path.join(folder, f"{i:04d}.jpg"))