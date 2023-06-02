from create5Ggraph import *
from pdb_to_graph import *
import scipy as sp
# list of edges
l = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 1), (0, 2), (1, 3)]

multigraph1G = nx.MultiGraph(l)


filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)
test = pdb_to_graph(path)

nx.draw(test, with_labels=True)
plt.show()

# print(multigraph.edges)


# g5 = create5Ggraph(multigraph)
# print("5G: ",g5.edges)
# mg5 = create5Ggraph(g)
# nx.draw(mg5, with_labels=True)
# plt.show()
