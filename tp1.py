import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# -----------------------------
# A Simple Location Class
# -----------------------------
class Location:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def distanceTo(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

    def toString(self):
        return f"({self.x}, {self.y}, {self.z})"

# -----------------------------
# Data set: List of tuples (Location, distance)
# -----------------------------
dataset = [
    (Location(0.5, 0.5, 0.5), 3.0),
    (Location(4.0, 0.0, 0.0), 2.0),
    (Location(4.0, 5.0, 5.0), 4.2),
    (Location(3.0, 3.0, 3.0), 2.5)
]

# -----------------------------
# NLateration Function
# -----------------------------
def NLateration(data, step=0.1, xSize=0.0, ySize=0.0, zSize=0.0, md=0.0, dmax=10):
    minLoc = Location()
    minDist = float('inf')
    revStep = int(1 / step)
    xSize, ySize, zSize = max(k[0].x for k in data), max(k[0].y for k in data), max(k[0].z for k in data)

    for k in np.arange(0, xSize, step):
        for l in np.arange(0, ySize, step):
            for m in np.arange(0, zSize, step):
                d = 0.0
                currentLoc = Location(k, l, m)
                for n in data:
                    d += abs(n[0].distanceTo(currentLoc) - n[1])
                if d < minDist:
                    minDist = d
                    minLoc = currentLoc

    return minLoc, minDist

# -----------------------------
# Visualization Function
# -----------------------------
def visualize(data, computed_location):
    fig, ax = plt.subplots()
    # Draw circles for each data point
    for location, distance in data:
        circle = Circle((location.x, location.y), distance, fill=False, color='blue', linestyle='dotted')
        ax.add_patch(circle)
        ax.plot(location.x, location.y, 'bo')  # Mark the emitter location

    # Mark the computed location
    ax.plot(computed_location.x, computed_location.y, 'rx')  # 'rx' for red 'x'

    # Setting the limits on the plot
    ax.set_xlim(min(loc.x - dist for loc, dist in data), max(loc.x + dist for loc, dist in data))
    ax.set_ylim(min(loc.y - dist for loc, dist in data), max(loc.y + dist for loc, dist in data))
    ax.set_aspect('equal', adjustable='datalim')
    plt.grid(True)
    plt.show()

# -----------------------------
# Main Function
# -----------------------------
def main():
    computed_location, total_error = NLateration(dataset, step=0.5)
    print("Computed location: " + computed_location.toString())
    print("Total distance error: {:.2f} m".format(total_error))
    visualize(dataset, computed_location)

if __name__ == '__main__':
    main()