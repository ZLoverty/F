---
date: 2025-01-07
title: evaporation droplet size evolution
---

# Evaporation droplet size evolution

The size of condensation droplets evolve over time. There are primarily two phases, where the time dependence of size are difference. Phase one is the early stage, where no coalescence happens. In this phase, the radius of a droplet scales with time as $R\sim t^{1/3}$. Phase two is the later stage, where coalescence happens. In this case, the radius of droplet scales with time as $R\sim t$ (Beysens 2023). 

Theoretically, this growth law can be derived under the assumption that the vapor flux towards the condensation surface is a constant. Constant flux implies that the total volume of water on the surface grows linearly with time, $V_T\sim t$. The relations between total volume $V_T$ and droplet size $R$ depends on whether coalescence happens or not. When considering the no-coalescence case, as illustrated below on the left, the droplet expands in three dimensions, so $V_T\sim R^3$. When considering the coalescence case, as illustrated below on the right, the surface coverage of the droplets $S_c$ is roughly a constant, so that the total volume of the water "film" only expands in the direction perpendicular to the surface, so $V_T\sim R$. 

<img src="/assets/images/2025/01/condensation-droplet-growth.png" width=700px>  

It would be nice if we can verify this scaling with our experimental data. However, when plotting the mean radius as a function of time, as shown below, the increasing part is pretty linear, suggesting that at the beginning of the data (around 8 min), where droplets are large enough to be detected, the system is already in the coalescence regime. Indeed, the image shows that the droplets on the surface are so dense that they are mostly in contact with neighboring droplets.

<img src="/assets/images/2025/01/size-evolution.png" width=700px> 

In the evaporation stage (after 20 min), the droplet size evolution should be free from coalescence effect, and therefore should follow the 1/3 scaling. The mean radius evolution shows a little bit asymmetry between condensation and evaporation, suggesting this possibility. To be more quantitative, I also look at a few specific droplets and see how their radii reduce. The results are shown below. I use $(120-t)$ as the horizontal axis variable to recover the $t^{1/3}$ scaling. In the evaporation stage, the decrease of droplet radius indeed follows the 1/3 power, verifying the constant flux hypothesis. 

<img src="/assets/images/2025/01/evaporation-droplet-size.png" width=500px> 
