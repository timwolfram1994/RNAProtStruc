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
        return visited

    def dfs_reach(digraph: nx.MultiDiGraph, u, v, stop_at_pebble=False):
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
        return visited

    # Definitions
    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)
    total_pebbles = len(V) * k
    identified_components = []
    # initiate directed pebble graph D with k pebbles and zero edges

    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    len_d_nodes = len(V)
    components = np.zeros((len_d_nodes, len_d_nodes), dtype=int)
    components_pd = pd.DataFrame

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
        '''bei Pebble game mit l<k erlaubt! To be added!'''
        if k <= l and u == v:
            continue

        # prüfung ob (u,v) in irgendeiner Komponente (matrix zelle true): falls ja, nächste Kante
        index_u = V.index(u)
        index_v = V.index(v)
        if components[int(index_u)][int(index_v)] == 1:
            print("Edge already in rigid component identified")
            continue

        # Tiefensuche für u (eingeschlossen v)
        while D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] < (l + 1):
            dfs_u = True
            if D.nodes[u]["pebbles"] == k:
                dfs_u = False

            if dfs_u == True:
                dfs_u = dfs_find_pebble(D, u, v)
                # redirect pebble-path
            if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= (l + 1):
                break
            dfs_v = True
            if D.nodes[v]["pebbles"] == k:
                dfs_v = False
            if dfs_v == True:
                dfs_v = dfs_find_pebble(D, v, u)

            if dfs_u != True and dfs_v != True:
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
            # 2a) suche im Reach von u oder v nach einem pebble. Ist eins vorhanden, wird die suche gestoppt und "True" wiedergegeben.
            # Die Component Detection bricht dann ab.
            # -> berechnet nicht zwingend den ganzen reach, sofern nicht erforderlich und spart somit Zeit
            pebble_in_reach_u = dfs_reach(D, u, v, stop_at_pebble=True)
            if pebble_in_reach_u == True:
                continue
            pebble_in_reach_v = dfs_reach(D, v, u, stop_at_pebble=True)
            if pebble_in_reach_v == True:
                continue

            # sofern kein pebble gefunden wurde, wird für 2b) der reach(u,v) bereitgestellt
            reach_uv = set(pebble_in_reach_u)
            reach_uv.update(pebble_in_reach_v)

            # 2.b) DFS from nodes not in reach(u,v) in Supportgraph with all edges reversed:
            '''alle knoten von 2a reach_uv haben folglich 0 pebbles (außer ggf. u oder v selsbt) und gehören zur Komponente!, auch wenn im reach von w'''
            not_reached = [node for node in D.nodes if node not in reach_uv and D.nodes[node]["pebbles"] != 0]
            # nx.draw(D, with_labels=True)
            # plt.show
            print("Reach(u,v) :", reach_uv)
            current_component_nodes = set(D.nodes)
            dfs_w = {*reach_uv}

            while not_reached:
                w = not_reached.pop()
                revered_reach_w = dfs_reach_reverse(D, w, dfs_w)
                dfs_w.update(revered_reach_w)
                for node in revered_reach_w:
                    if node in not_reached:
                        not_reached.remove(node)

            for reached_node_from_w in dfs_w:
                if reached_node_from_w in current_component_nodes:
                    current_component_nodes.remove(reached_node_from_w)

            current_component_nodes.update(reach_uv)

            # Update der n x n matrix
            current_component_nodes = list(current_component_nodes)
            component_nodes_len = len(current_component_nodes)

            '''alternativ als pd.DF; mit indizes/columns alle namen der d.notes knoten verwenden -> erspart umrechnung'''
            current_component = []
            for i in range(0, component_nodes_len - 1):
                for j in range(i + 1, component_nodes_len):
                    index_i = V.index(current_component_nodes[i])
                    index_j = V.index(current_component_nodes[j])
                    components[index_j][index_i] = 1
                    current_component.append((current_component_nodes[i],current_component_nodes[j]))
                    components[index_i][index_j] = 1
            identified_components.append(current_component)
    print("------------------------------------------------------------------------")
    print("REMAINING EDGES : ", len(edges_to_insert))
    print("INSERTED EDGES : ", len(D.edges))

    nx.draw(D, with_labels=True)
    plt.show()

    print("identified components: ", identified_components)
    # fomat matrix
    header_column = np.array([node for node in D.nodes])
    components = np.column_stack((header_column, components))
    header_null = np.array(["-"])
    header_row = np.hstack((header_null, header_column))
    components = np.row_stack((header_row, components))

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

    return identified_components


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

    # '''Moser spindle (Laman-Graph mit 7 Knoten; für 2,3 Pebble Game'''
    # laman7 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("B", "D"), ("D", "E"), ("D", "F"), ("E", "F"),
    #           ("E", "G"), ("F", "G"),
    #           ("G", "A")]
    # well_constraint = nx.from_edgelist(laman7)
    # pebblegame(well_constraint, 2, 3)

    # overconstrant_1 = [(0, 1), (0, 8), (0, 9), (0, 11), (1, 7), (1, 8), (1, 10), (1, 11), (1, 13), (2, 3), (2, 7),
    #                    (2, 8), (2, 14), (3, 6), (3, 14), (4, 5), (4, 8), (4, 9), (4, 11), (4, 12), (5, 6), (5, 7),
    #                    (5, 9), (5, 12), (5, 13), (6, 13), (6, 14), (7, 12), (7, 14), (8, 12), (8, 13), (8, 14), (9, 10),
    #                    (9, 12), (10, 11)]
    # over = nx.from_edgelist(overconstrant_1)
    # pebblegame(over, 2, 3)
    # #
    # underconstraint = [(0, 6), (0, 11), (0, 12), (0, 14), (1, 6), (1, 7), (1, 8), (1, 9), (2, 12), (3, 6), (3, 7),
    #                    (3, 10), (4, 5), (4, 7), (4, 12), (4, 14), (5, 8), (7, 11), (7, 13), (9, 10), (9, 11), (9, 13),
    #                    (10, 12), (12, 14), (13, 14)]
    #
    # under = nx.from_edgelist(underconstraint)
    # pebblegame(under, 2, 3)

    # other_0 = [(0, 4), (0, 6), (0, 11), (0, 13), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 3),
    #            (3, 5), (3, 7), (3, 13), (4, 5), (4, 8), (4, 11), (5, 9), (5, 10), (5, 13), (6, 10), (6, 11), (6, 14),
    #            (7, 8), (7, 10), (7, 14), (8, 9), (8, 11), (9, 12), (11, 13), (12, 13)]
    # other = nx.from_edgelist(other_0)
    # pebblegame(other, 2, 3)

    path = "graphs/test_2octa.edgelist"
    open(path, "rb")
    test2_octa = nx.read_edgelist(path)
    test2_octa_5G = create5Ggraph(test2_octa)
    pebblegame(test2_octa_5G,5,6)


'''zusätzliches pebble_game für l<k, wobei selbstreflexive Kanten erlaubt sind. hierbei sind Komponenten auch Knotendisjunkt. 
Ein Knoten existiert nur in einer Komponente. Eine Komponente, kann dabei eine andere Komponente schlucken'''


'''d.notes[index(x) vermeiden, hierbei pd.dataframe zurückgreifen und dabei node_index als Name verwenden '''