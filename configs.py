# configs.py

# MOT hyperparameters
MAX_AGE = 3         # How many frames to keep a track without matches
MIN_HITS = 3        # Minimum matches before track is valid
IOU_THRESHOLD = 0.1 # IoU threshold for association

# Kalman Filter
DT = 1.0            # Assume 1 frame = 1 time unit