"""
compare_detection.py
===================

This script is used to compare the droplet detection parameters. It runs the detection algorithm with different sets of parameters and compares the results with the ground truth data. The script calculates the ratio of true positives, false positives and size accuracy for each set of parameters. 

Syntax
------
```
python compare_detection.py
```

Edit
----
Oct 09, 2024: Initial commit.
Jan 20, 2025: Separate the detection and evaluation functions.
"""

import cv2
import numpy as np
import pandas as pd
from scipy.spatial import KDTree
from myimagelib.myImageLib import readdata
import os
import pdb

def count_overlapping_points_with_tolerance(list1, list2, tolerance):
    # Extract (x, y) coordinates from the lists
    points1 = [(x, y) for x, y, r in list1]
    points2 = [(x, y) for x, y, r in list2]

    # Create a KDTree for the second list of points
    tree = KDTree(points2)

    overlap_count = 0
    matched_points = set()

    for ind1, point in enumerate(points1):
        # Query the KDTree for points within the tolerance
        indices = tree.query_ball_point(point, tolerance)
        for ind2 in indices:
            if ind2 not in matched_points:
                overlap_count += 1
                matched_points.add((ind1, ind2))
                break  # Move to the next point in list1 once a match is found

    return overlap_count, matched_points

def evaluate_detection(ground_truth, detected, tol=5):
    """Evaluate the detection performance using precision, recall, and F1-score."""
    circle1 = [tuple([x[0],x[1],x[2]*2]) for x in ground_truth.to_records(index=False)]
    circle2 = [tuple([x[0],x[1],x[2]*2]) for x in detected.to_records(index=False)]
    
    oc, mp = count_overlapping_points_with_tolerance(circle1, circle2, tol)
    
    # true positive / ground truth
    tp = oc/len(circle1)

    # false positive / detected
    fp = (len(circle2)-oc)/len(circle2)

    # size accuracy: mean of the ratio of the size difference and the ground truth size
    r0 = ground_truth.loc[[ind1 for ind1, ind2 in mp]].r.values
    r = detected.loc[[ind2 for ind1, ind2 in mp]].r.values

    # pdb.set_trace()

    sa = np.mean(np.abs(r0-r)/r0)

    return tp, fp, sa

if __name__ == "__main__":

    folder = r"G:\My Drive\Research projects\F\Data\compare_params"
    min_detected = 100
    tol_list = range(1, 6)
    l = readdata(os.path.join(folder, "scan_params"), "csv")
    ground_truth = pd.read_csv(os.path.join(folder, "ground_truth.csv"))

    df_list = []
    for num, i in l.iterrows():
        detected = pd.read_csv(i.Dir)
        for tol in tol_list:
            if len(detected) > min_detected:
                tp, fp, sa = evaluate_detection(ground_truth, detected, tol=tol)
            else:
                tp, fp, sa = 0, 0, 1

            # process i.Name to extract the parameters
            minthres, maxthres, circ, conv, iner = map(float, i.Name.split("_")[1::2])
            # save the dataframe entry
            df = pd.DataFrame([[minthres, maxthres, circ, conv, iner, tol, tp, fp, sa]], columns=["minThreshold", "maxThreshold", "circularity", "convexity", "inertia", "tol", "TP", "FP", "SA"])
            df_list.append(df)
            print(f"TP: {tp:.2f}, FP: {fp:.2f}, SA: {sa:.2f}")

    data = pd.concat(df_list)
    data.to_csv(os.path.join(folder, "results.csv"), index=False)
