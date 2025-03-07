import random
import pickle
from tabulate import tabulate

class Node:
    """ Represents a page (node) in the graph """
    def __init__(self, id_num):
        self._id = id_num
        self._total_nb_moves = 0  # Count of times this node was visited

    def get_id(self):
        return self._id

    def get_nb_moves(self):
        return self._total_nb_moves

    def add_move(self):
        """ Increments the count of moves made from this node """
        self._total_nb_moves += 1


class Graph:
    """ Represents a Markov Model-based transition graph for web navigation """
    def __init__(self, nb_nodes=5):
        self._nodes = [Node(i) for i in range(nb_nodes)]
        self._edges = [[0] * nb_nodes for _ in range(nb_nodes)]
        self._current_node_id = 0  # Start at page 0

    def move(self, next_node_id):
        """ Moves from the current node to the specified next node """
        if 0 <= next_node_id < 5:  # Ensuring only pages 0-4
            self._nodes[self._current_node_id].add_move()
            self._edges[self._current_node_id][next_node_id] += 1
            self._current_node_id = next_node_id
            return True
        return False  # Invalid move

    def node_stats(self, origin_id, destination_id):
        """ Calculates percentage of transitions from origin to destination """
        total_moves = self._nodes[origin_id].get_nb_moves()
        if total_moves == 0:
            return (0, 0.0)  # Avoid division by zero, return (moves, 0%)
        moves = self._edges[origin_id][destination_id]
        percentage = (moves * 100) / total_moves
        return (moves, percentage)

    def predict_next_move(self):
        """ Predicts the most probable next move based on past transitions """
        stats = [self.node_stats(self._current_node_id, j)[1] for j in range(5)]
        if all(s == 0 for s in stats):  # No transitions recorded
            return None  # No valid prediction
        return stats.index(max(stats))

    def save_graph(self, filename="graph_data.pkl"):
        """ Saves the graph transition data to a file """
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_graph(filename="graph_data.pkl"):
        """ Loads the graph transition data from a file """
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("No saved data found. Starting a new graph.")
            return None

    def __str__(self):
        """ Returns a formatted table of transition counts with move counts and percentages """
        headers = ["Node\\Remote"] + [f"Page {i}" for i in range(5)]
        table = []
        
        for i in range(5):
            row = [f"Page {i}"]
            for j in range(5):
                moves, percentage = self.node_stats(i, j)
                row.append(f"{moves} m, {percentage:.2f}%")
            table.append(row)

        formatted_table = tabulate(table, headers=headers, tablefmt="grid")

        return f"{formatted_table}\nCurrent node: {self._current_node_id}, Predicted next node: {self.predict_next_move()}"


# ------------------------------------------
# TESTING OPTIONS: INTERACTIVE / RANDOM
# ------------------------------------------
def interactive_mode(graph):
    """ Allows user to enter moves dynamically """
    print("Interactive Mode: Enter node numbers (0-4) to move. Enter -1 to exit.\n")
    while True:
        try:
            next_move = int(input("Enter next move: "))
            if next_move == -1:
                break  # Exit
            if graph.move(next_move):
                print(graph)  # Show updated transition matrix
            else:
                print("Invalid move! Please enter a number between 0 and 4.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def random_mode(graph, moves=10):
    """ Simulates random user navigation for testing """
    for _ in range(moves):
        next_move = random.randint(0, 4)  # Ensures move is always 0-4
        graph.move(next_move)
    print(graph)  # Show transition table


if __name__ == "__main__":
    print("Choose Mode:\n1. Load previous session\n2. Start a new session")
    choice = input("Enter 1 or 2: ")

    # Load previous data if available
    if choice == "1":
        graph = Graph.load_graph()
        if not graph:
            graph = Graph(5)  # Create a new graph if loading fails
    else:
        graph = Graph(5)  # Start a new graph

    print("\nSelect Testing Mode:\n1. Interactive Mode\n2. Random Mode")
    mode = input("Enter 1 or 2: ")

    if mode == "1":
        interactive_mode(graph)  # Manual Testing Mode
    else:
        random_mode(graph, moves=10)  # Automated Random Mode

    graph.save_graph()  # Save data for next session
