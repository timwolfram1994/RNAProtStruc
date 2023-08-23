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

    for i in range(0, len(g.edges)):
        # wähle eine zufällige Kante aus Edges_to_insert aus, über den Index der Liste einzufügender Kanten
        current_edge_to_insert = edges_to_insert[random.randint(0, len(edges_to_insert))]

        # definiere die Knoten u und v aus der einzusetzenden Kante
        u = V[V.index(current_edge_to_insert[0])]
        v = V[V.index(current_edge_to_insert[1])]

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
            D.add_edge(current_edge_to_insert[0], current_edge_to_insert[1])
            u["pebbles"] = u["pebbles"]-1
            '''Prüfung, ob u-knoten 0 pebbles hat + problembehandlung ausstehend!'''

        else:
            while pebbles_uv < l+1:
                # Tiefensuche: zuerst für u...
                if u["pebbles"] < k:
                    # ...sofern v bereits k pebbles hat
                    if v["pebbles"] == k:
                        current_node = u

                        dfs_path_u = deque(u)
                        to_visit_u = deque(current_node)
                        while to_visit_u:
                            current_node = to_visit_u.pop()
                            successors = D.successors(current_node)
                            if successors:
                                for successor in successors:
                                    if successor["pebbles"] ==0 and successor is not v:
                                        to_visit_u.append(successor)
                                    else:
                                        successor["pebbles"] -=1
                                        u["pebbles"] += 1
                                        for edge in dfs_path_u:


                            last_node = current_node
                            dfs_path_u.append((last_node,current_node))
                            pass


        '''search for pebbles'''
        # move pebbles around

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if D.nodes[current_edge_to_insert[0]]["pebbles"] + D.nodes[current_edge_to_insert[1]]["pebbles"] >= l + 1:
            continue

        # 2.) compute reach:
        else:
            # Definition eines u und v Knotens sowie zweier Listen für abgearbeitete Knoten und erkannte, noch nicht besuchte Knoten innerhalb des Reaches
            visited = []
            '''set statt liste -> für effizienteren Durchgang ohne Dopplungen -> weniger iterationen'''
            to_visit = []
            u = current_edge_to_insert[0]
            v = current_edge_to_insert[1]

            # initiale Befüllung der Listen mit direkten Nachfolgern von u und v
            visited.append(u)
            successors_of_u = D.successors(u)
            for successor in successors_of_u:
                to_visit.append(successor)
            if v not in to_visit:
                successors_of_v = D.successors(v)
                for successor in successors_of_v:
                    to_visit.append(successor)

            # iteratives Befüllen der Listen mit indirekten Nachfolgern, so lange es noch zu besuchende Knoten gibt:

            while len(to_visit) != 0:
                current_node = to_visit[-1]
                if current_node not in visited:
                    visited.append(to_visit[-1])
                    '''ist  das richtig so? -> zu prüfen'''
                    if len(D.successors(current_node)) == 0:
                        to_visit.pop(-1)

                    else:
                        successors = D.successors(current_node)
                        for successor in successors:
                            to_visit.append(successor)

            # 2.a) check for any free pebble within all elements of reach(u,v)
            for node in visited:
                if node["pebbles"] != 0:
                    break
                '''prüfen!!! ob der mit neuer Kante weitermacht'''

                # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:
                else:
                # Reversed Graph erstellen
                supportgraph_reversed = D.reverse(copy=True)

                # Alle Knoten auflisten, welche nicht im Reach(u,v) liegen
                not_in_reach = [node for node in D.nodes if node not in visited]
                # DFS für alle Knoten außerhalb des Reaches(u,v)
                identified_component = []
                visited = set()
                for node in not_in_reach:
                    # initiale Befüllung von to_visit und visited
                    to_visit = []
                    visited.add(node)
                    successors = supportgraph_reversed.successors(node)
                    for successor in successors:
                        to_visit.append(successor)
                    # DFS(node)
                    while len(to_visit) != 0:
                        current_node = to_visit[-1]
                        if current_node not in visited:
                            visited.add(to_visit[-1])
                            if len(D.successors(current_node)) == 0:
                                to_visit.pop(-1)

                            else:
                                successors = D.successors(current_node)
                                for successor in successors:
                                    to_visit.append(successor)

                identified_component.append(node for node in D.nodes if node not in visited)
                # Update der n x n matrix
            '''delete all previous Vi???'''
            for i in range(0, len(identified_component - 1) - 1):
                for j in range(i + 1, len(identified_component)):
                    index_i = list(D.nodes).index(identified_component[i])
                    index_j = list(D.nodes).index(identified_component[j])

                    components[index_j][index_i] = 1
                    components[index_i][index_j] = 1

        edges_to_insert.pop(current_edge_to_insert)

    remaining_pebbles = 0
    for node in D.nodes:
        remaining_pebbles = remaining_pebbles + node["pebbles"]
    print("remaining pebbles :", remaining_pebbles)
    if len(D.edges) < len(G.edges):
        print("edges have been left out")
    else:
        print("no edges have been left out")
