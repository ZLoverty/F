"""
find_drops.py
=============

This script is used to find the drops in the data. It uses the data from the condensation experiment images to find the drops. The script uses the following steps to find the drops:

1. read the image;
2. preprocess the image, including: gray_scale, blur and erode;
3. detect dark blobs in the image using `cv2.SimpleBlobDetector`;
4. adaptively refine the detection results using either `expand_blob` or `refine_with_hough` function.

This script reads an .avi video as the input image and saves the detected drops as a .csv file, which contains the x, y coordinates and the radius of the drops in each frame. It takes the path of the video `folder/{name}.avi` as the input argument and saves the .csv file in a subdirectory of the video folder `folder/tracking/{name}/blob/%04d.csv`

Syntax
------

```
python find_drops.py video_path [--start_frame start_frame]
```

Edit
----

Sep 12, 2024: Initial commit. 
Sep 18, 2024: Add tolerance to expand_blob function.
Oct 07, 2024: Add refine_with_hough function to refine the detected droplets using Hough circle transform.
Oct 14, 2024: Process images in separate files, instead of a video. This allows for easier testing on individual frames.
"""

import cv2
import numpy as np
import pandas as pd
import os
import argparse
from myimagelib.myImageLib import show_progress, readdata
import pdb

#function to exrtract frames from a video file
def get_frame_from_video(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not read frame {frame_number}")
    return frame

def preprocess(frame):
    #preprocessing frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    # use gaussian blur
    blurred_frame = cv2.GaussianBlur(gray_frame, (7,7), 11) # Apply Gaussian blur to reduce noise
    kernel = np.ones((3, 3), np.uint8)  # Erode the image to shrink white regions and expand dark regions
    eroded = cv2.erode(blurred_frame, kernel, iterations=1)
    return eroded

def detect_droplets(frame):
    # Set up SimpleBlobDetector parameters
    params = cv2.SimpleBlobDetector_Params()

    # filter color
    params.blobColor = 0

    # Change thresholds
    params.minThreshold = 100
    params.maxThreshold = 255

    # Filter by Area
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 10000

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.5

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.5

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    # Step 5: Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs
    keypoints = detector.detect(frame)

    return keypoints

def calculate_mean_brightness(image, center, radius):
    mask = np.zeros(image.shape, dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, thickness=cv2.FILLED)
    mean_val = cv2.mean(image, mask=mask)[0]
    return mean_val

def expand_blob(image, keypoint, max_iterations=10, step=1, tolerance=0.01):
    x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
    initial_radius = int(keypoint.size / 2)
    best_radius = initial_radius
    best_brightness = calculate_mean_brightness(image, (x, y), initial_radius)
    
    for _ in range(max_iterations):
        expanded_radius = best_radius + step
        expanded_brightness = calculate_mean_brightness(image, (x, y), expanded_radius)
        
        if expanded_brightness > best_brightness * (1 + tolerance):
            best_brightness = expanded_brightness
            best_radius = expanded_radius
        else:
            break

    return best_radius * 2
    
    

def refine_with_hough(image, keypoint):
    """
    Refine the keypoints using the Hough circle transform
    """
    h, w = image.shape
    x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
    r = int(keypoint.size / 2)
    x1, x2 = max(0, x-2*r), min(x+2*r, w)
    y1, y2 = max(0, y-2*r), min(y+2*r, h)
    roi = image[y1:y2, x1:x2]
    circles = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, dp=1, minDist=4*r, param1=1, param2=10, minRadius=r, maxRadius=3*r)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        cx, cy, radius = circles[0, 0]
        return cx+x1, cy+y1, radius*2
    else:
        return x, y, r*2

if __name__ == "__main__":

    # parse the input arguments
    parser = argparse.ArgumentParser(description="Find droplets in the video")
    parser.add_argument("img_path", type=str, help="Path to the images to be analyzed")
    args = parser.parse_args()
    
    img_path = args.img_path

    # read the video and detect droplets
    # cap = cv2.VideoCapture(video_path)
    # ret = True
    # frame_number = 0
    # while ret:
    #     if frame_number < start_frame:
    #         ret, _ = cap.read()
    #         frame_number += 1
    #         continue

    #     # Read the frame
    #     ret, frame = cap.read()
    #     print(f"Processing frame {frame_number}\n")
    l = readdata(img_path, "jpg")
    for num, i in l.iterrows():
        frame = cv2.imread(i.Dir)

        # detect droplets
        processed = preprocess(frame)
        keypoints = detect_droplets(processed)

        # refine detected droplets
        refined_keypoints = []
        for j, keypoint in enumerate(keypoints):
            # here, we experiment different methods to refine the detected droplets
            # available methods: expand_blob, refine_with_hough
            # if expand_blob is used:
            # x, y = keypoint.pt
            # refined_keypoints.append((x, y, expand_blob(processed, keypoint)))
            # if refine_with_hough is used:
            refined_keypoints.append(refine_with_hough(processed, keypoint))
            show_progress(j/len(keypoints), label=f"Refining {j+1:d}/{len(keypoints):d}")

        # save the data in a csv file
        data = [[keypoint[0], keypoint[1], keypoint[2] / 2] for keypoint in refined_keypoints]
        df = pd.DataFrame(data, columns=["x", "y", "r"])
        df.to_csv(os.path.join(img_path, f"{i.Name}.csv"), index=False)