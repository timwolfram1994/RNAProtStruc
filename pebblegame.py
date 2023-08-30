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
    components = np.zeros((len(G.nodes), len(G.nodes)))

    # iterate in an arbitrary order over all nodes from G
    # edges_to_insert = list(G.edges)
    # random.shuffle(edges_to_insert)
    edges_to_insert = [('A', 'B', 0), ('C', 'D', 0), ('B', 'D', 0), ('C', 'F', 2), ('C', 'D', 1), ('A', 'E', 0),
                       ('C', 'F', 0), ('A', 'C', 1), ('C', 'E', 0), ('A', 'E', 1), ('B', 'D', 1), ('C', 'F', 1),
                       ('A', 'D', 0), ('C', 'D', 2), ('A', 'C', 0)]
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
        if components[index_u][index_v] == 1:
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
            nx.draw(D, with_labels=True)
            plt.show()
            for node in D.nodes:
                print(node,": ",D.nodes[node]["pebbles"])
            D_reversed = D.reverse(copy=True)
            not_reached = [node for node in D_reversed.nodes if node not in reach_uv and D.nodes[node]["pebbles"] != 0]
            nx.draw(D_reversed, with_labels=True)
            plt.show()
            print("Reach(u,v) :", reach_uv)

            identified_component = list(D.nodes)
            for w in not_reached:
                for successor in nx.descendants(D_reversed, w):
                    if successor in identified_component:
                        identified_component.remove(successor)


            # Update der n x n matrix
            matrix_len = len(identified_component)
            for i in range(0, matrix_len - 1):
                for j in range(i + 1, matrix_len):
                    index_i = list(D.nodes).index(identified_component[i])
                    index_j = list(D.nodes).index(identified_component[j])
                    components[index_j][index_i] = 1
                    components[index_i][index_j] = 1

    if total_pebbles == l:
        if len(D.edges) == len(G.edges):
            print("well-constraint; l pebbles remain. no edge has been left out")
        else:
            print("over-constraint; l pebbles remain. ,", len(G.edges) - len(D.edges), " have been left out")
    elif total_pebbles > l:
        if len(D.edges) == len(G.edges):
            print("under-constraint; ", total_pebbles, " pebbles remain. no edge has been left out")
        else:
            print("other: ", total_pebbles, " pebbles remain,", len(G.edges) - len(D.edges), " have been left out")
    else:
        print("error!", total_pebbles, "pebbles remain")
    print("Matrix steifer Komponenten: \n", components)


if __name__ == "__main__":
    '''well-constraint-Beispiel:'''
    figure_3a = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
                 ("C", "D"),
                 ("C", "D"), ("C", "D"),
                 ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]
    well_constraint = nx.MultiDiGraph(figure_3a)
    pebblegame(well_constraint, 3, 3)

    '''under-constraint-Beispiel:'''

    '''well constraint-Beispiel:'''
    # figure_3b = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"), ("C", "D"), ("C", "D"), ("C", "D"),
    #                             ("C", "E"), ("C", "F"), ("C", "F",)]
    # under_constraint = nx.MultiDiGraph(figure_3b)
    # pebblegame(under_constraint, 3, 3)
