from matplotlib import pyplot as plt
from pdb_to_graph import *
from pebblegame import *
import scipy as sp

# list of edges
well_constrained_leestreinu = [(A, B), (A, C), (A, C), (A, D), (A, E), (A, E), (B, D), (B, D), (C, D), (C, D), (C, D),
                               (C, E), (C, F), (C, F), (C, F)]
under_constrained_leestreinu = [(A, B), (A, C), (A, C), (A, D), (A, E), (A, E), (B, D), (B, D), (C, D), (C, D), (C, D),
                                (C, E), (C, F), (C, F,)]


multigraph1G = nx.MultiGraph(under_constrained_lee_streinu)

# filename = "2eso.pdb"
# path = os.path.join(os.getcwd(),"pdb_samples", filename)
test = multigraph1G  # pdb_to_graph(path)
test5g = create5Ggraph(test)
# nx.draw(test, with_labels=True)
# plt.show()
supportgraph = initiate_supportGraph(test5g)
print(supportgraph.nodes)
print(supportgraph.nodes[0]["pebbles"])
supportgraph.nodes[0]["pebbles"] = supportgraph.nodes[0]["pebbles"] - 1
print(supportgraph.nodes[0]["pebbles"])
# toprint = test5g.edges
# for edge in toprint:
#     print(edge)


# print(multigraph.edges)


# g5 = create5Ggraph(multigraph)
# print("5G: ",g5.edges)
# mg5 = create5Ggraph(g)
# nx.draw(mg5, with_labels=True)
# plt.show()
