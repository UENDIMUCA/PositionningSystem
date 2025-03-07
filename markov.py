import random
import pickle
import networkx as nx
import matplotlib.pyplot as plt
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

    def draw_graph(self):
        """ Draws the Markov Model transition graph with loops in green and bidirectional edges in red/blue """

        G = nx.DiGraph()  # Directed Graph
        edge_labels = {}  # Stores transition percentages
        colors = {}  # Stores different colors for bidirectional edges

        for i in range(5):
            for j in range(5):
                moves, percentage = self.node_stats(i, j)
                if moves > 0:
                    G.add_edge(i, j, weight=percentage)
                    edge_labels[(i, j)] = f"{percentage:.1f}%"
                    # Assign different colors
                    if i == j:  # Loop edge (self-referencing)
                        colors[(i, j)] = "green"
                    elif (j, i) in edge_labels:  # Bidirectional edge
                        colors[(i, j)] = "blue"
                        colors[(j, i)] = "red"
                    else:
                        colors[(i, j)] = "black"  # Default color for single-direction edges

        pos = nx.spring_layout(G, seed=42)  # Positioning nodes

        plt.figure(figsize=(8, 6))

        # Draw the nodes
        nx.draw(G, pos, with_labels=True, node_color="skyblue",
                node_size=3000, font_size=12, font_weight="bold")

        # Draw edges with specific colors
        for (i, j), color in colors.items():
            if i == j:  # Self-loop (green)
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color="green",
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.3", width=2)
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): edge_labels[(i, j)]},
                                             font_size=10, font_color="green", label_pos=0.5)
            elif (j, i) in colors:
                # Draw bidirectional curved edges
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color=color,
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.2", width=2)
                nx.draw_networkx_edges(G, pos, edgelist=[(j, i)], edge_color=colors[(j, i)],
                                       arrowstyle='-|>', connectionstyle="arc3,rad=-0.2", width=2)
                # Label each arrow
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): edge_labels[(i, j)]},
                                             font_size=10, font_color=color, label_pos=0.3)
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(j, i): edge_labels[(j, i)]},
                                             font_size=10, font_color=colors[(j, i)], label_pos=0.7)
            else:
                # Normal single-direction edges
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color=color,
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0", width=2)
                nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): edge_labels[(i, j)]},
                                             font_size=10, font_color=color, label_pos=0.5)

        plt.title("Markov Model - Web Navigation Transition Graph")
        plt.show()

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


# INTERACTIVE / RANDOM
def interactive_mode(graph):
    """ Allows user to enter moves dynamically. 
        Enter numbers 0-4 to make a move.
        Enter 5 to generate the graph visualization.
        Enter -1 to exit.
    """
    print("Interactive Mode: Enter node numbers (0-4) to move.")
    print("Enter 5 to generate the graph visualization.")
    print("Enter -1 to exit.\n")
    while True:
        try:
            next_move = int(input("Enter next move: "))
            if next_move == -1:
                break  # Exit
            elif next_move == 5:
                # Generate the graph visualization without making a move
                graph.draw_graph()
            elif 0 <= next_move <= 4:
                if graph.move(next_move):
                    print(graph)  # Show updated transition matrix
                else:
                    print("Move failed. Try again.")
            else:
                print("Invalid move! Please enter a number between 0 and 5 (-1 to exit).")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def random_mode(graph, moves=10):
    """ Simulates random user navigation for testing """
    for _ in range(moves):
        next_move = random.randint(0, 4)  # Ensures move is always 0-4
        graph.move(next_move)

    print(graph)  # Show transition table
    graph.draw_graph()  # Draw graph after random moves


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
