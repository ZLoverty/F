"""
stackshot_preprocess.py
=======================

Description
-----------

This script puts stackshot images in separate folders, each of which contains a single stack of images. This is a necessary preprocessing for the program CZPBatch.exe to work properly. The folders will be named as stack%04d, starting from 0. The folder of images will be provided as a string argument. The number of images per stack will be provided as an integer argument. 

Syntax
------

python image_folder number_of_images_per_stack

Edit
----

Jun 28, 2024: Initial commit.
"""

import sys
import os

from myimagelib.myImageLib import readdata

image_folder = sys.argv[1]
nImages = int(sys.argv[2])

l = readdata(image_folder, "jpg")

# out folder numbering
j = 0

for s in range(len(l)//nImages+1):
    
    # create out folder
    out_folder = os.path.join(image_folder, "stack{:04d}".format(j))
    if os.path.exists(out_folder) == False:
        os.makedirs(out_folder)

    # move images to out folder    
    for num, i in l[s*nImages: (s+1)*nImages].iterrows():
        os.rename(i.Dir, os.path.join(out_folder, i.Name+".jpg"))
    
    j += 1