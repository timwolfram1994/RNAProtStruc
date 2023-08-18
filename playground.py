from matplotlib import pyplot as plt
from pdb_to_graph import *
# from pebblegame import *
import scipy as sp
# list of edges
if __name__=="__main__":

# l = [(0, 1), (1, 2), (2, 3), (3, 0), (1, 0), (0, 2), (1, 3)]
    test_reach = [(0,1),(1,2),(3,1),(1,4),(4,5),(5,6),(6,4),(7,0),(7,8),(9,10),(10,7),(0,10),(0,11),(11,13),(12,11)]
    multiDigraph1G = nx.MultiDiGraph(test_reach)
    nx.draw(multiDigraph1G, with_labels=True)
    plt.show()

    # for nodes
    # visited = []
    # to_visit = []
    u_node = multiDigraph1G.nodes(0)
    print(u_node)
    # v_node = currentEdge[1]
    # visited.append(u_node)
    # to_visit.append(supportGraph.successors(u_node))
    # if v_node not in to_visit:
    #     to_visit.append(supportGraph.successors(v_node))
    #     visited.append(v_node)
    # while len(to_visit) != 0:
    #     currentNode = to_visit[-1]
    #     visited.append(to_visit[-1])
    #     to_visit.append(to)
    #

#
# # filename = "2eso.pdb"
# # path = os.path.join(os.getcwd(),"pdb_samples", filename)
# test = multigraph1G #pdb_to_graph(path)
# test5g = create5Ggraph(test)
# # nx.draw(test, with_labels=True)
# # plt.show()
# supportgraph = initiate_supportGraph(test5g)
# print(supportgraph.nodes)
# print(supportgraph.nodes[0]["pebbles"])
# supportgraph.nodes[0]["pebbles"] = supportgraph.nodes[0]["pebbles"] -1
# print(supportgraph.nodes[0]["pebbles"])
# # toprint = test5g.edges
# # for edge in toprint:
# #     print(edge)


# print(multigraph.edges)


# g5 = create5Ggraph(multigraph)
# print("5G: ",g5.edges)
# mg5 = create5Ggraph(g)
# nx.draw(mg5, with_labels=True)
# plt.show()



