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
                for i in (range(0, 3)):
                    row.append(G.nodes[node]['pos'][i] - G.nodes[edge[edge.index(node) - 1]]['pos'][i])
            else:
                row.append(0)
                row.append(0)
                row.append(0)
        R.append(row)

    R = np.array(R)
    rank = np.linalg.matrix_rank(R)

    print(R)
    print("Rank: ", rank)
    print(f'deg_free: {3 * num_nodes - num_edges}')
    # compares matrix rank with the degrees of freedom
    # if they are equal then the graph is rigid
    if rank == 3 * num_nodes - num_edges:
        print('The Graph is rigid')
        return True
    else:
        print('The Graph is flexible')
        return False
    print(R)

    return R


if __name__ == "__main__":



    # create tetrahedron

    G = nx.Graph()

    G.add_nodes_from([

        ('A', {"pos": (1, 1, 1)}),
        ('B', {"pos": (1, -1, -1)}),
        ('C', {"pos": (-1, 1, -1)}),
        ('D', {"pos": (-1, -1, 1)}),

    ])
    # Add nodes with specified positions


    # Define the edges of the tetrahedron
    edges = [('A', 'B'), ('A', 'C'), ('A', 'D'),
             ('B', 'C'), ('B', 'D'),
             ('C', 'D')]

    # Add edges to the graph
    G.add_edges_from(edges)

    #print(G.nodes['A']['pos'])
    #print(nx.get_node_attributes(G, "pos"))

    rigidity_matrix(G)

    ###OCTAHEDRON###

    G = nx.Graph()

    # Add nodes with specified positions
    G.add_nodes_from([
        ('A', {"pos": (0, 0, 1)}),
        ('B', {"pos": (0, 0, -1)}),
        ('C', {"pos": (1, 0, 0)}),
        ('D', {"pos": (-1, 0, 0)}),
        ('E', {"pos": (0, 1, 0)}),
        ('F', {"pos": (0, -1, 0)}),
    ])

    # Define the edges of the octahedron
    edges = [
        ('A', 'C'), ('A', 'D'), ('A', 'E'),
        ('B', 'C'), ('B', 'D'), ('B', 'E'),
        ('C', 'F'), ('D', 'F'), ('Aq', 'F'),
        ('C', 'E'), ('B', 'F'), ('C', 'D')
    ]

    # Add edges to the graph
    G.add_edges_from(edges)

    print('Test Octahedron:')
    print(G)
    rigidity_matrix(G)

