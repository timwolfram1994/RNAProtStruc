from create5Ggraph import *

# list of edges
l = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 1), (0, 2), (1, 3)]

multigraph1G = nx.MultiGraph()
for i in range(0,1):
    multigraph1G.add_edges_from(l)

print(multigraph1G.edges)

edges = multigraph1G.edges

g5 = create5Ggraph(multigraph1G)
print("5G: ",g5.edges)
# mg5 = create5Ggraph(g)
# nx.draw(mg5, with_labels=True)
# plt.show()
