import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


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


def pebblegame(multiDiGraph: nx.MultiDiGraph, k, l):
    def dfs_reach_reverse(digraph: nx.MultiDiGraph, u, v):
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
        visited.remove(u)
        return visited

    def dfs_reach(digraph: nx.MultiDiGraph, u, v):
        visited = set()
        visited.add(u), visited.add(v)
        to_visit = [(u, iter(digraph.successors(u)))]
        while to_visit:
            parent, childen = to_visit[-1]
            try:
                child = next(childen)
                if child not in visited:
                    visited.add(child)
                    to_visit.append((child, iter(digraph.successors(child))))
            except StopIteration:
                to_visit.pop(-1)
        visited.remove(u), visited.remove(v)
        return visited

    def dfs_find_pebble(digraph: nx.MultiDiGraph, u, v):
        visited = []
        visited.append((u, v))
        to_visit = [(u, iter(digraph.successors(u)))]
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
                        # Pfade umdrehen, damit der Pfad von hinten nach vorn effizienter durchgegangen wird
                        visited.reverse()
                        visited.pop(
                            -1)  # entferne den knoten v, da dieser nicht zum Pfad gehört, sondern nur zur Abgrenzung des Reaches diente
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
        return False

    # Definitions
    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)
    total_pebbles = len(V) * k
    # initiate directed pebble graph D with k pebbles and zero edges

    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    len_g_nodes = len(G.nodes)
    components = np.zeros((len_g_nodes, len_g_nodes))

    # components = np.zeros((len_g_nodes + 1, len_g_nodes + 1))
    # i = iter(range(1, len_g_nodes+1))
    # for node in D.nodes:
    #     index = next(i)
    #     components[0][index] = node
    #     components[index][0] = node




    # iterate in an arbitrary order over all nodes from G
    edges_to_insert = list(G.edges)
    random.shuffle(edges_to_insert)
    while edges_to_insert:
        print("------------------------------------------------------------------------")
        print("REMAINING EDGES : ", len(edges_to_insert))
        print("INSERTED EDGES : ", len(D.edges))
        # wähle eine zufällige Kante aus Edges_to_insert aus, über den Index der Liste einzufügender Kanten
        e = edges_to_insert.pop(-1)

        # definiere die Knoten u und v aus der einzusetzenden Kante
        u = e[0]
        v = e[1]
        print("edge to insert: ", u, v)

        # Prüfung ob u = v, falls ja, nächste Kante
        if u == v:
            continue

        # prüfung ob (u,v) in irgendeiner Komponente (matrix zelle true): falls ja, nächste Kante
        index_u = V.index(u)
        index_v = V.index(v)
        if components[index_u+0][index_v+0] == 1:
            print("Edge already in rigid component identified")
            continue

        # Tiefensuche für u (eingeschlossen v)
        while D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] < (l + 1):
            dfs_u = True
            if D.nodes[u]["pebbles"] == k:
                dfs_u = False

            if dfs_u:
                dfs_u = dfs_find_pebble(D, u, v)
                # redirect pebble-path
            if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= (l + 1):
                break
            dfs_v = True
            if D.nodes[v]["pebbles"] == k:
                dfs_v = False
            if dfs_v:
                dfs_v = dfs_find_pebble(D, v, u)

            if not dfs_u and not dfs_v:
                break

        # (nach Tiefensuche) einfügen der neuen Kante (u,v)
        edge_inserted = False
        if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= l + 1:
            D.add_edge(e[0], e[1])
            D.nodes[u]["pebbles"] = D.nodes[u]["pebbles"] - 1
            total_pebbles -= 1
            edge_inserted = True

        if not edge_inserted:
            continue

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= l + 1:
            continue
        # 2.) compute reach:
        else:
            reach_uv = dfs_reach(D, u, v)
            reach_uv.update(dfs_reach(D, v, u))

            # 2.a) check for any free pebble within all elements of reach(u,v)
            '''hier kann man auch die pebble suche funktion anwenden, damit nicht der gesamte reach berechnet wird!'''
            pebble_found = False
            for node in reach_uv:
                if D.nodes[node]["pebbles"] != 0:
                    pebble_found = True
                    break
            if pebble_found:
                continue

            # 2.b) DFS from nodes not in reach(u,v) in Supportgraph with all edges reversed:
            '''alle knoten von 2a reach_uv haben folglich 0 pebbles und gehören zur Komponente!, auch wenn im reach von w'''
            not_reached = [node for node in D.nodes if node not in reach_uv and D.nodes[node]["pebbles"] != 0]
            print("Reach(u,v) :", reach_uv)

            identified_component = set(D.nodes)
            dfs_w = set()

            while not_reached:
                w = not_reached.pop()
                dfs_w.update(dfs_reach_reverse(D, w, dfs_w))
                for node in dfs_w:
                    if node in not_reached:
                        not_reached.remove(node)

            for reached_node_from_w in dfs_w:
                if reached_node_from_w in identified_component:
                    identified_component.remove(reached_node_from_w)

            for reached_node_from_uv in reach_uv:
                identified_component.add(reached_node_from_uv)

            # Update der n x n matrix
            identified_component = list(identified_component)
            matrix_len = len(identified_component)
            for i in range(0, matrix_len - 1):
                for j in range(i + 1, matrix_len):
                    index_i = list(D.nodes).index(identified_component[i])
                    index_j = list(D.nodes).index(identified_component[j])
                    components[index_j][index_i] = 1
                    components[index_i][index_j] = 1
    print("------------------------------------------------------------------------")
    if total_pebbles == l:
        if len(D.edges) == len(G.edges):
            print("well-constraint; l pebbles remain. no edge has been left out")
        else:
            print("over-constraint; l pebbles remain. ,", len(G.edges) - len(D.edges), "have been left out")
    elif total_pebbles > l:
        if len(D.edges) == len(G.edges):
            print("under-constraint; ", total_pebbles, "pebbles remain. no edge has been left out")
        else:
            print("other: ", total_pebbles, "pebbles remain,", len(G.edges) - len(D.edges), "edges have been left out")
    else:
        print("error!", total_pebbles, "pebbles remain")
    print("Matrix steifer Komponenten: \n", components)


if __name__ == "__main__":
    '''well-constraint-Beispiel:'''
    # figure_3a = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
    #              ("C", "D"),
    #              ("C", "D"), ("C", "D"),
    #              ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]
    # well_constraint = nx.MultiDiGraph(figure_3a)
    # pebblegame(well_constraint, 3, 3)
    #
    '''under-constraint-Beispiel:'''
    # # figure_3b = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"), ("C", "D"), ("C", "D"), ("C", "D"),
    # #                             ("C", "E"), ("C", "F"), ("C", "F",)]
    # # under_constraint = nx.MultiDiGraph(figure_3b)
    # # pebblegame(under_constraint, 3, 3)

    '''over-constraint-Beispiel:'''
    # full_graph_octaeder = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5),
    #                        (4, 6), (5, 6)]
    # G = nx.from_edgelist(full_graph_octaeder)
    # G_5 = create5Ggraph(G)
    # pebblegame(G_5, 5, 6)

    '''under-constraint-Beispiel but definetely with rigid components:'''
    full_graph_octaeder_and_additional_limb = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6),
                                               (3, 4), (3, 5), (3, 6), (4, 5),
                                               (4, 6), (5, 6), (6, 7)]
    G = nx.from_edgelist(full_graph_octaeder_and_additional_limb)
    G_5 = create5Ggraph(G)
    pebblegame(G_5, 5, 6)
