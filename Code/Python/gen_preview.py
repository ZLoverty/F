"""
gen_preview.py
==============

Description
-----------
This script generates a preview of the video file by drawing circles around the detected droplets in each frame. It reads the .csv file containing the x, y coordinates and the radius of the droplets in each frame and saves the preview as a .avi video file in the same directory as the input video.

Syntax
------
python gen_preview.py video_path

Edit
----
Sep 12, 2024: Initial commit.
"""

import cv2
import numpy as np
import pandas as pd
import os
import argparse
from myimagelib.myImageLib import show_progress, readdata
import matplotlib.pyplot as plt

#function to exrtract frames from a video file
def get_frame_from_video(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not read frame {frame_number}")
    return frame

if __name__ == "__main__":
    # process arguments
    parser = argparse.ArgumentParser(description='Generate preview of droplet detection')
    parser.add_argument('video_path', type=str, help='Path to the video file')
    args = parser.parse_args()

    # process paths
    video_path = args.video_path
    folder, filename = os.path.split(video_path)
    name, _ = os.path.splitext(filename)
    blob_folder = os.path.join(folder, 'tracking', os.path.splitext(os.path.basename(video_path))[0], 'blob')
    overlay_folder = os.path.join(blob_folder, 'overlay')

    # create overlay folder
    os.makedirs(overlay_folder, exist_ok=True)

    # if filelist exists, remove it
    if os.path.exists(os.path.join(overlay_folder, "filelist.txt")):
        os.remove(os.path.join(overlay_folder, "filelist.txt"))

    # # loop over the frames
    l = readdata(blob_folder, "csv")
    for num, i in l.iterrows():
        frame_num = int(i.Name)
        show_progress(num/len(l), f"Processing frame {frame_num}")

        # generate filelist for ffmpeg
        with open(os.path.join(overlay_folder, "filelist.txt"), "a") as f:
            f.write(f"file '{os.path.join(overlay_folder, f'{frame_num:04d}.jpg')}'\n")

        # read the frame and the droplets detection data
        frame = get_frame_from_video(video_path, frame_num)
        h, w = frame.shape[:2]
        droplets = pd.read_csv(i.Dir)

        # create keypoints
        keypoints = []
        for _, droplet in droplets.iterrows():
            x, y, r = droplet[["x", "y", "r"]]
            keypoints.append(cv2.KeyPoint(x, y, r * 2))

        # Display the output image
        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
                                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # convert to rgb
        rgb = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2RGB)

        # save overlay image
        dpi = 600
        plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
        plt.imshow(rgb)
        plt.axis("off")
        plt.savefig(os.path.join(overlay_folder, f"{frame_num:04d}.jpg"), bbox_inches="tight", pad_inches=0)
        plt.close()

        # save raw image for manual correction
        cv2.imwrite(os.path.join(blob_folder, f"{frame_num:04d}.jpg"), frame)
    
    # create video from images
    os.system(f"ffmpeg -f concat -safe 0 -i {os.path.join(overlay_folder, 'filelist.txt')} -vf \"scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p\" -c:v libx264 -r 10 {os.path.join(blob_folder, 'preview.mp4')} -y")