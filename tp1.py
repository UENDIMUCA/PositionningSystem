import sys
from math import ceil, floor
import math
from numpy import arange

# -----------------------------
# A Simple Location Class
# -----------------------------
class Location:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = ygit
        self.z = z

    def distanceTo(self, other):
        """Calculate Euclidean distance to another Location."""
        return math.sqrt((self.x - other.x)**2 +
                         (self.y - other.y)**2 +
                         (self.z - other.z)**2)

    def toString(self):
        """Return a string representation of the location."""
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
    '''
    Returns a tuple containing:
      (Computed Location, Total distance error, first image row,
       x-dimension size (in steps), y-dimension size (in steps),
       imageArray, maxDist)

    :param data: Array of tuples containing (Location, distance) for known emitters.
    :param step: Increment of grid search (lower step => better precision but slower).
    :param xSize: The X dimension of the cuboid containing all the emitters (auto-computed if not specified).
    :param ySize: The Y dimension of the cuboid containing all the emitters (auto-computed if not specified).
    :param zSize: The Z dimension of the cuboid containing all the emitters (auto-computed if not specified).
    :param md: A threshold value for image coloring.
    :param dmax: Maximum distance used for color scaling.
    :return: A tuple as described above.
    '''
    minLoc = Location()
    minDist = 0.0
    maxDist = 0.0
    revStep = ceil(1 / step)
    
    # Initialize minDist and compute the extents (xSize, ySize, zSize)
    for k in data:
        # Use the distance from the origin as a baseline error estimate.
        minDist += abs(k[0].distanceTo(Location()) - k[1])
        xSize = k[0].x if k[0].x > xSize else xSize
        ySize = k[0].y if k[0].y > ySize else ySize
        zSize = k[0].z if k[0].z > zSize else zSize

    # Create an image array for visualization (each z-slice is a list of color tuples)
    imageArray = [[] for i in range(0, floor(zSize * revStep))]

    # Grid search over the cuboid defined by xSize, ySize, and zSize.
    for k in arange(0, xSize, step):
        print(".", end="")
        sys.stdout.flush()
        for l in arange(0, ySize, step):
            for m in arange(0, zSize, step):
                d = 0.0
                currentLoc = Location(k, l, m)
                # Sum the absolute error in distance from each emitter.
                for n in data:
                    d += abs(n[0].distanceTo(currentLoc) - n[1])
                # Update the minimum error and best location found.
                if d < minDist:
                    minDist = d
                    minLoc = Location(round(k, 2), round(l, 2), round(m, 2))
                if d > maxDist:
                    maxDist = d

                pd = d
                # Adjust d for image color scaling (non-linear transformation)
                d = (max(1 - d / dmax, 0)) ** (2 / 3)
                
                # Append a color tuple to the imageArray for the current m index.
                index = floor(m * revStep)
                if index >= len(imageArray):
                    index = len(imageArray) - 1  # Prevent out-of-range error

                if pd > md:
                    # Compute a color tuple based on the transformed distance value.
                    color = (260 - floor(360 - d * 360), 200, floor(200 + d * 50))
                    imageArray[index].append(color)
                else:  # Mark the computed location with a distinct color (e.g., white or purple)
                    imageArray[index].append((100, 0, 255))
    
    return (minLoc, minDist, imageArray[0], floor(xSize * revStep), floor(ySize * revStep), imageArray, maxDist)

# -----------------------------
# Main Function
# -----------------------------
def main():
    # Run the NLateration algorithm on the dataset with a specified step size.
    result = NLateration(dataset, step=1)
    print("\n\nN-Lateration:")
    print("Computed location : " + result[0].toString())
    print("With distance error = " + str(round(result[1], 2)) + " m")
    # You can also process the imageArray (result[5]) if you wish to visualize it.

if __name__ == '__main__':
    main()
