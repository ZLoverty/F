---
date: 2024-10-07
title: blob and hough
---

# Blob and Hough

To detect condensation droplets in images, I've been working with primarily two methods, `simpleBlobDetector` and `HoughCircle`, both from the `opencv` package. `HoughCircle` is good at detecting circles, but it requires a minimum and a maximum radius as input arguments to work. This limits its use in an image with big variations of circle size. `simpleBlobDetector`, on the other hand, detects blobs of various sizes well, but it does not always identify the bright contour as the droplet. Instead, it usually detects the dark core of droplets, which significantly underestimate the droplet size. 

To utilize the advantage of both methods, here I consider to combine them in order: first apply `simpleBlobDetector` to get the location of droplets, then crop the image in the vicinity of each detected droplet, and finally use `HoughCircle` to refine the droplet detection. 

The following image shows a comparison between pure `impleBlobDetector` and `blob+hough`. For most detection, `blob+hough` increases the size of the detected droplet. Most of them are improved, with a few detections too big. `blob+hough` also amplifies the many wrong detections with were so small that were often overlooked. This is another asset of this method. With `blob+hough` detection, less manual correction is needed and the mistaken detections are easier to spot. 

<img src="/assets/images/2024/10/blob-hough-comparison.png" width=500px>  