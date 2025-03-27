import random
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
        self._previous_node_id = None  # To store the last visited node

    def move(self, next_node_id):
        """ Moves from the current node to the specified next node """
        if 0 <= next_node_id < 5:  # Ensuring only pages 0-4
            self._nodes[self._current_node_id].add_move()
            self._edges[self._current_node_id][next_node_id] += 1
            self._previous_node_id = self._current_node_id  # Store current as previous before moving
            self._current_node_id = next_node_id
            return True
        return False  # Invalid move

    def node_stats(self, origin_id, destination_id):
        """ Calculates percentage of transitions from origin to destination """
        total_moves = self._nodes[origin_id].get_nb_moves()
        if total_moves == 0:
            return (0, 0.0)  # Avoid division by zero
        moves = self._edges[origin_id][destination_id]
        percentage = (moves * 100) / total_moves
        return (moves, percentage)

    def predict_next_move(self):
        """ Predicts the most probable next move based on past transitions (row-based analysis) """
        stats = [self.node_stats(self._current_node_id, j)[1] for j in range(5)]
        if all(s == 0 for s in stats):  # No transitions recorded
            return None  # No valid prediction
        return stats.index(max(stats))

    def predict_previous_move(self):
        """ Predicts the most probable previous move based on who linked to the current page (column-based analysis) """
        stats = []
        for i in range(5):
            total_moves_from_i = self._nodes[i].get_nb_moves()
            if total_moves_from_i == 0:
                stats.append(0)
            else:
                # Percentage of times 'i' linked to current page
                stats.append((self._edges[i][self._current_node_id] * 100) / total_moves_from_i)

        if all(s == 0 for s in stats):
            return None  # No valid prediction

        return stats.index(max(stats))

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
                    if i == j:  # Loop edge 
                        colors[(i, j)] = "green"
                    elif (j, i) in edge_labels:  # Bidirectional edge
                        colors[(i, j)] = "blue"
                        colors[(j, i)] = "red"
                    else:
                        colors[(i, j)] = "black"  # Default color for single-direction edges

        pos = nx.spring_layout(G, seed=42)  # Positioning nodes

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color="skyblue",
                node_size=3000, font_size=12, font_weight="bold")

        # Draw edges with specific colors
        for (i, j), color in colors.items():
            if i == j:  # Self-loop (green)
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color="green",
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.3", width=2)
            else:
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color=color,
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.2", width=2)
                nx.draw_networkx_edges(G, pos, edgelist=[(j, i)], edge_color=colors.get((j, i), color),
                                       arrowstyle='-|>', connectionstyle="arc3,rad=-0.2", width=2)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.title("Markov Model - Web Navigation Transition Graph")
        plt.show()

    def __str__(self):
        """ Returns a formatted table of transition counts with move counts and percentages, plus total visits """
        headers = ["From\\To"] + [f"Page {i}" for i in range(5)] + ["Total Visits"]
        table = []

        for i in range(5):
            row = [f"Page {i}"]
            for j in range(5):
                moves, percentage = self.node_stats(i, j)
                row.append(f"{moves} m, {percentage:.2f}%")
            row.append(f"{self._nodes[i].get_nb_moves()} visits")
            table.append(row)

        # Add total visits row at the end
        total_visits_row = ["Total Visits"]
        for j in range(5):
            total_visits_col = sum(self._edges[i][j] for i in range(5))
            total_visits_row.append(f"{total_visits_col} moves")
        total_visits_row.append(f"{sum(node.get_nb_moves() for node in self._nodes)} visits")

        table.append(total_visits_row)

        return tabulate(table, headers=headers, tablefmt="grid")


def interactive_mode(graph):
    """ Allows user to enter moves dynamically. """
    print("Interactive Mode: Enter node numbers (0-4) to move.")
    print("Enter 5 to generate the graph visualization.")
    print("Enter -1 to exit.\n")
    while True:
        try:
            next_move = int(input("Enter next move: "))
            if next_move == -1:
                break
            elif next_move == 5:
                graph.draw_graph()
            elif 0 <= next_move <= 4:
                graph.move(next_move)
                print(graph)
                print(f"Current Node: {graph._current_node_id}")
                print(f"Original Previous Node: {graph._previous_node_id if graph._previous_node_id is not None else 'None'}")
                next_prediction = graph.predict_next_move()
                prev_prediction = graph.predict_previous_move()
                print(f"Predicted Next Page: {next_prediction if next_prediction is not None else 'Unknown'}")
                print(f"Predicted Previous Page: {prev_prediction if prev_prediction is not None else 'Unknown'}\n")
            else:
                print("Invalid move! Please enter a number between 0 and 5 (-1 to exit).")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def random_mode(graph, moves=10):
    """ Simulates random user navigation for testing """
    for _ in range(moves):
        graph.move(random.randint(0, 4))
        print(graph)
        print(f"Current Node: {graph._current_node_id}")
        print(f"Original Previous Node: {graph._previous_node_id if graph._previous_node_id is not None else 'None'}")
        next_prediction = graph.predict_next_move()
        prev_prediction = graph.predict_previous_move()
        print(f"Predicted Next Page: {next_prediction if next_prediction is not None else 'Unknown'}")
        print(f"Predicted Previous Page: {prev_prediction if prev_prediction is not None else 'Unknown'}\n")


if __name__ == "__main__":
    graph = Graph(5)
    print("Select Testing Mode:\n1. Interactive Mode\n2. Random Mode")
    mode = input("Enter 1 or 2: ")
    if mode == "1":
        interactive_mode(graph)
    else:
        random_mode(graph, moves=10)