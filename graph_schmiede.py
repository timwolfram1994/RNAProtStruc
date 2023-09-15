import networkx as nx
import matplotlib.pyplot as plt


# create two octahedrons connected by a path of 5 nodes

# Create a graph
G = nx.Graph()

# Define the vertices of the octahedron
vertices = [0, 1, 2, 3, 4, 5]

# Define the edges of the octahedron
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]

# Create two octahedrons and connect them with a path
for i in range(2):
    G.add_nodes_from([v + i * 6 for v in vertices])  # Shift vertices for each octahedron
    G.add_edges_from([(u + i * 6, v + i * 6) for u, v in edges])  # Shift edges for each octahedron

# Connect the centers of the octahedrons with a path
center_nodes = [5, 11]
path_nodes = [12, 13, 14, 15, 16]
G.add_edges_from([(center_nodes[0], path_nodes[0]), (center_nodes[1], path_nodes[4])])
for i in range(4):
    G.add_edge(path_nodes[i], path_nodes[i + 1])

# Draw the graph (optional)
'''pos = nx.spring_layout(G, seed=42)  # Layout for visualization
nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", width=2)
plt.axis("off")
plt.show()'''

# create edgelist

fh = open("graphs/test_2octa.edgelist", "wb")
nx.write_edgelist(G, fh)

