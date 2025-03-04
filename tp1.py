import numpy as np
from scipy.optimize import least_squares

# -----------------------------
# N-Lateration Class (Computes Position)
# -----------------------------
class NLateration:
    def __init__(self, points, distances):
        """
        Initializes the N-Lateration class with known points (emitters) and their distances to the receiver.
        :param points: List of (x, y, z) coordinates of the emitters.
        :param distances: List of distances from the receiver to each emitter.
        """
        self.points = np.array(points)
        self.distances = np.array(distances)

    def estimate_location(self):
        """
        Uses the least squares method to estimate the position of the receiver.
        :return: The estimated (x, y, z) position.
        """
        # Initial guess for the receiver's position
        x0 = np.array([0, 0, 0])

        # Define the optimization function
        def fun(x):
            return np.linalg.norm(self.points - x, axis=1) - self.distances

        # Apply least squares optimization
        res = least_squares(fun, x0)

        # Return the estimated position
        return res.x

# -----------------------------
# Emitter Class (Represents Emitters in 3D Space)
# -----------------------------
class Emitter:
    def __init__(self, center):
        """
        Represents an emitter in 3D space.
        :param center: Tuple (x, y, z) representing the emitter's coordinates.
        """
        self.center = center

# -----------------------------
# Position Class (Represents Estimated Position)
# -----------------------------
class Position:
    def __init__(self, x, y, z):
        """
        Represents a position in 3D space.
        :param x: X coordinate.
        :param y: Y coordinate.
        :param z: Z coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

# -----------------------------
# Receiver Class (Estimates Position)
# -----------------------------
class Receiver:
    def __init__(self, distances):
        """
        Represents the receiver and computes its estimated position based on given distances.
        :param distances: List of distances to emitters.
        """
        self.distances = distances

    def estimate_position(self):
        """
        Calls the N-Lateration algorithm to compute the estimated position.
        :return: An instance of the Position class with estimated (x, y, z) coordinates.
        """
        n_lateration = NLateration(points, self.distances)
        estimated_pos = n_lateration.estimate_location()
        return Position(*estimated_pos)

# -----------------------------
# Given Problem Data
# -----------------------------
points = [(0.5, 0.5, 0.5), (4, 0, 0), (4, 5, 5), (3, 3, 3)]
distances = [3, 2, 4.2, 2.5]

# Create receiver object
receiver = Receiver(distances)

# Compute estimated position
position = receiver.estimate_position()

# Print estimated position
print(f"Estimated Position: ({position.x:.6f}, {position.y:.6f}, {position.z:.6f})")
