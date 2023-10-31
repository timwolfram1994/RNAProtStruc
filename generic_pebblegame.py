import random
import networkx as nx
import test_samples


def create5Ggraph(multigraph1G):
    """based on molecular conjuncture, this function converts a (multigraph) into a 5G-Graph
     for pebble game application with a G^2 graph"""
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

    # create a sober edge list and the correct 5G Graph by only including the maximum 6 edges between two nodes
    edgelist5G = [x for x in listofedges if x[2] < 6]
    multigraph5G = nx.MultiGraph(edgelist5G)

    return multigraph5G


def generic_pebblegame(multiDiGraph: nx.MultiDiGraph, k, l):
    def dfs_find_pebble(digraph: nx.MultiDiGraph, u, v):
        """A function for a DFS, that stops immediately after a pebble is found on a node
        # to avoid unnessessary computational resources. It returns the boolean true,
        if a pebble has been found and the whole reach of u,v otherwise."""

        # Initiation of the lists for visited notes (visited) and the
        # backlog of nodes to visit (to_visit)
        visited = []
        visited.append((u, v))
        to_visit = [(u, iter(digraph.successors(u)))]
        # To do until the list of to-visit-nodes and all of its successors have been traversed
        while to_visit:
            parent, childen = to_visit[-1]
            try:
                child = next(childen)
                # pebble found
                child_already_visited = False
                for edge in visited:
                    if child in edge:
                        child_already_visited = True
                        break
                if not child_already_visited:
                    visited.append((parent, child))
                    if D.nodes[child]["pebbles"] != 0:
                        D.nodes[child]["pebbles"] -= 1
                        D.nodes[u]["pebbles"] += 1
                        # Reverse path, to walk the path in a more efficient way from its end to its start
                        visited.reverse()
                        visited.pop(
                            -1)  # Reverse node v, since it was only used for seggregation
                        for edge in visited:
                            if edge[1] == child:
                                D.remove_edge(edge[0], edge[1])
                                D.add_edge(edge[1], edge[0])
                                if edge[0] == u:
                                    return True
                                child = edge[0]
                    else:
                        to_visit.append((child, iter(digraph.successors(child))))
            except StopIteration:
                to_visit.pop(-1)
        return visited

    '''Definitions and initiations of datastructures, notated accordingly to "Pebble game algorithms and sparse graphs"
    by Audrey Lee and Ileana Streinu as appeared in Discrete Mathematics 308 (2008) 1425-1437)'''

    # initiate directed pebble graph D with k pebbles and zero edges
    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)
    total_pebbles = len(V) * k

    # iterate in an arbitrary order over all nodes from G
    edges_to_insert = list(G.edges)
    random.shuffle(edges_to_insert)

    while edges_to_insert:
        print("------------------------------------------------------------------------")
        print("REMAINING EDGES : ", len(edges_to_insert))
        print("INSERTED EDGES : ", len(D.edges))
        # wähle eine zufällige Kante aus Edges_to_insert aus, über den Index der Liste einzufügender Kanten
        e = edges_to_insert.pop(-1)

        # Define u,v out of the edge to be inserted
        u = e[0]
        v = e[1]
        print("edge to insert: ", u, v)

        '''though there might be cases for the generic pebblegame to tread special cases of loops 
        (i.e. edge(u,v)| u = v) we hereby decide to leave this control structure out, 
        since there is no application herefore on molecule graphs with a 5,6 pebble game.'''

#           Check if the edge is a loop (u == v): if so, continue with next edge
#           if k <= l and u == v:
#               continue

        # edge acceptance: gather information on amount of pebbles and apply the DFS for pebble search,
        # if the sufficient amount of pebbles is not callable yet

        peb_u = D.nodes[u]["pebbles"]
        peb_v = D.nodes[v]["pebbles"]

        # initiate pebble-collection
        while peb_u + peb_v < (l + 1):

            '''the variables dfs_u and dfs_v are initially set to True. If a dfs-pebble search fails
            or if there are already k pebbles on u or v, the referring variable will be set to False
            if both variables remain false (i.e. DFS failed or not allowed at the node) at the end of 
            the one round collecting pebbles for u and v, the collecting process ends.'''

            dfs_u = True
            if peb_u == k:
                dfs_u = False

            if dfs_u == True:
                dfs_u = dfs_find_pebble(D, u, v)
                if dfs_u == True:
                    peb_u = peb_u + 1
            if peb_u + peb_v >= (l + 1):
                break

            dfs_v = True
            if D.nodes[v]["pebbles"] == k:
                dfs_v = False
            if dfs_v == True:
                dfs_v = dfs_find_pebble(D, v, u)
                if dfs_v == True:
                    peb_v = peb_v + 1

            if dfs_u != True and dfs_v != True:
                break

        # Edge Insertion: Check whether enough pebbles could be collected and if so, insert the edge into D.
        if peb_u + peb_v >= l + 1:
            D.add_edge(e[0], e[1])
            D.nodes[u]["pebbles"] = D.nodes[u]["pebbles"] - 1
            peb_u = peb_u - 1
            total_pebbles -= 1

        continue

    if total_pebbles == l:
        if len(D.edges) == len(G.edges):
            print("well-constraint; l pebbles remain. no edge has been left out")
        else:
            print("over-constraint; l pebbles remain.", len(G.edges) - len(D.edges), "edges have been left out")
    elif total_pebbles > l:
        if len(D.edges) == len(G.edges):
            print("under-constraint; ", total_pebbles, "pebbles remain. no edge has been left out")
        else:
            print("other: ", total_pebbles, "pebbles remain,", len(G.edges) - len(D.edges), "edges have been left out")
    else:
        print("error! This is result is not supposed to appear...", total_pebbles, "pebbles remain")


if __name__ == "__main__":
    generic_pebblegame(test_samples.sample10_graph, 2, 3)

