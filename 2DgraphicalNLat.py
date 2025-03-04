import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

# Dataset: Known positions of access points (emitters) and their distances to the receiver
emitters = [
    {"pos": (0.5, 0.5), "distance": 3.0},
    {"pos": (4.0, 0.0), "distance": 2.0},
    {"pos": (4.0, 5.0), "distance": 4.2},
    {"pos": (3.0, 3.0), "distance": 2.5}
]

# Function to compute distance error
def distance_error(guess, emitters):
    x, y = guess
    return [np.sqrt((x - e["pos"][0])**2 + (y - e["pos"][1])**2) - e["distance"] for e in emitters]

# Find the estimated receiver position by minimizing the error
initial_guess = (2, 2)  # Initial assumption for receiver position
result = least_squares(distance_error, initial_guess, args=(emitters,))
estimated_x, estimated_y = result.x

# Plot the emitters and their circles
fig, ax = plt.subplots(figsize=(8, 8))
for emitter in emitters:
    x, y = emitter["pos"]
    distance = emitter["distance"]
    circle = plt.Circle((x, y), distance, color='b', fill=False, linestyle="dotted")
    ax.add_patch(circle)
    ax.scatter(x, y, color='blue', label="Access Points" if "Access Points" not in ax.get_legend_handles_labels()[1] else "")

# Plot the estimated receiver position
ax.scatter(estimated_x, estimated_y, color='red', marker="^", label="Estimated Position")

# Formatting the plot
ax.set_xlim(-2, 8)
ax.set_ylim(-2, 8)
ax.set_xlabel("X Coordinate")
ax.set_ylabel("Y Coordinate")
ax.set_title("Graphical Resolution of N-Lateration Problem (2D)")
ax.legend()
ax.grid(True)
plt.show()
