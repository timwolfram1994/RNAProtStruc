import networkx as nx


def create5Ggraph(multigraph1G):
    # create an edge list for the 5G Graph
    listofedges = []
    for edge in multigraph1G.edges:
        for i in range(0, 5):
            listofedges.append((edge[0], edge[1]))

    # append all edges from edge list to a new 5G Graph (not mattering about too many edges)
    # to achieve an edge list with (x,x,x) tuples
    multigraph5G = nx.MultiGraph(listofedges)
    listofedges.clear()
    for tuple in multigraph5G.edges:
        listofedges.append(tuple)

    # create a sober edge list and the correct 5G Graph
    edgelist5G = [x for x in listofedges if x[2] < 6]
    multigraph5G = nx.MultiGraph(edgelist5G)

    return multigraph5G


def initiate_supportGraph(multigraph5G):
    k = 5
    l = 6
    h = nx.MultiDiGraph()
    h.add_nodes_from(multigraph5G, pebbles=k)
    return h


def pebblegame(supportGraph, multigraph5G):
    k = 5
    l = 6
    original_edges = []
    for originalEdge in multigraph5G.edges:
        original_edges.append(originalEdge)

    # randomizer for iterating over arbitrary edges

    components = []  # list of lists
    activecomponent = 0
    for i in range(0, 6):
        for originalEdge in multigraph5G.edges:
            # component detection noch falsch! s. Paper!
            if (originalEdge[0], originalEdge[1]) not in components:

                if supportGraph.nodes[originalEdge[0]]["pebbles"] + supportGraph.nodes[originalEdge[1]][
                    "pebbles"] >= l + 1:
                    # add edge
                    supportGraph.add_edge(originalEdge[0], originalEdge[1])
                    # reduce pebbles
                    supportGraph.nodes[originalEdge[0]]["pebbles"] = supportGraph.nodes[originalEdge[0]]["pebbles"] - 1
                    supportGraph.nodes[originalEdge[1]]["pebbles"] = supportGraph.nodes[originalEdge[1]]["pebbles"] - 1


                else:
            # DFS

            # create new component

            # add component
                    return