import simple_test_samples
import networkx as nx
import pandas as pd


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


def pebblegame(multiDiGraph: nx.MultiDiGraph, k, l):
    def dfs_gather_pebble(digraph: nx.MultiDiGraph, u, v):
        """A modified function for a DFS and path rearrangement, that stops immediately
        after a pebble is found on a node to avoid unnessessary computational resources.
        It returns the boolean true, if a pebble has been found and the whole reach of u,v otherwise."""

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

    def dfs_reach(digraph: nx.MultiDiGraph, u, v, stop_at_pebble=False):
        """A function for a DFS, with the option to stop after a pebble is found on a node
        It returns the boolean true, if it is supposed to stop after finding a pebble
        or the whole reach of u,v otherwise."""
        visited = set()
        visited.add(u), visited.add(v)
        to_visit = [(u, iter(digraph.successors(u)))]
        if not stop_at_pebble:
            while to_visit:
                parent, childen = to_visit[-1]
                try:
                    child = next(childen)
                    if child not in visited:
                        visited.add(child)
                        to_visit.append((child, iter(digraph.successors(child))))
                except StopIteration:
                    to_visit.pop(-1)
            return visited
        if stop_at_pebble:
            while to_visit:
                parent, childen = to_visit[-1]
                try:
                    child = next(childen)
                    if child not in visited:
                        visited.add(child)
                        if D.nodes[child]["pebbles"] != 0:
                            return True
                        else:
                            to_visit.append((child, iter(digraph.successors(child))))
                except StopIteration:
                    to_visit.pop(-1)
            return visited

    def dfs_reach_reverse(digraph: nx.MultiDiGraph, u, v):
        """A function for a DFS, which returns all predecessors of u,v."""
        visited = set()
        visited.add(u)
        for node in v:
            visited.add(node)
        to_visit = [(u, iter(digraph.predecessors(u)))]
        while to_visit:
            child, parents = to_visit[-1]
            try:
                parent = next(parents)
                if parent not in visited:
                    visited.add(parent)
                    to_visit.append((parent, iter(digraph.predecessors(parent))))
            except StopIteration:
                to_visit.pop(-1)
        return visited

    '''Definitions and initiations of datastructures, notated accordingly to "Pebble game algorithms and sparse graphs"
    by Audrey Lee and Ileana Streinu as appeared in Discrete Mathematics 308 (2008) 1425-1437)'''
    # Definitions
    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)
    total_pebbles = len(V) * k
    identified_components = []
    # initiate directed pebble graph D with k pebbles and zero edges

    # initiate n x n matrix of all vertices to present identified components
    component_matrix = pd.DataFrame(columns=V, index=V)
    component_matrix.fillna(0, inplace=True)

    # iterate in an arbitrary order over all nodes from G
    edges_to_insert = list(G.edges)

    '''(For demonstration purposes the list of edges to insert should be shuffled to achieve a real arbitrary order. 
    Nevertheless, to avoid additional overhead for the algorithm, the code is here fore is marked out.'''
    # random.shuffle(edges_to_insert)
    while edges_to_insert:
        # choose from an arbitrary edge of E(G) to be inserted.
        e = edges_to_insert.pop(-1)

        # define the nodes u and v from the to be inserted edge
        u = e[0]
        v = e[1]

        '''though there might be cases for the generic pebble game to tread special cases of loops 
        (i.e. edge(u,v)| u = v) we hereby decide to leave this control structure out, 
        since there is no application therefore on molecule graphs with a 5,6 pebble game.'''

        #           Check if the edge is a loop (u == v): if so, continue with next edge
        #           if k <= l and u == v:
        #               continue

        # check if (u,v) already are in any component (matrix cell -> true): if so, proceed with next edge
        index_u = V.index(u)
        index_v = V.index(v)
        if component_matrix.at[u, v] == 1:
            #print("Edge already in rigid component identified")
            continue

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
                dfs_u = dfs_gather_pebble(D, u, v)
                if dfs_u == True:
                    peb_u = peb_u + 1
            if peb_u + peb_v >= (l + 1):
                break

            dfs_v = True
            if D.nodes[v]["pebbles"] == k:
                dfs_v = False
            if dfs_v == True:
                dfs_v = dfs_gather_pebble(D, v, u)
                if dfs_v == True:
                    peb_v = peb_v + 1

            if dfs_u != True and dfs_v != True:
                break

        # Edge Insertion: Check whether enough pebbles could be collected and if so, insert the edge into D.
        edge_inserted = False
        if peb_u + peb_v >= l + 1:
            D.add_edge(e[0], e[1])
            D.nodes[u]["pebbles"] = D.nodes[u]["pebbles"] - 1
            peb_u = peb_u - 1
            total_pebbles -= 1
            edge_inserted = True

        if not edge_inserted:
            continue

        '''Component Detection V2:'''
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if peb_u + peb_v >= l + 1:
            continue
        # 2.) compute reach:
        else:
            '''2a) Search in reach of u or v for a pebble. If one is available, the search and the whole component
            detection are stopped. If the search is not successful, the search returns the reach(u,v) for part 2.b'''

            pebble_in_reach_u = dfs_reach(D, u, v, stop_at_pebble=True)
            if pebble_in_reach_u == True:
                continue
            pebble_in_reach_v = dfs_reach(D, v, u, stop_at_pebble=True)
            if pebble_in_reach_v == True:
                continue

            # The search was not successful, so the reach(u,v) for part 2.b is provided
            reach_uv = set(pebble_in_reach_u)
            reach_uv.update(pebble_in_reach_v)

            # 2.b) Reverse-DFS from nodes not in reach(u,v) in Supportgraph:

            # build a list of not reached nodes from u,v with at least one pebble
            not_reached = [node for node in D.nodes if node not in reach_uv and D.nodes[node]["pebbles"] != 0]

            # instead of adding nodes to the current_component-set, the set initially includes all nodes of V
            # and will be reduced by the nodes reached from w.
            current_component = set(D.nodes)
            dfs_w = {*reach_uv}

            '''To increase the pebble game's efficiency, we decided to not reverse all edges in the support graph D 
            and perform an ordinary DFS, but to use a customized DFS for predecessor nodes instead of successors.'''

            # perform a reversed-DFS for every not reached node:

            while not_reached:
                w = not_reached.pop()
                revered_reach_w = dfs_reach_reverse(D, w, dfs_w)
                dfs_w.update(revered_reach_w)
                # since there is a high probability of nodes from this list being other nodes predecessors,
                # the list not_reached is reduced by already traversed nodes after every DFS.
                for node in revered_reach_w:
                    if node in not_reached:
                        not_reached.remove(node)

            for reached_node_from_w in dfs_w:
                if reached_node_from_w in current_component:
                    current_component.remove(reached_node_from_w)

            current_component.update(reach_uv)

            # Update of the n x n matrix
            current_component = list(current_component)
            component_nodes_len = len(current_component)

            component_edges = set()
            '''to bypass unnecessary calls of D.nodes we use a pandas dataframe here 
            # and call the referring cells directly'''
            for i in range(0, component_nodes_len - 1):
                for j in range(i + 1, component_nodes_len):
                    node_i = current_component[i]
                    node_j = current_component[j]
                    component_matrix.at[node_i, node_j] = 1
                    component_matrix.at[node_j, node_i] = 1
                    component_edge = frozenset([node_i,node_j])
                    component_edges.add(component_edge)
            identified_components.append(set(component_edges))

    print("identified components: ", identified_components)

    print("Component-Matrix:\n", identified_components)
    if total_pebbles == l:
        if len(D.edges) == len(G.edges):
            print("well-constraint; l pebbles remain. no edge has been left out")
        else:
            print("over-constraint; l pebbles remain. ,", len(G.edges) - len(D.edges), "edges have been left out")
    elif total_pebbles > l:
        if len(D.edges) == len(G.edges):
            print("under-constraint; ", total_pebbles, "pebbles remain. no edge has been left out")
        else:
            print("other: ", total_pebbles, "pebbles remain,", len(G.edges) - len(D.edges), "edges have been left out")
    else:
        print("error!", total_pebbles, "pebbles remain")
    print("Matrix of rigid components: \n", component_matrix)

    return identified_components


if __name__ == "__main__":
    pebblegame(simple_test_samples.sample11_graph, 2, 3)
