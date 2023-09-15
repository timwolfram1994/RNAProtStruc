import pebblegame as pg
import networkx as nx
import pdb_to_graph as pdb
import os
import pickle
import matplotlib.pyplot as plt
import json
import pandas as pd
import numpy as np


'''Protokoll: 
To-Do: component detection 1 debuggen, Testgraphen erstellen, PDB-to-graph debuggen, 

'''


# Complete Graph (K5):
e_K5 = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
G = nx.from_edgelist(e_K5)

# laman Graph
e_Laman = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (2, 4), (2, 5)]
G = nx.from_edgelist(e_Laman)
#pg.pebblegame(G, 2, 3)

# complete octaeder

e_oct = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
G = nx.from_edgelist(e_oct)
G_5 = pg.create5Ggraph(G)
#pg.pebblegame(G_5,5,6)

# complete 100
'''G = nx.complete_graph(100)
print(G)
G = eso = pg.create5Ggraph(G)
print(G)'''

# PDB file
'''filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)
eso = pdb.pdb_to_graph(path)
'''

with open('graphs/outgraph.pickle', 'rb') as f:
    eso = pickle.load(f)


print(nx.number_connected_components(eso))
print(eso)
eso = pg.create5Ggraph(eso)
print(eso)
#pg.pebblegame(eso, 5, 6) # takes forever

fh = open("graphs/2mgo.edgelist", "rb")
oxy = nx.read_edgelist("graphs/2mgo.edgelist")
print(oxy)
oxy = pg.create5Ggraph(oxy)
print(oxy)
#comp_mat = pg.pebblegame(oxy, 5, 6)

fh = open('graphs/test_2octa.edgelist', 'rb')
G = nx.read_edgelist(fh)
G = pg.create5Ggraph(G)
comp_mat = pg.pebblegame(G, 5, 6)







'''pos = nx.spring_layout(eso)  # Layout algorithm
nx.draw(eso, pos, with_labels=True, node_color='skyblue', font_weight='bold')
plt.show()'''
#pg.pebblegame(eso,5,6)

# Convert the graph to Cytoscape.js JSON format
'''cytoscape_json = {
    'elements': {
        'nodes': [{'data': {'id': node}} for node in eso.nodes()],
        'edges': [{'data': {'source': source, 'target': target}} for source, target in eso.edges()]
    }
}

print(cytoscape_json)
'''
# Save the Cytoscape.js JSON to a file
'''with open('graphs/cytoscape_graph.json', 'w') as file:
    json.dump(cytoscape_json, file, indent=4)
'''

# creating five octahedrons connected

# Create a graph
G = nx.Graph()

# Define the vertices of the octahedron
vertices = [0, 1, 2, 3, 4, 5]

# Define the edges of the octahedron
edges = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 5), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]

# Create 5 octahedrons and connect them
for i in range(5):
    G.add_nodes_from([v + i * 6 for v in vertices])  # Shift vertices for each octahedron
    G.add_edges_from([(u + i * 6, v + i * 6) for u, v in edges])  # Shift edges for each octahedron

# Connect the centers of the octahedrons
center_nodes = [5, 11, 17, 23, 29]
G.add_edges_from([(center_nodes[i], center_nodes[(i + 1) % 5]) for i in range(5)])
G.remove_edge(5,29)
#G.remove_edge()


# Draw the graph
'''pos = nx.spring_layout(G, seed=42)  # Layout for visualization
nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", width=2)
plt.axis("off")
plt.show()'''

#perform component detection

'''G = pg.create5Ggraph(G)
comp_mat = pg.pebblegame(G, 5, 6)'''


data_matrix = comp_mat[1:, 1:]

# Check which columns have at least one element not equal to 0
non_zero_columns = np.any(data_matrix != 0, axis=0)

# Count the number of columns with at least one non-zero element
count_non_zero_columns = np.sum(non_zero_columns)

print("Number of nodes in rigid Components:", count_non_zero_columns)


#df = pd.DataFrame(comp_mat)
#df.to_csv('matrices/test_5octa.csv', index=False)






