import random
import pylab as pl
from collections import deque
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
    # Tiefen-Pebble-Suche als Fkt

    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)

    def dfs_find_pebble(digraph: nx.MultiDiGraph, u, v):
        for node in D.nodes:
            print(node, ": ", D.nodes[node]["pebbles"])
        pos_nodes = {
            "A": (0, 0),
            "B": (-0.1, -0.1),
            "C": (0.1, -0.1),
            "D": (0, -0.2),
            "E": (0.2, 0),
            "F": (0.2, -0.2)
        }
        # nx.draw(D, with_labels=True,pos = pos_nodes)
        # pl.show()
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
                        visited.append((parent, child))
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

    # initiate directed pebble graph D with k pebbles and zero edges

    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    components = np.zeros((len(G.nodes), len(G.nodes)))

    # randomizer for iterating over arbitrary edges
    # without replacement
    # edges_to_insert = list(G.edges)
    # random.shuffle(edges_to_insert)
    edges_to_insert = [('B', 'D', 0), ('A', 'E', 1), ('A', 'B', 0), ('A', 'E', 0), ('A', 'C', 0), ('C', 'E', 0),
                       ('C', 'F', 1), ('A', 'C', 1), ('C', 'F', 2), ('C', 'D', 2), ('C', 'D', 0), ('A', 'D', 0),
                       ('C', 'D', 1), ('B', 'D', 1), ('C', 'F', 0)]

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
        if components[V.index(u)][
            V.index(v)] == 1:
            continue

        # Tiefensuche für u (eingeschlossen v)
        while D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] < (l + 1):
            print("DFS required, next: DFS(u), peb(u+v) = ", D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"])

            dfs_u = True
            if D.nodes[u]["pebbles"] == k:
                print("u pebble limit reached")
                dfs_u = False

            if dfs_u:
                dfs_u = dfs_find_pebble(D, u, v)
                if dfs_u:
                    print("DFS(u) successful")
                else:
                    print("DFS(u) failed")
                # redirect pebble-path
            if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= (l + 1):
                break
            print("DFS(u) done. DFS still required: peb(u+v) = ", D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"])
            dfs_v = True
            if D.nodes[v]["pebbles"] == k:
                print("v pebble limit reached")
                dfs_v = False
            if dfs_v:
                dfs_v = dfs_find_pebble(D, v, u)
                if dfs_v:
                    print("DFS(v) successful")
                else:
                    print("DFS(v) failed")

            if not dfs_u and not dfs_v:
                break

        # (nach Tiefensuche) einfügen der neuen Kante (u,v)
        edge_inserted = False
        if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= l + 1:
            D.add_edge(e[0], e[1])
            D.nodes[u]["pebbles"] = D.nodes[u]["pebbles"] - 1
            edge_inserted = True

        if not edge_inserted:
            continue

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if D.nodes[u]["pebbles"] + D.nodes[v]["pebbles"] >= l + 1:
            continue
        # 2.) compute reach:
        else:
            reach = set()
            for successor_u in nx.descendants(D, u):
                reach.add(successor_u)
            for successor_v in nx.descendants(D, v):
                reach.add(successor_v)

            # 2.a) check for any free pebble within all elements of reach(u,v)
            '''hier kann man auch die pebble suche funktion anwenden, damit nicht der gesamte reach berechnet wird!'''
            pebble_found = False
            for node in reach:
                if D.nodes[node]["pebbles"] != 0:
                    pebble_found = True
                    break
            if pebble_found:
                continue

            # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:
            # Reversed Graph erstellen
            D_reversed = D.reverse(copy=True)
            # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:
            not_reached = [node for node in D_reversed.nodes if node not in reach and D.nodes[node]["pebbles"] != 0]
            identified_component = list(D.nodes)
            for w in not_reached:
                for successor in nx.descendants(D_reversed, w):
                    try:
                        index_successor = identified_component.index(successor)
                        if index_successor:
                            identified_component.pop(identified_component[index_successor])
                    finally:
                        continue

            # Update der n x n matrix
            '''delete all previous Vi???'''
            l = len(identified_component)
            for i in range(0, l - 1):
                for j in range(i + 1, l):
                    index_i = list(D.nodes).index(identified_component[i])
                    index_j = list(D.nodes).index(identified_component[j])
                    components[index_j][index_i] = 1
                    components[index_i][index_j] = 1

    count_remaining_pebbles = 0
    for node in D.nodes:
        count_remaining_pebbles = count_remaining_pebbles + D.nodes[node]["pebbles"]
    print("remaining pebbles :", count_remaining_pebbles)
    if len(D.edges) < len(G.edges):
        print("Some edges have been left out")
    else:
        print("no edges have been left out")


if __name__ == "__main__":
    figure_3a = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
                 ("C", "D"),
                 ("C", "D"), ("C", "D"),
                 ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]

    well_constraint = nx.MultiDiGraph(figure_3a)
    pebblegame(well_constraint, 3, 3)
# Backup

#     '''2 Seperate Tiefensuchen für u und v'''
#     '''Prüfe, ob u oder v bereits k pebbles hat, überspringe ggf. diese Tiefensuche'''
#
#     # Sofern u bereits 5 pebbles hat, werden u und v vertauscht.
#     # stellt sicher, dass nie mehr als 5 pebbles an u liegen werden
#     if u["pebbles"] == k:
#         u = V[V.index(e[1])]
#         v = V[V.index(e[0])]
#     visited = []
#     current_node = u
#     to_visit = deque()
#     # Vorabrunde, damit ich später Knoten in to_visit habe, die ich für meine DFS abarbeiten kann
#
#     Continue_with_descendats = True
#     childenOfU = []
#     for successor in D.successors(u):
#         if successor["pebbles"] != 0:
#             successor["pebbles"] -= 1
#             u["pebbles"] += 1
#             D.remove_edge(u, successor)
#             D.add_edge(successor, u)
#             Continue_with_descendats = False
#             break
#         else:
#             childenOfU.append(successor)
#             continue
#
#     if not Continue_with_descendats:
#         continue  # ... with while loop to find another pebble additionally to the one, just found - or to build the edge e
#
#     # Tiefensuche innerhalb des Reaches, bis Pebble gefunden wurde
#
#     parental_node = u
#     to_visit.append([u, iter(D[childenOfU])])
#     while to_visit:
#         current_node = to_visit.pop()
#         # füge traversierte Kante visited hinzu
#         traversed_edge = (parental_node, current_node)
#         visited.append(traversed_edge)
#
#         for successor in D.successors(u):
#             for edge in visited:
#                 if successor in edge:
#                     continue
#                 else:
#                     to_visit.append(successor)
#             if successor["pebbles"] != 0:
#
#     pebbles_after_dfs = "TBD"
#     if pebbles_uv == u["pebbles"] + v["pebbles"]:
#         break
#     pebbles_uv = u["pebbles"] + v["pebbles"]
#
# # While-Schleife erfolgreich: Genug pebbles sind vorhanden, eine neue Kante wird eingefügt.
# if pebbles_uv >= l + 1:
#     D.add_edge(e[0], e[1])
#     u["pebbles"] = u["pebbles"] - 1
# # While-Schleife nicht erfolgreich: Abarbeiten der nächsten Kante
# else:
#     continue
