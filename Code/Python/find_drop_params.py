"""
find_drop_params.py
===================

This script is used to find the best parameters for droplet detection using SimpleBlobDetector and Hough circle transform. It performs grid search over the parameter space to find the best combination of parameters that maximizes the F1-score.

Syntax
------
```
python find_drop_params.py
```

Edit
----
Oct 09, 2024: Initial commit.
"""

import cv2
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

def preprocess(image):
    """Preprocess the image for blob detection."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def detect_droplets(image, params):
    """Detect droplets using SimpleBlobDetector with given parameters."""
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(image)
    return keypoints

def refine_with_hough(image, keypoints, hough_params):
    """Refine the keypoints using the Hough circle transform with given parameters."""
    h, w = image.shape
    refined_keypoints = []
    for keypoint in keypoints:
        x, y = int(keypoint.pt[0]), int(keypoint.pt[1])
        r = int(keypoint.size / 2)
        x1, x2 = max(0, x-2*r), min(x+2*r, w)
        y1, y2 = max(0, y-2*r), min(y+2*r, h)
        roi = image[y1:y2, x1:x2]
        
        # Enhance contrast and edges
        roi = cv2.equalizeHist(roi)
        roi = cv2.GaussianBlur(roi, (5, 5), 0)
        
        circles = cv2.HoughCircles(roi, cv2.HOUGH_GRADIENT, **hough_params)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                cx, cy, radius = circle
                new_keypoint = cv2.KeyPoint(float(x1 + cx), float(y1 + cy), float(radius * 2))
                refined_keypoints.append(new_keypoint)
        else:
            refined_keypoints.append(keypoint)
    return refined_keypoints

def evaluate_detection(detected_keypoints, ground_truth):
    """Evaluate the detection performance using precision, recall, and F1-score."""
    detected_points = np.array([[kp.pt[0], kp.pt[1], kp.size/2] for kp in detected_keypoints])
    ground_truth_points = np.array(ground_truth)
    
    # Calculate distances between detected points and ground truth points
    distances = np.linalg.norm(detected_points[:, np.newaxis, :] - ground_truth_points[np.newaxis, :, :], axis=2)
    
    # Match detected points to ground truth points
    matches = distances.min(axis=1) < 10  # Consider a match if distance is less than 10 pixels
    
    precision = precision_score(np.ones(len(matches)), matches)
    recall = recall_score(np.ones(len(matches)), matches)
    f1 = f1_score(np.ones(len(matches)), matches)
    
    return precision, recall, f1

def grid_search(image, ground_truth, param_grid):
    """Perform grid search to find the best parameters."""
    best_params = None
    best_score = 0
    
    for blob_params in param_grid['blob']:
        for hough_params in param_grid['hough']:
            image = preprocess(image)
            keypoints = detect_droplets(image, blob_params)
            refined_keypoints = refine_with_hough(image, keypoints, hough_params)
            precision, recall, f1 = evaluate_detection(refined_keypoints, ground_truth)
            
            if f1 > best_score:
                best_score = f1
                best_params = (blob_params, hough_params)
    
    return best_params, best_score

# Example usage
image = cv2.imread(r'G:\My Drive\Research projects\F\Data\09172024\tracking\exp1\blob\0250.jpg')
data = pd.read_csv(r'G:\My Drive\Research projects\F\Data\09172024\tracking\exp1\blob\0250.csv')
ground_truth = [(i.x, i.y, i.r) for num, i in data.iterrows()]  

param_grid = {
    'blob': [
        cv2.SimpleBlobDetector_Params(),  # Add different sets of parameters here
        # Example: params1, params2, ...
    ],
    'hough': [
        {'dp': 1, 'minDist': 20, 'param1': 10, 'param2': 30, 'minRadius': 10, 'maxRadius': 50},
        {'dp': 1, 'minDist': 20, 'param1': 20, 'param2': 30, 'minRadius': 10, 'maxRadius': 50},
        {'dp': 1, 'minDist': 20, 'param1': 30, 'param2': 30, 'minRadius': 10, 'maxRadius': 50},
        {'dp': 1, 'minDist': 20, 'param1': 40, 'param2': 30, 'minRadius': 10, 'maxRadius': 50},
        {'dp': 1, 'minDist': 20, 'param1': 50, 'param2': 30, 'minRadius': 10, 'maxRadius': 50}
        # Add different sets of parameters here
        # Example: hough_params1, hough_params2, ...
    ]
}

best_params, best_score = grid_search(image, ground_truth, param_grid)
print(f"Best parameters: {best_params}")
print(f"Best F1-score: {best_score}")