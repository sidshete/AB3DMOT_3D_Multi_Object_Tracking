# association.py

import numpy as np
from scipy.optimize import linear_sum_assignment
from utils import iou3d

def associate_tracks(tracks, detections, iou_thresh):
    if len(tracks) == 0 or len(detections) == 0:
        return [], list(range(len(tracks))), list(range(len(detections)))

    cost_matrix = np.zeros((len(tracks), len(detections)))
    for i, track in enumerate(tracks):
        for j, det in enumerate(detections):
            cost_matrix[i, j] = 1 - iou3d(track.bbox, det)

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    matches, unmatched_tracks, unmatched_dets = [], [], []
    for r, c in zip(row_ind, col_ind):
        if cost_matrix[r, c] > (1 - iou_thresh):
            unmatched_tracks.append(r)
            unmatched_dets.append(c)
        else:
            matches.append((r, c))

    unmatched_tracks += list(set(range(len(tracks))) - set(row_ind))
    unmatched_dets += list(set(range(len(detections))) - set(col_ind))

    return matches, unmatched_tracks, unmatched_dets
