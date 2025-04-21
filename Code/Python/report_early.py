"""
report_early.py
===============

This script processes droplet detection results to generate "report" graphs. It should be run after the droplet detection step. This script is specifically designed to work with the "early" data. 

Syntax
------
python report_early.py folder [-n nBins] [-o overlap]

Edit
----
* Apr 14, 2025: Initial commit.
* Apr 21, 2025: (i) Save the data in h5 format. (ii) Fix the flux calculation by dividng by the area of the band.
"""

import argparse
import os
from myimagelib import readdata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib
matplotlib.rcParams["font.family"] = "STIXGeneral"
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["xtick.direction"] = "in"
matplotlib.rcParams["ytick.direction"] = "in"
plt.rcParams['xtick.major.size'] = 2  # Length of major ticks
plt.rcParams['ytick.major.size'] = 2  # Length of major ticks
plt.rcParams['xtick.minor.size'] = 1  # Length of minor ticks
plt.rcParams['ytick.minor.size'] = 1  # Length of minor ticks

def read_info(folder):
    """Reads the experimental information from file info.txt"""
    info_path = os.path.join(folder, "info.txt")
    keywords = ["start_time", "interval", "mpp", "center", "image_dims"]

    if not os.path.exists(info_path):
        raise FileNotFoundError(f"info.txt not found in the specified folder: {folder}")
    
    with open(info_path, "r") as f:
        lines = f.readlines()
    
    # read the info
    info = {}
    for line in lines:
        if line.startswith("#"):
            continue
        try:
            kw, val = line.strip().split(":")
        except:
            continue
        if kw in keywords:
            info[kw] = val.strip()

    # parse the info
    for kw in info:
        if kw in ["center", "image_dims"]:
            info[kw] = [float(i) for i in info[kw].split(",")]
        else:
            info[kw] = float(info[kw])
    
    return info

def compute_number_and_size(folder, start_time, interval, mpp):
    """Computes the number and size of droplets from the detection results."""
    # Read the droplet detection results
    l = readdata(folder, "csv")

    t = []
    nDrops = []
    radii = []
    
    for num, i in l.iterrows():
        xyr = pd.read_csv(i.Dir)
        t.append((start_time + num * interval)/60)
        nDrops.append(len(xyr))
        radii.append(xyr.r.mean()*mpp)

    return t, nDrops, radii

