---
date: 2024-09-26
title: zoom in fungus edge
---

# Zoom in fungus edge

[Earlier](2024-09-10-condensation-flux.md), we did condensation expeirment with a large field of view (12 mm x 7 mm) and examined the condensation flux distribution in space. There are several issues with that experiment:

1. From the beginning of cooling, it took about 8 minutes for me to be able to resolve droplets in the images. Before that, the droplets are too small so that they appear as a white connected region. Ideally, we want to see the early stage of the condensation.
2. The fungal patch may not affect the condensation very far away from it self. In the earlier experiment, the field of view is 4 times of the patch diameter. Ideally, we want to zoom in a smaller regiond.

Due to these issues, we use a zoom lens with higher magnification (Navitar) to observe the condensation around the fungal patch. The field of view with the new setup is much smaller (0.5 mm x 0.3 mm). The figure below compares the condensation droplets observed at the same stage (2 minutes after cooling) using different magnifications. Obviously, higher magnification helps resolve the droplets at a much earlier stage. Next, we perform the condensation flux analysis, assuming hemisphere droplets as before. We also discuss the new problems that arised: (i) poor image quality and less circular droplets; (ii) absorption of water, wet fungal patch, count as droplet or not.

<img src="/assets/images/2024/09/fungus-different-magnifications.png" width=700px>  

## Condensation flux analysis

As before, we mostly hand labeled the size and locations of the condensation droplets. Two frames at 3.6 and 4.2 minutes are shown below as examples of droplet detection. A few observations can be made: (i) near the fungal patch, some droplets are absorbed into the fungal patch, forming a complex with a distinct look than other droplets (blue circles); (ii) coalescence of droplets happens at early stages of condensation. An example is circled in black; (iii) the image quality is noticeably poor, as some droplets can be barely seen. An example is circled in red.

<img src="/assets/images/2024/09/two-droplet-detection-frames.png" width=400px>

30 frames are picked out from a 20-minute video for analysis. We look at the temporal evolution of droplet number and average size. Then we compute the total volume and evaluate condensation flux. We finally plot the spatial distribution of condensation flux. The results are shown below. 

<img src="/assets/images/2024/09/number-and-mean-size.png" width=700px>  

<img src="/assets/images/2024/09/volume-and-flux-2.png" width=500px>  

<img src="/assets/images/2024/09/spatial-flux.png" width=400px>  

## New technical issues

1. Poor image quality: at high magnification, the images are more blurry in general. A big problem is the illumination near the fungal patch, because the patch can block the light from one side, making the droplets near the patch look like arcs. The arcs shorten as we approach the fungal patch. As a result, the detection of droplets right next to the fungal patch involves some guess. The different looks of droplets are shown below. 

<img src="/assets/images/2024/09/different-looks-of-droplets.png" width=700px>

2. Absorption of water into the fungal patch: a few instances can be seen in the image above. Whether to include them as droplets or not affects the condensation calculation. The size of them is also hard to define. 


