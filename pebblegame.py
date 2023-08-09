import random

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

    # randomizer for iterating over arbitrary edges
    # without replacement
    original_edges = []
    for originalEdge in multigraph5G.edges:
        original_edges.append(originalEdge)
    initialLen = len(original_edges)
    for i in range(0,initialLen):
        randLen = len(original_edges)
        next_int = random.randint(0,randLen)
        currentEdge = original_edges[next_int]

        # Component Detection V2:
        if supportGraph.nodes[currentEdge[0]]["pebbles"] + supportGraph.nodes[currentEdge[1]]["pebbles"] >= l+1:
            supportGraph.add_edge(currentEdge[0], currentEdge[1])
            supportGraph.nodes[currentEdge[0]]["pebbles"] = supportGraph.nodes[currentEdge[0]]["pebbles"] - 1

        else:
            #compute reach:
            visited = []
            to_visit = []
            u_node = currentEdge[0]
            v_node = currentEdge[1]
            visited.append(u_node)
            to_visit.append(supportGraph.successors(u_node))
            if not v_node in to_visit:


            currentnode

            unitedReach = [nx.dfs_preorder_nodes()]

        original_edges.pop(currentEdge)



                # return {} -> edge is free
            # 2. else:
            #       compute reach(u) u reach (v) = reach (u,v)
            #       if any element of reach (u,v) has at least on free pebble, return -> {}
            #       else:
            #
            

                if supportGraph.nodes[originalEdge[0]]["pebbles"] + supportGraph.nodes[originalEdge[1]]["pebbles"] >= l + 1:
                    # add edge
                    supportGraph.add_edge(originalEdge[0], originalEdge[1])
                    # reduce pebbles
                    supportGraph.nodes[originalEdge[0]]["pebbles"] = supportGraph.nodes[originalEdge[0]]["pebbles"] - 1
                    supportGraph.nodes[originalEdge[1]]["pebbles"] = supportGraph.nodes[originalEdge[1]]["pebbles"] - 1


                else:
                    #DFS

                # create new component

                # add component