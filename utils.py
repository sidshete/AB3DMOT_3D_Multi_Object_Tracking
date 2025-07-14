# utils.py

import numpy as np

def iou3d(box1, box2):
    """
    Compute approximate 3D IoU.
    For a simple version, use BEV IoU and height overlap.
    """
    bev_iou = iou_bev(box1, box2)

    z1_min = box1[2] - box1[5]/2
    z1_max = box1[2] + box1[5]/2

    z2_min = box2[2] - box2[5]/2
    z2_max = box2[2] + box2[5]/2

    z_overlap = max(0, min(z1_max, z2_max) - max(z1_min, z2_min))
    h1 = box1[5]
    h2 = box2[5]

    intersection = bev_iou * z_overlap
    union = h1 + h2 - z_overlap

    return intersection / union

def iou_bev(box1, box2):
    """
    Bird's eye view IoU: simple approximation
    """
    # Assuming aligned boxes for simplicity
    x1, y1, l1, w1 = box1[0], box1[1], box1[3], box1[4]
    x2, y2, l2, w2 = box2[0], box2[1], box2[3], box2[4]

    # Compute overlap in x and y
    x1_min, x1_max = x1 - l1/2, x1 + l1/2
    y1_min, y1_max = y1 - w1/2, y1 + w1/2
    x2_min, x2_max = x2 - l2/2, x2 + l2/2
    y2_min, y2_max = y2 - w2/2, y2 + w2/2

    x_overlap = max(0, min(x1_max, x2_max) - max(x1_min, x2_min))
    y_overlap = max(0, min(y1_max, y2_max) - max(y1_min, y2_min))

    intersection = x_overlap * y_overlap
    area1 = l1 * w1
    area2 = l2 * w2

    union = area1 + area2 - intersection

    return intersection / union if union > 0 else 0

