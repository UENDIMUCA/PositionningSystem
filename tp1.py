import numpy as np
from scipy.optimize import least_squares

# -----------------------------
# Position Class (3D Coordinates)
# -----------------------------
class Position:
    def __init__(self, x, y, z):
        """Represents a 3D position."""
        self.x = x
        self.y = y
        self.z = z

# -----------------------------
# Emitter Class (Represents Known Points)
# -----------------------------
class Emitter:
    def __init__(self, position):
        """Represents an emitter in 3D space."""
        self.position = position

# -----------------------------
# Receiver Class (Stores Distance Information)
# -----------------------------
class Receiver:
    def __init__(self, points, distances):
        """
        Represents the receiver and computes its estimated position.
        :param points: List of known emitter positions.
        :param distances: List of distances from emitters to receiver.
        """
        self.points = points
        self.distances = distances

    def estimate_position(self):
        """
        Calls the N-Lateration algorithm to compute the estimated position.
        :return: An instance of the Position class with estimated (x, y, z) coordinates.
        """
        n_lateration = NLateration(self.points, self.distances)
        estimated_pos = n_lateration.estimate_location()
        return estimated_pos  # FIXED: No unpacking needed

# -----------------------------
# N-Lateration Algorithm (Computes Position)
# -----------------------------
class NLateration:
    def __init__(self, points, distances):
        """
        Initializes N-Lateration with emitter positions and distances.
        :param points: List of emitter positions.
        :param distances: List of distances from receiver to emitters.
        """
        self.points = np.array(points)
        self.distances = np.array(distances)

    def estimate_location(self):
        """
        Uses least squares optimization to estimate the receiver's position.
        :return: Estimated (x, y, z) position as a Position object.
        """
        x0 = np.mean(self.points, axis=0)  # Use average emitter position as initial guess

        def fun(x):
            return np.linalg.norm(self.points - x, axis=1) - self.distances

        res = least_squares(fun, x0)
        return Position(*res.x)

# -----------------------------
# Factory Class (Creates Objects Dynamically)
# -----------------------------
class PositioningFactory:
    """Factory class for dynamically creating emitters and receivers."""
    
    @staticmethod
    def create_emitter(x, y, z):
        """Creates an Emitter object with a given position."""
        return Emitter(Position(x, y, z))

    @staticmethod
    def create_receiver(points, distances):
        """Creates a Receiver object with given emitter positions and distances."""
        return Receiver(points, distances)

# -----------------------------
# User Input Function (Allows User to Enter Custom Values)
# -----------------------------
def get_user_input():
    """
    Allows the user to input their own emitter positions and distances.
    If the user doesn't want to enter values, the default dataset is used.
    """
    use_default = input("Do you want to use the default dataset? (yes/no): ").strip().lower()

    if use_default == "yes":
        return {
            "emitters": [(0.5, 0.5, 0.5), (4, 0, 0), (4, 5, 5), (3, 3, 3)],
            "distances": [3, 2, 4.2, 2.5]
        }
    
    emitters = []
    distances = []

    print("\nEnter emitter positions (x, y, z) and their distances. Enter 'done' to finish.")

    while True:
        user_input = input("Enter emitter position (x y z distance) or 'done' to finish: ").strip()

        if user_input.lower() == "done":
            break
        
        try:
            values = list(map(float, user_input.split()))
            if len(values) != 4:
                print("Please enter exactly 4 numbers: x, y, z, and distance.")
                continue
            
            x, y, z, distance = values
            emitters.append((x, y, z))
            distances.append(distance)

        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")

    if len(emitters) < 4:
        print("\n⚠️ Not enough emitters provided! Using the default dataset instead.\n")
        return {
            "emitters": [(0.5, 0.5, 0.5), (4, 0, 0), (4, 5, 5), (3, 3, 3)],
            "distances": [3, 2, 4.2, 2.5]
        }

    return {"emitters": emitters, "distances": distances}

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    # Get user input or default dataset
    dataset = get_user_input()

    # Create emitters using the Factory
    emitters = [PositioningFactory.create_emitter(*coords) for coords in dataset["emitters"]]

    # Extract positions of emitters
    points = [(emitter.position.x, emitter.position.y, emitter.position.z) for emitter in emitters]

    # Create receiver using the Factory
    receiver = PositioningFactory.create_receiver(points, dataset["distances"])

    # Compute estimated position using N-Lateration
    estimated_position = receiver.estimate_position()

    # Print estimated position
    print(f"\n Estimated Position: ({estimated_position.x:.6f}, {estimated_position.y:.6f}, {estimated_position.z:.6f})")
