class Cellule:
    """ Represents a fingerprint reference point with RSSI values """
    def __init__(self, position, rssi):
        self.position = position  # (x, y) coordinates
        self.rssi = rssi  # List of RSSI values

    def __repr__(self):
        return f"Cellule({self.position}, {self.rssi})"


class RSSIComparator:
    """ Computes RSSI differences """
    @staticmethod
    def rssi_difference(rssi1, rssi2):
        """ Compute the absolute sum difference between two RSSI vectors """
        return sum(abs(rssi1[i] - rssi2[i]) for i in range(len(rssi1)))


class FingerprintLocalization:
    """ Handles the localization process """
    def __init__(self, grid, k=4):
        self.grid = grid
        self.k = k
    
    def find_k_nearest(self, tm_rssi):
        """ Identifies the k-nearest neighbors based on RSSI similarity """
        distances = [(RSSIComparator.rssi_difference(cell.rssi, tm_rssi), cell.position) for cell in self.grid]
        distances.sort()
        return distances[:self.k]
    
    def compute_weights(self, k_nearest):
        """ Calculates weight for each neighbor """
        d1 = k_nearest[0][0]  # Smallest difference
        weights = [(1 / d) if d != 0 else 1 for d, _ in k_nearest]
        weights = [w / sum(weights) for w in weights]  # Normalize
        return weights
    
    def estimate_position(self, k_nearest, weights):
        """ Computes final estimated position """
        estimated_x = sum(w * coord[0] for w, (_, coord) in zip(weights, k_nearest))
        estimated_y = sum(w * coord[1] for w, (_, coord) in zip(weights, k_nearest))
        return estimated_x, estimated_y


class LocalizationSystem:
    """ Handles execution """
    def __init__(self):
        self.grid = self.initialize_grid()
        self.localizer = FingerprintLocalization(self.grid)

    def initialize_grid(self):
        """ Creates fingerprint reference points """
        return [
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

    def run_localization(self, tm_rssi):
        """ Runs the fingerprint localization algorithm """
        k_nearest = self.localizer.find_k_nearest(tm_rssi)
        weights = self.localizer.compute_weights(k_nearest)
        estimated_x, estimated_y = self.localizer.estimate_position(k_nearest, weights)
        print(f"Estimated Position (RSSI Weighted): ({estimated_x:.2f}, {estimated_y:.2f})")


if __name__ == "__main__":
    system = LocalizationSystem()
    tm_rssi = [-26, -42, -13, -46]  # Live RSSI from mobile device
    system.run_localization(tm_rssi)
