import numpy as np

class KalmanFilter3D:
    def __init__(self, dt=1.0):
        self.dim_x = 10  # State: [x, y, z, vx, vy, vz, l, w, h, yaw]
        self.dim_z = 7   # Measured: [x, y, z, l, w, h, yaw]

        # Initialize state and covariance
        self.x = np.zeros((self.dim_x, 1))
        self.P = np.eye(self.dim_x) * 10.

        # State transition matrix (motion model)
        self.F = np.eye(self.dim_x)
        for i in range(3):
            self.F[i, i+3] = dt  # position += velocity * dt

        # Measurement matrix (what we observe)
        self.H = np.zeros((self.dim_z, self.dim_x))
        self.H[0:3, 0:3] = np.eye(3)  # position
        self.H[3:6, 6:9] = np.eye(3)  # size
        self.H[6, 9] = 1.0            # yaw

        # Process noise (model uncertainty)
        self.Q = np.eye(self.dim_x)
        self.Q[0:3, 0:3] *= 0.1   # position noise
        self.Q[3:6, 3:6] *= 1.0   # velocity noise
        self.Q[6:9, 6:9] *= 0.01  # size noise
        self.Q[9, 9] *= 0.01      # yaw noise

        # Measurement noise (sensor noise)
        self.R = np.eye(self.dim_z) * 0.5

    def predict(self):
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q

    def update(self, z):
        z = z.reshape(-1, 1)
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R + np.eye(self.dim_z) * 1e-6  # Numerical stability
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.dim_x)
        self.P = (I - K @ self.H) @ self.P

    def get_state(self):
        s = self.x.flatten()
        return {
            'position': s[0:3],
            'velocity': s[3:6],
            'size': s[6:9],
            'yaw': s[9]
        }
