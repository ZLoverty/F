---
date: 2025-01-21
title: screen droplet detection parameters
---

# Screen droplet detection parameters

In [the previous note](2025-01-15-assume-constant-flux.md), we analyzed the vapor flux at early times. It seemed that the flux closer to the fungal patch is smaller than that farther away, in qualitative agreement with the theory. A problem of the data in the previous note is that there are only two frames. We could verify this trend by analyzing the frames in between these two frames. However, due to the large number of droplets and the inaccurate algorithm detection, this task is very time consuming. 

To improve the droplet detection algorithm performance, I'm doing a parameter screening here. Our starting point is a ground truth detection that I labeled manually. A snapshot is shown below.

<img src="/assets/images/2025/01/ground-truth-overlay.png" width=700px>

The droplet detection algorithm is the `SimpleBlobDetector` by OpenCV. It has a few parameters that can be tuned to improve detection result, namely `minThreshold`, `maxThreshold`, `minCircularity`, `minConvexity` and `minInertiaRatio`. It is unclear what's the best set of parameters. Here, I screen a range of parameter set and compare the results with the ground truth to measure the performance. 

## Parameter sets

```
params = {}
params["minThreshold"] = range(0, 250, 0)
params["maxThreshold"] = range(50, 300, 0)
params["circularity"] = [0.2, 0.4, 0.5, 0.6, 0.8]
params["convexity"] = [0.2, 0.4, 0.5, 0.6, 0.8]
params["inertia"] = [0.2, 0.4, 0.5, 0.6, 0.8]
```

Each of these varied parameters are tested against a set of default values [0, 255, 0.5, 0.5, 0.5]. 

## Performance measures

We want to detect droplet location correctly. In the mean time, we want to minimize the wrong detections. Therefore, we use two numbers to evaluate the performance of the detection parameter sets. 

1. True positive (TP): the correctly detected droplet number / total droplets, we want to maximize this number. 
2. False positive (FP): the wrongly detected droplet number / total detected droplets, we want to minimize this number.
3. Size error (SE): the error

As a result, we use TP - FP as a score to measure the location accuracy. The SA will be used later when we address the droplet size. 

## Results

We plot the TP, FP, SE as functions of all the parameters, including the overlap detection tolerance. The results are shown below.

<img src="/assets/images/2025/01/droplet-detection-params-screen.png" width=600px>

## Refining the detections

The `SimpleBlobDetector` method does not give good size detection. While the droplets typical appear as a dark core surrounded by a bright ring, the detector usually only get the dark core, thus underestimate the droplet size. To get more accurate size detection, I developed two refine schemes: adaptive expansion and hough circle. The former gradually expand the detection and stop when the mean intensity along the edge reaches maximum. The hough circle is to look for circle in the neighborhood of each blob detected by the `SimpleBlobDetector`. Here, I examined the performance of the two methods by looking at the size error `se`. In the figure below, I overlay the raw, adaptive expansion and hough refining results on the image, and compare them with the ground truth. The result is that, although the adaptive expansion gets a few droplet detection nearly perfect, it makes many mistakes. As a result, it increases the mean size error when compared to the raw detection by `SimpleBlobDetector`. In contrast, the hough circle method is more effective in reducing the size error.

<img src="/assets/images/2025/01/refine-methods.png" width=700px>
