import random
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
    # initiate directed pebble graph D with k pebbles and zero edges
    G = multiDiGraph
    D = nx.MultiDiGraph()
    D.add_nodes_from(G, pebbles=k)
    V = list(D.nodes)

    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    components = np.zeros((len(G.nodes), len(G.nodes)))

    # randomizer for iterating over arbitrary edges
    # without replacement
    edges_to_insert = []
    for edge_of_G in G.edges:
        edges_to_insert.append(edge_of_G)

    for i in range(0, len(G.edges)):
        # wähle eine zufällige Kante aus Edges_to_insert aus, über den Index der Liste einzufügender Kanten
        e = edges_to_insert[random.randint(0, len(edges_to_insert))]

        # definiere die Knoten u und v aus der einzusetzenden Kante
        u = V[V.index(e[0])]
        v = V[V.index(e[1])]

        # Prüfung ob u = v, falls ja, nächste Kante
        if u == v:
            continue

        # prüfung ob (u,v) in irgendeiner Komponente (matrix zelle true): falls ja, nächste Kante
        if components[list(D.nodes).index(u)][
            list(D.nodes).index(v)] == 1:
            continue

        # einfügen der neuen Kante (u,v)
        pebbles_uv = u["pebbles"] + v["pebbles"]

        if pebbles_uv >= l + 1:
            D.add_edge(e[0], e[1])
            u["pebbles"] = u["pebbles"] - 1

        # Tiefensuche für u (eingeschlossen v) .
        else:

            while u["pebbles"] + v["pebbles"] < l + 1:

                # Sofern u bereits 5 pebbles hat, werden u und v vertauscht.
                # stellt sicher, dass nie mehr als 5 pebbles an u liegen werden
                if u["pebbles"] == 5:
                    u = V[V.index(e[1])]
                    v = V[V.index(e[0])]
                visited = []
                current_node = u
                to_visit = deque()
                # Vorabrunde, damit ich später Knoten in to_visit habe, die ich für meine DFS abarbeiten kann

                Continue_with_descendats = True
                for successor in D.successors(u):
                    if successor["pebbles"] != 0:
                        successor["pebbles"] -= 1
                        u["pebbles"] += 1
                        D.remove_edge(u, successor)
                        D.add_edge(successor, u)
                        Continue_with_descendats = False
                        break
                    else:
                        to_visit.append(successor)
                        continue

                if not Continue_with_descendats:
                    continue  # ... with while loop to find another pebble additionally to the one, just found - or to build the edge e

                # Tiefensuche innerhalb des Reaches, bis Pebble gefunden wurde
                parental_node = u
                while to_visit:
                    current_node = to_visit.pop()
                    # füge traversierte Kante visited hinzu
                    traversed_edge = (parental_node, current_node)
                    visited.append(traversed_edge)

                    for successor in D.successors(u):
                        for edge in visited:
                            if successor in edge:
                                continue
                        if successor["pebbles"] != 0:


                pebbles_after_dfs = "TBD"
                if pebbles_uv == u["pebbles"] + v["pebbles"]:
                    break
                pebbles_uv = u["pebbles"] + v["pebbles"]

            # While-Schleife erfolgreich: Genug pebbles sind vorhanden, eine neue Kante wird eingefügt.
            if pebbles_uv >= l + 1:
                D.add_edge(e[0], e[1])
                u["pebbles"] = u["pebbles"] - 1
            # While-Schleife nicht erfolgreich: Abarbeiten der nächsten Kante
            else:
                continue

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if D.nodes[e[0]]["pebbles"] + D.nodes[e[1]]["pebbles"] >= l + 1:
            continue

        # 2.) compute reach:
        else:
            reach = set()
            for successor_u in nx.descendants(D, u):
                reach.add(successor_u)
            for successor_v in nx.descendants(D, v):
                reach.add(successor_v)

            # 2.a) check for any free pebble within all elements of reach(u,v)
            for node in reach:
                if node["pebbles"] != 0:
                    break
                # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:

            # Reversed Graph erstellen
            D_reversed = D.reverse(copy=True)
            # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:
            not_reached = [node for node in D_reversed.nodes if node not in reach and node["pebbles" != 0]]
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

        edges_to_insert.pop(e)

    count_remaining_pebbles = 0
    for node in D.nodes:
        count_remaining_pebbles = count_remaining_pebbles + node["pebbles"]
    print("remaining pebbles :", count_remaining_pebbles)
    if len(D.edges) < len(G.edges):
        print("edges have been left out")
    else:
        print("no edges have been left out")
