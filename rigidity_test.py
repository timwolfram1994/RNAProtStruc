import pebblegame_copy as pg
import networkx as nx
import pdb_to_graph as pdb
import os
import pickle
import matplotlib.pyplot as plt
import json

'''Protokoll: 
04.09. Component-Detection von Alex ergibt ebenfalls andere Komponenten nach jedem Durchlauf
To-Do: component detection debuggen, Testgraphen erstellen, PDB-to-graph debuggen

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

fh = open("graphs/eso.edgelist", "wb")
nx.write_edgelist(eso, fh)
eso = nx.read_edgelist("graphs/eso.edgelist")

print(nx.number_connected_components(eso))
print(eso)
#eso = pg.create5Ggraph(G)
print(eso)




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

nx.write_graphml_lxml(eso, "graphs/2eso.graphml")






