---
date: 2024-09-10
title: condensation flux around a fungal patch
---

# Condensation flux around a fungal patch

I use the hand labeling data from the summer students (Anushka and Cole's sister) to compute the condensation flux near a fungal patch. The calculation is based on the assumption that the condensation droplets are always hemi-spheres. Practically, this assumption ignores the ubiquitous phenomenon of "contact angle hysteresis", so this must be a very crude assumption. Here, we take this as the first step towards unrevealing the condensation flux. In the future, we will try to employ better models and measurements to obtain better condensation flux data. 

Before writing this note, I've already did [a short presentation](https://docs.google.com/presentation/d/1q85TJxatt8UFOiJjkSOckfiNcMwKs6shn9xjBCdU_nA/edit?usp=sharing) on this subject in the monthly meeting with the Northwestern group. This note summarizes the main message of the presentation and record the suggestions I got from the meeting.

The following picture is an example of the hand labeled droplets. Most of the droplets are correctly detected so the analysis here is trusted. 

<img src="/assets/images/2024/09/hand-labeling-example.jpg" width=700px>

I first measure the total number of droplets detected, as well as the mean radius of all droplets. The results are shown below. The total number of droplets decreases monotonically with time. This is expected because condensation always starts with many many tiny droplets. As the droplets grow in size, coalescence happens and leads to dramatic increase of droplet size. The mean radius of droplets increases before 20 min and decreases after 20 min. This is because at 20 min, we stop cooling the plate, effectively triggering the evaporation phase of the experiment. 

<img src="/assets/images/2024/09/total-number-and-mean-radius.png" width=700px>

I then measured the volume of droplets $V$ as

$$
V = \sum_{i=0}^{N-1} \frac{2}{3} \pi r_i^3, 
$$

and the flux $J$ as 

$$
J = \frac{1}{A} \frac{\partial V}{\partial t},
$$

where $A$ is the area on the surface. These measurements are done in different bands that are at different distance from the fungal patch. The distance is indicated using colors in the plot below. We observe total volume to increase then decrease in each band. The flux is positive in the condensation phase and is negative in the evaporation phase.

<img src="/assets/images/2024/09/volume-and-flux.png" width=700px> 

Finally, I plot the flux $J$ as a function of distance from the fungal patch $R$, in order to contrast with [the theory](https://pubs.acs.org/doi/10.1021/acs.langmuir.1c00473). The result, as well as the theoretical prediction, is shown in the figure below. The experimental flux is very noisy, and in general does not follow the predicted trend. 

<img src="/assets/images/2024/09/flux-vs-distance.png" width=700px>  

A few helpful feedbacks from the meeting:

1. the distance between condensation droplets may be related to the relative humidity in the chamber. Since spaced droplets are easier to detect, we want to take advantage of it while keep the essential physics. In future experiment, I will try different humidity level and optimize the image quality. 
2. The noise in the flux could be due to coalescence (very likely), as we noticed before. We need to figure out a method to detect coalescence events, and account for this "fake" boost of liquid volume. 
3. I notice that in some frames, the total volume of droplets decreases in the condensation phase. This is unphysical, but I don't know what gives rise to this in the data. It has to do with the crude assumption about droplet shape though.
