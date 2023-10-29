import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


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


def generic_pebblegame(multiDiGraph: nx.MultiDiGraph, k, l):
    def dfs_find_pebble(digraph: nx.MultiDiGraph, u, v):
    # A function for a DFS, that stops immediately after a pebble is found on a node
    # to avoid unnessessary computational resources.
    # it returns the boolean true, if a pebble has been found and the whole reach of u,v otherwise.

        # Initiation of the lists for visited notes (visited) and the
        # backlog of nodes to visit (to_visit)
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
        return visited

    # Definitions and initiations of datastructures, notated accordingly to "Pebble game algorithms and sparse graphs"
    # by Audrey Lee and Ileana Streinu as appeared in Discrete Mathematics 308 (2008) 1425-1437)

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

        # definiere die Knoten u und v aus der einzusetzenden Kante
        u = e[0]
        v = e[1]
        print("edge to insert: ", u, v)

        # Check if the edge is a loop (u == v): if so, continue with next edge

        if k <= l and u == v:
            continue
        # though there might be cases for the generic pebblegame to tread special cases of loops (i.e. edge(u,
        # v)| u = v) we hereby decide to leave this control structure out, since there is no application herefore on
        # molecule graphs with a 5,6 pebble game.

        # edge acceptance: gather information on amount of pebbles and apply the DFS for pebble search,
        # if the sufficient amount of pebbles is not callable

        peb_u = D.nodes[u]["pebbles"]
        peb_v = D.nodes[v]["pebbles"]

        # initiate pebble-collection
        while peb_u + peb_v < (l + 1):

            # the variables dfs_u and dfs_v are initially set to True. If a dfs-pebble search fails
            # or if there are already k pebbles on u or v, the referring variable will be set to False
            # if both variables remain false (i.e. DFS failed or not allowed at the node) at the end of the one round
            # collecting pebbles for u and v, the collecting process ends.

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
    '''well-constraint-Beispiel:'''
    # figure_3a = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
    #              ("C", "D"),
    #              ("C", "D"), ("C", "D"),
    #              ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]
    # well_constraint = nx.MultiDiGraph(figure_3a)
    # pebblegame(well_constraint, 3, 3)

    '''under-constraint-Beispiel:'''
    # figure_3b = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
    #              ("C", "D"), ("C", "D"), ("C", "D"),
    #              ("C", "E"), ("C", "F"), ("C", "F",)]
    # under_constraint = nx.MultiDiGraph(figure_3b)
    # pebblegame(under_constraint, 3, 3)

    # '''over-constraint-Beispiel:'''
    # full_graph_octaeder = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5),
    #                        (3, 6), (4, 5),
    #                        (4, 6), (5, 6)]
    # G = nx.from_edgelist(full_graph_octaeder)
    # G_5 = create5Ggraph(G)
    # pebblegame(G_5, 5, 6)

    # '''other-Beispiel but definetely with rigid components:'''
    # full_graph_octaeder_and_additional_limb = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6),
    #                                            (3, 4), (3, 5), (3, 6), (4, 5),
    #                                            (4, 6), (5, 6), (6, 7)]
    # G = nx.from_edgelist(full_graph_octaeder_and_additional_limb)
    # G_5 = create5Ggraph(G)
    # pebblegame(G_5, 5, 6)

    # '''Moser spindle (Laman-Graph mit 7 Knoten; für 2,3 Pebble Game'''
    # laman7 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("B", "D"), ("D", "E"), ("D", "F"), ("E", "F"),
    #           ("E", "G"), ("F", "G"),
    #           ("G", "A")]
    # well_constraint = nx.from_edgelist(laman7)
    # pebblegame(well_constraint, 2, 3)

    # '''Moser spindle 3D (3D  Hajós construction; für 5,6 Pebble Game'''
    # '''2 Steife Komponenten im Graph enthalten; die um AD oder DG sich drehen können'''
    # hajos_edges = [("A", "B"), ("A", "C"), ("B", "C"),("C", "D"), ("B", "D"), ("E", "F"), ("D", "F"),
    #                ("D", "G"), (
    #                    "F", "G"), ("E", "A"), ("G", "E")]
    #
    # hajos_graph = nx.from_edgelist(hajos_edges)
    # hajos5G = create5Ggraph(hajos_graph)
    # pebblegame(hajos5G, 5, 6)

    '''Moser spindle (Laman-Graph mit 7 Knoten; für 2,3 Pebble Game'''
    laman7 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("B", "D"), ("D", "E"), ("D", "F"), ("E", "F"),
              ("E", "G"), ("F", "G"),
              ("G", "A")]
    well_constraint = nx.from_edgelist(laman7)
    generic_pebblegame(well_constraint, 2, 3)

    # overconstrant_1 = [(0, 1), (0, 8), (0, 9), (0, 11), (1, 7), (1, 8), (1, 10), (1, 11), (1, 13), (2, 3), (2, 7),
    #                    (2, 8), (2, 14), (3, 6), (3, 14), (4, 5), (4, 8), (4, 9), (4, 11), (4, 12), (5, 6), (5, 7),
    #                    (5, 9), (5, 12), (5, 13), (6, 13), (6, 14), (7, 12), (7, 14), (8, 12), (8, 13), (8, 14), (9, 10),
    #                    (9, 12), (10, 11)]
    # over = nx.from_edgelist(overconstrant_1)
    # generic_pebblegame(over, 2, 3)
    # #
    # underconstraint = [(0, 6), (0, 11), (0, 12), (0, 14), (1, 6), (1, 7), (1, 8), (1, 9), (2, 12), (3, 6), (3, 7),
    #                    (3, 10), (4, 5), (4, 7), (4, 12), (4, 14), (5, 8), (7, 11), (7, 13), (9, 10), (9, 11), (9, 13),
    #                    (10, 12), (12, 14), (13, 14)]
    #
    # under = nx.from_edgelist(underconstraint)
    # generic_pebblegame(under, 2, 3)

    # other_0 = [(0, 4), (0, 6), (0, 11), (0, 13), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 3),
    #            (3, 5), (3, 7), (3, 13), (4, 5), (4, 8), (4, 11), (5, 9), (5, 10), (5, 13), (6, 10), (6, 11), (6, 14),
    #            (7, 8), (7, 10), (7, 14), (8, 9), (8, 11), (9, 12), (11, 13), (12, 13)]
    # other = nx.from_edgelist(other_0)
    # generic_pebblegame(other, 2, 3)

    # path = "graphs/test_2octa.edgelist"
    # open(path, "rb")
    # test2_octa = nx.read_edgelist(path)
    # test2_octa_5G = create5Ggraph(test2_octa)
    # pebblegame(test2_octa_5G, 5, 6)

'''zusätzliches pebble_game für l<k, wobei selbstreflexive Kanten erlaubt sind. hierbei sind Komponenten auch Knotendisjunkt. 
Ein Knoten existiert nur in einer Komponente. Eine Komponente, kann dabei eine andere Komponente schlucken'''

'''d.notes[index(x) vermeiden, hierbei pd.dataframe zurückgreifen und dabei node_index als Name verwenden '''


'''kl-sparsity eigenschaft'''
