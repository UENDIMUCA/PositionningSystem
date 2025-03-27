import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Needed for 3D plotting

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
        print("\n Not enough emitters provided! Using the default dataset instead.\n")
        return {
            "emitters": [(0.5, 0.5, 0.5), (4, 0, 0), (4, 5, 5), (3, 3, 3)],
            "distances": [3, 2, 4.2, 2.5]
        }

    return {"emitters": emitters, "distances": distances}

# -----------------------------
# Visualization Functions
# -----------------------------
def visualize(points, distances, estimated_position):
    """Displays both 2D and 3D visualizations."""
    # ----- 2D Visualization (XY Plane) -----
    fig2d, ax2d = plt.subplots()
    ax2d.set_title("2D Visualization (XY Plane)")
    ax2d.set_xlabel("X")
    ax2d.set_ylabel("Y")
    
    # Plot each AP and its range as a circle (only label the first for legend clarity)
    for idx, ((x, y, z), d) in enumerate(zip(points, distances)):
        circle = plt.Circle((x, y), d, fill=False, linestyle='--', edgecolor='b',
                            label="AP Range" if idx == 0 else None)
        ax2d.add_patch(circle)
        ax2d.plot(x, y, 'bo', label="AP" if idx == 0 else None)
    
    # Plot the estimated position
    ax2d.plot(estimated_position.x, estimated_position.y, 'r*', markersize=15, label="Estimated Position")
    ax2d.legend()
    ax2d.set_aspect('equal', 'box')
    ax2d.grid(True)

    # ----- 3D Visualization -----
    fig3d = plt.figure()
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.set_title("3D Visualization")
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Z")
    
    # Plot each AP and its sphere (wireframe) representing the distance
    for idx, ((x, y, z), d) in enumerate(zip(points, distances)):
        ax3d.scatter(x, y, z, c='b', marker='o', label="AP" if idx == 0 else None)
        
        # Create data for a sphere around the AP
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        xs = x + d * np.cos(u) * np.sin(v)
        ys = y + d * np.sin(u) * np.sin(v)
        zs = z + d * np.cos(v)
        ax3d.plot_wireframe(xs, ys, zs, color='b', alpha=0.2)
    
    # Plot the estimated position in 3D
    ax3d.scatter(estimated_position.x, estimated_position.y, estimated_position.z,
                 c='r', marker='*', s=100, label="Estimated Position")
    ax3d.legend()
    
    # Show both plots
    plt.show()

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    # Get user input or default dataset
    dataset = get_user_input()

    # Create emitters using the Factory
    emitters = [PositioningFactory.create_emitter(*coords) for coords in dataset["emitters"]]

    # Extract positions of emitters as tuples (x, y, z)
    points = [(emitter.position.x, emitter.position.y, emitter.position.z) for emitter in emitters]

    # Create receiver using the Factory
    receiver = PositioningFactory.create_receiver(points, dataset["distances"])

    # Compute estimated position using N-Lateration
    estimated_position = receiver.estimate_position()

    # Print estimated position
    print(f"\nEstimated Position: ({estimated_position.x:.6f}, {estimated_position.y:.6f}, {estimated_position.z:.6f})")

    # Visualize the results (both 2D and 3D)
    visualize(points, dataset["distances"], estimated_position)
