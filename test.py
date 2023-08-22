import networkx as nx

G = nx.Graph()
G.add_nodes_from([1, 2, 3, 4])
G.add_edges_from([(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)])

nx.set_node_attributes(G, 5, "pebbles")

for u, node in G.nodes(data=True):
    print(node['pebbles'])

