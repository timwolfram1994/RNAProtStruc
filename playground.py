from matplotlib import pyplot as plt
from pdb_to_graph import *
from pebblegame import *
import scipy as sp
# list of edges
if __name__=="__main__":

l = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 0), (0, 2), (1, 3)]

multigraph1G = nx.MultiGraph(l)


# filename = "2eso.pdb"
# path = os.path.join(os.getcwd(),"pdb_samples", filename)
test = multigraph1G #pdb_to_graph(path)
test5g = create5Ggraph(test)
# nx.draw(test, with_labels=True)
# plt.show()
supportgraph = initiate_supportGraph(test5g)
print(supportgraph.nodes)
print(supportgraph.nodes[0]["pebbles"])
supportgraph.nodes[0]["pebbles"] = supportgraph.nodes[0]["pebbles"] -1
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


