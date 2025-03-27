import random
import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate


class Node:
    def __init__(self, id_num):
        self._id = id_num
        self._total_nb_moves = 0

    def get_id(self):
        return self._id

    def get_nb_moves(self):
        return self._total_nb_moves

    def add_move(self):
        self._total_nb_moves += 1


class ReferenceLocation:
    def __init__(self, location_id, coordinates, rssi_values):
        self.location_id = location_id
        self.coordinates = coordinates
        self.rssi_values = rssi_values

    def __str__(self):
        return f"Location {self.location_id} at {self.coordinates} with RSSI {self.rssi_values}"


class RSSIComparator:
    @staticmethod
    def rssi_difference(rssi1, rssi2):
        return sum(abs(rssi1[i] - rssi2[i]) for i in range(len(rssi1)))


class FingerprintLocalization:
    def __init__(self, grid, k=4):
        self.grid = grid
        self.k = k

    def find_k_nearest(self, tm_rssi):
        distances = [(RSSIComparator.rssi_difference(cell.rssi_values, tm_rssi), cell.coordinates) for cell in self.grid]
        distances.sort()
        return distances[:self.k]

    def compute_weights(self, k_nearest):
        weights = [(1 / d) if d != 0 else 1 for d, _ in k_nearest]
        weights = [w / sum(weights) for w in weights]
        return weights

    def estimate_position(self, k_nearest, weights):
        estimated_x = sum(w * coord[0] for w, (_, coord) in zip(weights, k_nearest))
        estimated_y = sum(w * coord[1] for w, (_, coord) in zip(weights, k_nearest))
        return estimated_x, estimated_y


class LocalizationSystem:
    def __init__(self):
        self.grid = self.initialize_grid()
        self.localizer = FingerprintLocalization(self.grid)

    def initialize_grid(self):
        nb_ap = int(input("Enter number of Access Points (APs): "))
        num_locations = int(input("Enter number of reference locations: "))
        grid = []
        for i in range(num_locations):
            print(f"\nReference Location {i}:")
            x = float(input("Enter x coordinate: "))
            y = float(input("Enter y coordinate: "))
            rssi_input = input(f"Enter RSSI values from {nb_ap} APs (comma-separated): ")
            rssi_values = [int(val.strip()) for val in rssi_input.split(",")]
            if len(rssi_values) != nb_ap:
                print("Incorrect number of RSSI values. Try again.")
                return self.initialize_grid()
            grid.append(ReferenceLocation(i, (x, y), rssi_values))
        return grid

    def run_localization(self):
        print("\n--- Live RSSI Input ---")
        tm_rssi_input = input(f"Enter RSSI values from APs (comma-separated): ")
        tm_rssi = [int(val.strip()) for val in tm_rssi_input.split(",")]
        k_nearest = self.localizer.find_k_nearest(tm_rssi)
        weights = self.localizer.compute_weights(k_nearest)
        estimated_x, estimated_y = self.localizer.estimate_position(k_nearest, weights)
        print(f"\nEstimated Position (RSSI Weighted): ({estimated_x:.2f}, {estimated_y:.2f})")


if __name__ == "__main__":
    system = LocalizationSystem()
    system.run_localization()
