import numpy as np
from kalman_filter import KalmanFilter3D

class Track:
    """
    One track = one object with its own Kalman Filter.
    """
    count = 0

    def __init__(self, detection):
        """
        detection: [x, y, z, l, w, h, yaw]
        """
        self.kf = KalmanFilter3D()
        # Initialize state
        self.kf.x[0:3, 0] = detection[0:3]   # position
        self.kf.x[6:9, 0] = detection[3:6]   # size
        self.kf.x[9, 0]   = detection[6]     # yaw

        self.id = Track.count
        Track.count += 1

        self.age = 0
        self.hits = 1
        self.time_since_update = 0

    def predict(self):
        """
        Predict next state.
        """
        self.kf.predict()
        self.age += 1
        self.time_since_update += 1

    def update(self, detection):
        """
        Update with new detection.
        """
        z = np.array(detection[0:3].tolist() + detection[3:6].tolist() + [detection[6]])
        self.kf.update(z)
        self.hits += 1
        self.time_since_update = 0

    @property
    def bbox(self):
        """
        Get current bounding box: [x, y, z, l, w, h, yaw]
        """
        s = self.kf.get_state()
        return np.concatenate([s['position'], s['size'], [s['yaw']]])

    def is_dead(self, max_age):
        """
        Return True if the track has not been updated for too long.
        """
        return self.time_since_update > max_age

    def __repr__(self):
        s = self.kf.get_state()
        return f"[Track {self.id}] pos={s['position']} vel={s['velocity']} size={s['size']} yaw={s['yaw']:.2f}"