def compute_volume_and_flux(folder, start_time, interval, mpp, center, image_dims, nBins=5, overlap=0.1):
    """Computes the volume and flux of droplets."""
    # Read the droplet detection results
    l = readdata(folder, "csv")
    x0, y0, R = center
    binsize = image_dims[0] / (nBins - (nBins-1)*overlap)
    bins = np.linspace(R, R+image_dims[0], nBins)

    distance_bin_data = {}
    for j in range(nBins):
        distance_bin_data[j] = []
    for _, i in l.iterrows():
        xyr = pd.read_csv(i.Dir)
        xyr["R"] = xyr.x - x0

        # Step 4. divide droplets into bins and compute the volume of drops in each bin
        for j in range(nBins):
            sub_xyr = xyr.loc[(xyr.R > bins[j]) & (xyr.R <= bins[j]+binsize)]
            volume_bin = 2/3 * np.pi * (sub_xyr.r**3).sum()
            
            distance_bin_data[j].append(volume_bin)
    
    # Step 5. construct volume table
    volume_pxf = pd.DataFrame(data=distance_bin_data)

    # Step 6. construct flux table, note that the calculation of area varies with image
    # area =  2 * np.pi * bins[:-1] * dr # annulus area
    area = image_dims[1] * binsize # rectangular area
    flux_pxf = volume_pxf.diff().div(volume_pxf.index.to_series().diff().values, axis=0).div(area, axis=1)

    # Step 7. convert units and plot the results
    # We use the following conversion factors for volume and flux
    # volume: px^3 -> x mpp^3 x 1e-9 -> mm^3
    # flux: px/s -> x mpp x 1e-3 x fps x 60 -> mm/min
    volume = volume_pxf * mpp**3 * 1e-9
    flux = flux_pxf * mpp * 1e-3 / interval * 60
    flux["t"] = flux.index * interval / 60 + start_time / 60
    volume["t"] = volume.index * interval / 60 + start_time / 60

    return volume, flux, bins, binsize

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Generate report graphs for early data.")
    parser.add_argument("folder", type=str, help="Path to the folder containing the droplet detection results.")
    parser.add_argument("-n", type=int, default=5, help="Number of bins for volume and flux calculation.")
    parser.add_argument("-o", type=float, default=0, help="fraction of overlap in binning.")
    args = parser.parse_args()

    folder = args.folder
    if not os.path.exists(folder):
        raise FileNotFoundError(f"The specified folder does not exist: {folder}")
    
    info = read_info(folder)
    x0, y0, R = info["center"]
    w, h = info["image_dims"]
    mpp = info["mpp"]
    # print(info)

    # compute the time, number and size of droplets
    t, N, S = compute_number_and_size(folder, info["start_time"], info["interval"], info["mpp"])
    # print(t, N, S)

    # compute volume and flux
    V, F, bins, binsize = compute_volume_and_flux(folder, info["start_time"], info["interval"], info["mpp"], info["center"], info["image_dims"], nBins=args.n, overlap=args.o)

    # compute flux as a function of distance
    binarea = h * binsize * mpp**2 * 1e-6
    p_list = []
    for i in range(V.drop(columns="t").shape[1]):
        x, y =V.t[:], V.iloc[:, i] / binarea
        p = np.polyfit(x, y, 1)
        p_list.append(p[0])

    # Save N, radii, volume and flux data to an h5 file
    save_path = os.path.join(folder, "nrvf.h5")
    with pd.HDFStore(save_path, mode="w") as store:
        store["center"] = pd.Series([x0, y0, R], index=["x", "y", "R"])
        store["bins"] = pd.Series(bins, index=np.arange(len(bins)))
        store["binsize"] = pd.Series(binsize, index=[0])
        store["N"] = pd.DataFrame({"t": t, "N": N})
        store["R"] = pd.DataFrame({"t": t, "R": S})
        store["V"] = V
        store["F"] = F
        store["Fx"] = pd.DataFrame({"x": bins, "F": p_list})

    # Make plots
    fig = plt.figure(figsize=(7, 7))

    ax1 = fig.add_subplot(321)
    ax1.plot(t, N, ls="--", marker="o")
    ax1.set_xlabel("Time (min)")
    ax1.set_ylabel("Number of drops")

    ax2 = fig.add_subplot(323)
    ax2.plot(t, S, ls="--", marker="o")
    ax2.set_xlabel("Time (min)")
    ax2.set_ylabel("Mean radius (um)")
    cmap = plt.get_cmap("winter")

    ax3 = fig.add_subplot(322)
    ax4 = fig.add_subplot(324)
    # pdb.set_trace()
    for kw in V.drop(columns="t"):
        ax3.plot(V["t"], V[kw], color=cmap(kw/(args.n-1)))
        ax4.plot(F["t"], F[kw], color=cmap(kw/(args.n-1)))
    ax3.set_xlabel("Time (min)")
    ax3.set_ylabel("Volume (mm$^3$)")
    ax4.set_xlabel("Time (min)")
    ax4.set_ylabel("Flux (mm/min)")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(bins[0]/R, bins[-1]/R))
    cbar = plt.colorbar(sm, ax=ax3, label="Distance, $R/r_0$")
    cbar = plt.colorbar(sm, ax=ax4, label="Distance, $R/r_0$")

    ax5 = fig.add_subplot(325)
    ax5.plot(bins/R, p_list, marker="o")
    ax5.set_xlabel("Distance $x/R$")
    ax5.set_ylabel("Flux (mm/min)")

    plt.tight_layout()
    
    fig.savefig(os.path.join(folder, "report_early.pdf"))
