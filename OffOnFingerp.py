import numpy as np

class Cellule:
    """ Represents a fingerprint reference point with RSSI values """
    def __init__(self, position, rssi):
        self.position = position  # (x, y) coordinates
        self.rssi = rssi  # List of RSSI values

    def __repr__(self):
        return f"Cellule({self.position}, {self.rssi})"

def rssi_difference(rssi1, rssi2):
    """ Compute the absolute sum difference between two RSSI vectors """
    return sum(abs(rssi1[i] - rssi2[i]) for i in range(len(rssi1)))

def fingerprint_localization(grid, tm_rssi, k=4):
    """
    📍 RSSI-Based Online Phase: Perform Position Estimation
    """
    distances = []

    # Compute RSSI absolute differences with each reference cell
    for cell in grid:
        diff = rssi_difference(cell.rssi, tm_rssi)
        distances.append((diff, cell.position))

    # Sort by RSSI difference and select k-nearest neighbors
    distances.sort()
    k_nearest = distances[:k]

    # Compute inverse difference weights (Higher RSSI similarity = Higher weight)
    d1 = k_nearest[0][0]  # Smallest difference
    weights = [(1 / d) if d != 0 else 1 for d, _ in k_nearest]  # Avoid division by zero

    # Normalize weights
    weights = np.array(weights) / sum(weights)

    # Compute weighted estimated TM coordinates
    estimated_x = sum(w * coord[0] for w, (_, coord) in zip(weights, k_nearest))
    estimated_y = sum(w * coord[1] for w, (_, coord) in zip(weights, k_nearest))

    # Print results
    print(f"4 Nearest Cells (Based on RSSI Similarity): {[(coord[0], coord[1]) for _, coord in k_nearest]}")
    print(f"Estimated Position (RSSI Weighted): ({estimated_x:.2f}, {estimated_y:.2f})")

def main():
    """
    📡 Hardcoded Fingerprint Data (NO JSON FILE USED)
    """
    grid = [
        Cellule((0, 0), [-38, -27, -54, -13]),
        Cellule((4, 0), [-74, -62, -48, -33]),
        Cellule((8, 0), [-13, -28, -12, -40]),
        Cellule((0, 4), [-34, -27, -38, -41]),
        Cellule((4, 4), [-46, -48, -72, -35]),
        Cellule((8, 4), [-45, -37, -20, -15]),
        Cellule((0, 8), [-17, -50, -44, -33]),
        Cellule((4, 8), [-27, -28, -32, -45]),
        Cellule((8, 8), [-30, -20, -60, -40]),
    ]

    # Mobile Terminal (TM) RSSI
    tm_rssi = [-26, -42, -13, -46]  # Live RSSI from mobile device

    # Run localization algorithm
    fingerprint_localization(grid, tm_rssi, k=4)

if __name__ == "__main__":
    main()
