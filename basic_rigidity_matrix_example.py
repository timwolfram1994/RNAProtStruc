import os
import numpy as np
import networkx as nx
import pdb_to_graph

'''G = nx.MultiGraph()

# Add nodes
G.add_node(1, pos=(0, 0, 0))
G.add_node(2, pos=(1, 0, 0))
G.add_node(3, pos=(0, 1, 0))

# Add edges
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(2, 3)'''

filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)
G = pdb_to_graph.pdb_to_graph(path)

# Create an empty rigidity matrix R with the appropriate dimensions:
num_nodes = len(G.nodes)
num_edges = len(G.edges)
R = np.zeros((3 * num_edges, 3 * num_nodes))

# Iterate over each edge in the MultiGraph and populate the rigidity matrix:
edge_index = 0
for edge in G.edges:
    node1, node2 = edge[0], edge[1]

    # Get the coordinates of the nodes
    pos1 = np.array(G.nodes[node1]['pos'])
    pos2 = np.array(G.nodes[node2]['pos'])

    # Compute the direction vector and edge length
    direction = pos2 - pos1
    edge_length = np.linalg.norm(direction)

    # Normalize the direction vector
    direction = direction.astype(float) / edge_length

    # Compute the row indices for the rigidity matrix
    row_indices = slice(3 * edge_index, 3 * edge_index + 3)

    # Compute the column indices for the rigidity matrix
    col_indices = (slice(3 * node1, 3 * node1 + 3), slice(3 * node2, 3 * node2 + 3))

    # Populate the rigidity matrix
    R[row_indices, col_indices[0]] = -direction[:, np.newaxis]
    R[row_indices, col_indices[1]] = direction[:, np.newaxis]

    edge_index += 1

print(R)

rank_R = np.linalg.matrix_rank(R)

if rank_R == 3 * num_nodes - 1:
    print("The graph is rigid.")
else:
    print("The graph is flexible.")