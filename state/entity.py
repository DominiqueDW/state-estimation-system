import numpy as np

class EntityState:
    
    def __init__(self, entity_id):
        self.entity_id = entity_id

        # entity position and velocity
        self.X = np.array([[0.0],  # x
                           [0.0],  # y
                           [0.0],  # vx
                           [0.0]]) # yx
        
        # uncertainty
        self.P = np.eye(4) * 500 # large initial uncertainty

        self.last_position = None

        # time since last seen
        self.time_since_seen = 0.0

    def predict(self, dt):

        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1,  0],
            [0, 0, 0,  1]
        ])

        self.X = F @ self.X # prediction model (transition steps) in matrix form
        
        # process noise
        Q = np.eye(4) * 0.1

        # new_uncertainity = propagated_old_uncertainty + process_noise
        # prediction step ALWAYS increase uncertainty
        self.P = F @ self.P @ F.T + Q

        self.time_since_seen += dt

    def update_from_observation(self, obs_position):
        # Kalman filter update step

        # observation - what the sensor saw
        z = np.array([
            [obs_position[0]],
            [obs_position[1]]
        ])

        # helps extract position from X for comparison with observation
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        # expected measurement/instrument noise - lower R = trust sensor more, higher R = trust sensor less
        R = np.eye(2) * 0.5

        # innovation (observation - prediction)
        y = z - (H @ self.X)

        # innovation covariance
        S = H @ self.P @ H.T + R

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # update state/estimation
        self.X = self.X + K @ y

        # update covariance/estimation uncertainty
        identity_matrix = np.eye(4)
        self.P = (identity_matrix - K @ H) @ self.P

        self.time_since_seen = 0.0

    def initialize_state(self, position, velocity):
        self.X[0, 0] = position[0]
        self.X[1, 0] = position[1]
        self.X[2, 0] = velocity[0]
        self.X[3, 0] = velocity[1]

    def mahalanobis_distance(self, obs_position):
        z = np.array([
            [obs_position[0]],
            [obs_position[1]]
        ])

        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        R = np.eye(2) * 0.5

        # innovation
        y = z - (H @ self.X)

        # innovation covariance
        S = H @ self.P @ H.T + R

        # Mahalanobis distance
        d2 = (y.T @ np.linalg.inv(S) @ y)

        return float(d2)
    
    # Accessor - Can access the 'hidden' object data but cannot alter the data
    # Mutator - Can access and alter the 'hidden' object data

    @property
    def position(self):
        return [self.X[0, 0], self.X[1, 0]]

    @property
    def velocity(self):
        return [self.X[2, 0], self.X[3, 0]]