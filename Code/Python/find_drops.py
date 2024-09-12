"""
find_drops.py
=============

This script is used to find the drops in the data. It uses the data from the condensation experiment images to find the drops. The script uses the following steps to find the drops:

1. read the image;
2. preprocess the image, including: gray_scale, blur and erode;
3. detect dark blobs in the image using `cv2.SimpleBlobDetector`;
4. adaptively expand the blobs to include the bright contour.

This script reads an .avi video as the input image and saves the detected drops as a .csv file, which contains the x, y coordinates and the radius of the drops in each frame. It takes the path of the video `folder/{name}.avi` as the input argument and saves the .csv file in a subdirectory of the video folder `folder/tracking/{name}/blob/%04d.csv`

Syntax
------

```
python find_drops.py video_path
```

Edit
----

Sep 12, 2024: Initial commit. 

"""

import cv2
import numpy as np
import pandas as pd
import os
import argparse
from myimagelib.myImageLib import show_progress

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

def expand_blob(image, keypoint, max_iterations=10, step=1):
    x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
    initial_radius = int(keypoint.size / 2)
    best_radius = initial_radius
    best_brightness = calculate_mean_brightness(image, (x, y), initial_radius)
    
    for _ in range(max_iterations):
        expanded_radius = best_radius + step
        expanded_brightness = calculate_mean_brightness(image, (x, y), expanded_radius)
        
        if expanded_brightness > best_brightness:
            best_brightness = expanded_brightness
            best_radius = expanded_radius
        else:
            break
    
    keypoint.size = best_radius * 2  # Update the size attribute of the keypoint


if __name__ == "__main__":

    # parse the input arguments
    parser = argparse.ArgumentParser(description="Find droplets in the video")
    parser.add_argument("video_path", type=str, help="Path to the video file")
    parser.add_argument("--start_frame", type=int, default=25, help="Frame number to start processing")
    args = parser.parse_args()
    
    video_path = args.video_path
    start_frame = args.start_frame

    # create data folder for output
    folder, filename = os.path.split(video_path)
    name, _ = os.path.splitext(filename)
    data_folder = os.path.join(folder, "tracking", name, "blob")
    os.makedirs(data_folder, exist_ok=True)

    # read the video and detect droplets
    cap = cv2.VideoCapture(video_path)
    ret = True
    frame_number = 0
    while ret:
        if frame_number < start_frame:
            ret, _ = cap.read()
            frame_number += 1
            continue

        # Read the frame
        ret, frame = cap.read()
        print(f"Processing frame {frame_number}\n")

        # detect droplets
        processed = preprocess(frame)
        keypoints = detect_droplets(processed)

        # refine detected droplets
        for i, keypoint in enumerate(keypoints):
            expand_blob(processed, keypoint)
            show_progress(i/len(keypoints), label=f"Refining {i+1:d}/{len(keypoints):d}")

        # save the data in a csv file
        data = [[keypoint.pt[0], keypoint.pt[1], keypoint.size / 2] for keypoint in keypoints]
        df = pd.DataFrame(data, columns=["x", "y", "r"])
        df.to_csv(os.path.join(data_folder, f"{frame_number:04d}.csv"), index=False)

        frame_number += 1