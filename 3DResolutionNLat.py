import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Dataset: Known positions of access points (emitters) and their distances to the receiver
emitters = [
    {"pos": (0.5, 0.5, 0.5), "distance": 3.0},
    {"pos": (4.0, 0.0, 0.0), "distance": 2.0},
    {"pos": (4.0, 5.0, 5.0), "distance": 4.2},
    {"pos": (3.0, 3.0, 3.0), "distance": 2.5}
]

# Function to compute distance error
def distance_error(guess, emitters):
    x, y, z = guess
    return [np.sqrt((x - e["pos"][0])**2 + (y - e["pos"][1])**2 + (z - e["pos"][2])**2) - e["distance"] for e in emitters]

# Find the estimated receiver position by minimizing the error
initial_guess = (2, 2, 2)  # Initial assumption for receiver position
result = least_squares(distance_error, initial_guess, args=(emitters,))
estimated_x, estimated_y, estimated_z = result.x

# Create 3D plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot emitters and spheres
for emitter in emitters:
    x, y, z = emitter["pos"]
    distance = emitter["distance"]
    ax.scatter(x, y, z, color='blue', s=100, label="Access Points" if "Access Points" not in ax.get_legend_handles_labels()[1] else "")

    # Generate sphere surface
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    xs = x + distance * np.cos(u) * np.sin(v)
    ys = y + distance * np.sin(u) * np.sin(v)
    zs = z + distance * np.cos(v)
    
    ax.plot_wireframe(xs, ys, zs, color='b', alpha=0.2)

# Plot estimated receiver position
ax.scatter(estimated_x, estimated_y, estimated_z, color='red', marker="^", s=200, label="Estimated Position")

# Formatting
ax.set_xlabel("X Coordinate", fontsize=12)
ax.set_ylabel("Y Coordinate", fontsize=12)
ax.set_zlabel("Z Coordinate", fontsize=12)
ax.set_title("Graphical Resolution of N-Lateration Problem (3D)", fontsize=14)
ax.legend(fontsize=10)
ax.grid(True)

# Set axis limits dynamically
x_min = min(e["pos"][0] - e["distance"] for e in emitters) - 1
x_max = max(e["pos"][0] + e["distance"] for e in emitters) + 1
y_min = min(e["pos"][1] - e["distance"] for e in emitters) - 1
y_max = max(e["pos"][1] + e["distance"] for e in emitters) + 1
z_min = min(e["pos"][2] - e["distance"] for e in emitters) - 1
z_max = max(e["pos"][2] + e["distance"] for e in emitters) + 1

ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_zlim(z_min, z_max)

plt.show()
