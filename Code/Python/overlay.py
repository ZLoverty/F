"""
overlay.py
==========

Reads images from a folder and overlays the detected droplets on the images.
Saves the overlay images in a new folder "overlay". 

Syntax
------

python overlay.py folder

Edit
----
* Apr 21, 2025: Initial commit.
"""

import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from skimage import io
from myimagelib import readdata

parser = argparse.ArgumentParser(description='Overlay droplets on images')
parser.add_argument('folder', type=str, help='Folder containing images and data')
parser.add_argument('--dpi', type=int, default=300, help='Set the dpi of the saved images')
args = parser.parse_args()

# input args
folder = os.path.abspath(args.folder)
dpi = args.dpi

save_folder = os.path.join(folder, "overlay")
os.makedirs(save_folder, exist_ok=True)

l = readdata(folder, "jpg")
img = io.imread(l.Dir[0])
h, w = img.shape[:2]
for num, i in l.iterrows():
    if os.path.exists(os.path.join(save_folder, f"{i.Name}.jpg")):
        continue
    data_path = os.path.join(folder, f"{i.Name}.csv")
    img = io.imread(i.Dir)
    plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
    plt.imshow(img)
    plt.axis("off")
    try:
        drops = pd.read_csv(data_path)
        for _, drop in drops.iterrows():
            x, y, r = drop[["x", "y", "r"]].astype(int)
            circle = plt.Circle((x, y), r, color='yellow', fill=False, linewidth=2)
            plt.gca().add_artist(circle)
    except:
        pass

    # save image
    plt.savefig(os.path.join(save_folder, f"{i.Name}.jpg"), bbox_inches="tight", pad_inches=0)
    plt.close()