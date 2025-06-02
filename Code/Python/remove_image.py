"""
remove_image.py
===============

This script removes an image in each stack. The image to be removed is stacked by an integer. For example, 0 means removing the first image in each folder.

python remove_image.py folder to_remove

* folder: folder with folders of stacks
* to_remove: integer, number of the image to be removed

Edit
----
Jun 02, 2025: Initial commit.
"""

import re
import glob
import os
import shutil
import argparse

argparse = argparse.ArgumentParser(description="This script removes an image in each stack. The image to be removed is stacked by an integer. For example, 0 means removing the first image in each folder.")
argparse.add_argument("folder", type=str, help="The folder of image stacks to be processed.")
argparse.add_argument("to_remove", type=int, help="The number of images per stack.")
args = argparse.parse_args()

folder = args.folder
to_remove = args.to_remove

def extract_number(filename):
    match = re.search(r'Img(\d+)\.jpg', filename)
    return int(match.group(1)) if match else -1

sfL = next(os.walk(folder))[1]

for sf in sfL:
    l = glob.glob(os.path.join(folder, sf, "*.jpg"))
    l.sort(key=extract_number)
    os.remove(l[to_remove])