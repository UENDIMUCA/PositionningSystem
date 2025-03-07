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


class Graph:
    def __init__(self, nb_nodes):
        self._nodes = [Node(i) for i in range(nb_nodes)]
        self._edges = [[0] * nb_nodes for _ in range(nb_nodes)]
        self._current_node_id = 0

    def move(self, next_node_id):
        if 0 <= next_node_id < len(self._nodes):
            self._nodes[self._current_node_id].add_move()
            self._edges[self._current_node_id][next_node_id] += 1
            self._current_node_id = next_node_id

    def __str__(self):
        headers = [f"Page {i}" for i in range(len(self._nodes))]
        table = [[self._edges[i][j] for j in range(len(self._nodes))] for i in range(len(self._nodes))]
        return tabulate(table, headers=headers, showindex="always", tablefmt="grid")


# Test the optimized Graph
graph = Graph(5)
graph.move(1)
graph.move(2)
graph.move(3)
print(graph)
