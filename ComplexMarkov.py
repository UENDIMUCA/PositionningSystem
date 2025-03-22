
import random
import networkx as nx
import matplotlib.pyplot as plt
from tabulate import tabulate


class Node:
    """ Represents a room (node) in the graph """
    def __init__(self, id_num):
        self._id = id_num
        self._total_nb_moves = 0  # Count of times this room was visited

    def get_id(self):
        return self._id

    def get_nb_moves(self):
        return self._total_nb_moves

    def add_move(self):
        """ Increments the count of moves made from this room """
        self._total_nb_moves += 1


class Graph:
    """ Represents a Markov Model-based transition graph for house navigation """
    def __init__(self, nb_nodes=10):
        self._nodes = [Node(i) for i in range(nb_nodes)]
        self._edges = [[0] * nb_nodes for _ in range(nb_nodes)]
        self._current_node_id = 0  # Start at room 0
        self._previous_node_id = None  # To store the last visited room
        self._nb_nodes = nb_nodes

    def move(self, next_node_id):
        """ Moves from the current room to the specified next room """
        if 0 <= next_node_id < self._nb_nodes:
            self._nodes[self._current_node_id].add_move()
            self._edges[self._current_node_id][next_node_id] += 1
            self._previous_node_id = self._current_node_id
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
        """ Predicts the most probable next room (row-based analysis) """
        stats = [self.node_stats(self._current_node_id, j)[1] for j in range(self._nb_nodes)]
        if all(s == 0 for s in stats):
            return None
        return stats.index(max(stats))

    def predict_previous_move(self):
        """ Predicts the most probable previous room (column-based analysis) """
        stats = []
        for i in range(self._nb_nodes):
            total_moves_from_i = self._nodes[i].get_nb_moves()
            if total_moves_from_i == 0:
                stats.append(0)
            else:
                stats.append((self._edges[i][self._current_node_id] * 100) / total_moves_from_i)

        if all(s == 0 for s in stats):
            return None

        return stats.index(max(stats))

    def draw_graph(self):
        """ Draws the Markov Model transition graph for the house """
        G = nx.DiGraph()
        edge_labels = {}
        colors = {}

        for i in range(self._nb_nodes):
            for j in range(self._nb_nodes):
                moves, percentage = self.node_stats(i, j)
                if moves > 0:
                    G.add_edge(i, j, weight=percentage)
                    edge_labels[(i, j)] = f"{percentage:.1f}%"
                    if i == j:
                        colors[(i, j)] = "green"
                    elif (j, i) in edge_labels:
                        colors[(i, j)] = "blue"
                        colors[(j, i)] = "red"
                    else:
                        colors[(i, j)] = "black"

        pos = nx.spring_layout(G, seed=42)

        plt.figure(figsize=(12, 10))
        nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=3000, font_size=10, font_weight="bold")

        for (i, j), color in colors.items():
            if i == j:
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color="green",
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.3", width=2)
            else:
                nx.draw_networkx_edges(G, pos, edgelist=[(i, j)], edge_color=color,
                                       arrowstyle='-|>', connectionstyle="arc3,rad=0.2", width=2)
                nx.draw_networkx_edges(G, pos, edgelist=[(j, i)], edge_color=colors.get((j, i), color),
                                       arrowstyle='-|>', connectionstyle="arc3,rad=-0.2", width=2)

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
        plt.title("Markov Model - House Room Transition Graph")
        plt.show()

    def __str__(self):
        headers = ["From\\To"] + [f"Room {i}" for i in range(self._nb_nodes)] + ["Total Visits"]
        table = []

        for i in range(self._nb_nodes):
            row = [f"Room {i}"]
            for j in range(self._nb_nodes):
                moves, percentage = self.node_stats(i, j)
                row.append(f"{moves} m, {percentage:.2f}%")
            row.append(f"{self._nodes[i].get_nb_moves()} visits")
            table.append(row)

        total_visits_row = ["Total Visits"]
        for j in range(self._nb_nodes):
            total_visits_col = sum(self._edges[i][j] for i in range(self._nb_nodes))
            total_visits_row.append(f"{total_visits_col} moves")
        total_visits_row.append(f"{sum(node.get_nb_moves() for node in self._nodes)} visits")
        table.append(total_visits_row)

        return tabulate(table, headers=headers, tablefmt="grid")


def interactive_mode(graph):
    print("Interactive Mode: Enter room numbers (0-9) to move.")
    print("Enter 10 to generate the graph visualization.")
    print("Enter -1 to exit.\n")
    while True:
        try:
            next_move = int(input("Enter next move: "))
            if next_move == -1:
                break
            elif next_move == 10:
                graph.draw_graph()
            elif 0 <= next_move <= 9:
                graph.move(next_move)
                print(graph)
                print(f"Current Room: {graph._current_node_id}")
                print(f"Original Previous Room: {graph._previous_node_id if graph._previous_node_id is not None else 'None'}")
                next_prediction = graph.predict_next_move()
                prev_prediction = graph.predict_previous_move()
                print(f"Predicted Next Room: {next_prediction if next_prediction is not None else 'Unknown'}")
                print(f"Predicted Previous Room: {prev_prediction if prev_prediction is not None else 'Unknown'}\n")
            else:
                print("Invalid move! Please enter a number between 0 and 10 (-1 to exit).")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")


def random_mode(graph, moves=10):
    for _ in range(moves):
        graph.move(random.randint(0, 9))
        print(graph)
        print(f"Current Room: {graph._current_node_id}")
        print(f"Original Previous Room: {graph._previous_node_id if graph._previous_node_id is not None else 'None'}")
        next_prediction = graph.predict_next_move()
        prev_prediction = graph.predict_previous_move()
        print(f"Predicted Next Room: {next_prediction if next_prediction is not None else 'Unknown'}")
        print(f"Predicted Previous Room: {prev_prediction if prev_prediction is not None else 'Unknown'}\n")


if __name__ == "__main__":
    graph = Graph(10)  # House with 10 rooms
    print("Select Testing Mode:\n1. Interactive Mode\n2. Random Mode")
    mode = input("Enter 1 or 2: ")
    if mode == "1":
        interactive_mode(graph)
    else:
        random_mode(graph, moves=10)
