"""
stackshot_preprocess.py
=======================

Description
-----------

This script puts stackshot images in separate folders, each of which contains a single stack of images. This is a necessary preprocessing for the program CZPBatch.exe to work properly. The folders will be named as stack%04d, starting from 0. The folder of images will be provided as a string argument. The number of images per stack will be provided as an integer argument. 

Syntax
------

python stackshot_preprocess.py image_folder number_of_images_per_stack [-r reverse]

* image_folder: The folder of images to be processed.
* number_of_images_per_stack: The number of images per stack.
* -r reverse: Reverse action, to move images back to the original folder.

Edit
----

Jun 28, 2024: Initial commit.
Feb 20, 2025: Add a reverse action, to move images back to the original folder.
"""

import os
import argparse
from myimagelib.myImageLib import readdata
import shutil

argparse = argparse.ArgumentParser(description="Put stackshot images in separate folders, each of which contains a single stack of images. This is a necessary preprocessing for the program CZPBatch.exe to work properly. The folders will be named as stack%04d, starting from 0. The folder of images will be provided as a string argument. The number of images per stack will be provided as an integer argument.")
argparse.add_argument("image_folder", type=str, help="The folder of images to be processed.")
argparse.add_argument("nImages", type=int, help="The number of images per stack.")
argparse.add_argument("-r", "--reverse", default=0, help="Reverse action, to move images back to the original folder.")
args = argparse.parse_args()

image_folder = args.image_folder
nImages = args.nImages

if not args.reverse:
    

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
else:
    # reverse action
    sfL = next(os.walk(image_folder))[1]
    for sf in sfL:
        l = readdata(os.path.join(image_folder, sf), "jpg")
        # move images to out folder
        for num, i in l.iterrows():
            os.rename(i.Dir, os.path.join(image_folder, i.Name+".jpg"))
        shutil.rmtree(os.path.join(image_folder, sf))
