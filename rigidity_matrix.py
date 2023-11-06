import os
import numpy as np
import networkx as nx


def rigidity_matrix(G):

    '''Takes a Graph with 3D embedding (by node-atrribute pos) and
    draws a rigidity matrix. Checks for rigidity by comparing the matrix rank with the degrees of freedeom'''

    num_nodes = len(G.nodes)
    num_edges = len(G.edges)
    R = []

    for edge in G.edges():
        row = []
        for node in G.nodes():
            if node in edge: # if node is incident with e
                for i in (range(0, 2)):
                    row.append(G.nodes[node]['pos'][i] - G.nodes[edge[edge.index(node) - 1]]['pos'][i])
            else:
                row.append(0)
                row.append(0)
        R.append(row)

    R = np.array(R)
    rank = np.linalg.matrix_rank(R)

    print(R)
    print("Rank: ", rank)
    print(f'deg_free: {2 * num_nodes - 3}')
    # compares matrix rank with the degrees of freedom
    # if they are equal then the graph is rigid
    if rank == 2 * num_nodes - 3:
        print('The Graph is rigid')
        return True
    else:
        print('The Graph is flexible')
        return False
    print(R)

    return R


if __name__ == "__main__":

    G = nx.Graph()
    G.add_nodes_from([
        ('A', {"pos": (0, 0)}),
        ('B', {"pos": (1, 0)}),
        ('C', {"pos": (0.5, 0.866)})
    ])
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A')])
    print('Triangle')
    rigidity_matrix(G)
# square grid
    G = nx.Graph()
    G.add_nodes_from([
        ('A', {"pos": (0, 0)}),
        ('B', {"pos": (1, 0)}),
        ('C', {"pos": (1, 1)}),
        ('D', {"pos": (0, 1)})
    ])
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A')])

    print("Square grid:")
    rigidity_matrix(G)

# pentagon
    G = nx.Graph()
    G.add_nodes_from([
        ('A', {"pos": (0, 0)}),
        ('B', {"pos": (1, 0)}),
        ('C', {"pos": (1.5, 0.866)}),
        ('D', {"pos": (0.5, 1.866)}),
        ('E', {"pos": (-0.5, 0.866)})
    ])

    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')])

    print("Pentagon:")
    print(rigidity_matrix(G))

## well constraint pebble game

    G = nx.Graph()

    # Define the nodes and their 2D positions
    G.add_nodes_from([
        ("A", {"pos": (0, 0)}),
        ("B", {"pos": (1, 0)}),
        ("C", {"pos": (2, 0)}),
        ("D", {"pos": (3, 0)}),
        ("E", {"pos": (4, 0)}),
        ("F", {"pos": (5, 0)}),
        ("G", {"pos": (1, 1)}),
        ("H", {"pos": (2, 1)}),
        ("I", {"pos": (0.5, 0.866)})
    ])


    # Define the edge list
    edge_list = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"),
        ("A", "G"), ("B", "H"), ("C", "H"), ("D", "H"), ("E", "G"), ("F", "G"),
        ("G", "H"), ("A", "I"), ("B", "I")
    ]

    G.add_edges_from(edge_list)
    print("Pebble-game-well-constraint:")
    print(rigidity_matrix(G))

    #laman graph

    G = nx.Graph()

    # Define the nodes and their 2D positions
    G.add_nodes_from([
        ("A", {"pos": (1, 1)}),
        ("B", {"pos": (3, 1)}),
        ("C", {"pos": (4, 2)}),
        ("D", {"pos": (2.5, 3)}),
        ("E", {"pos": (1.5, 3)}),
        ("F", {"pos": (0, 2)}),
        ("G", {"pos": (1.5, 2)}),
        ("H", {"pos": (2.5, 2)})
         ])

    # Define the edge list
    edge_list = [
    ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"),
    ("A", "G"), ("B", "H"), ("C", "H"), ("D", "H"), ("E", "G"), ("F", "G"), ("G", "H")
    ]

    # Add edges to the graph
    G.add_edges_from(edge_list)
    print('Sample 7. Laman Graph:')
    print(rigidity_matrix(G))