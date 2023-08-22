import random

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


def initiate_supportGraph(multigraph5G):
    k = 5
    l = 6
    h = nx.MultiDiGraph()
    h.add_nodes_from(multigraph5G, pebbles=k)
    return h


def pebblegame(supportGraph: nx.MultiDiGraph, multigraph5G):
    k = 5
    l = 6


    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    components = np.zeros((len(multigraph5G.nodes),len(multigraph5G.nodes)))

    # randomizer for iterating over arbitrary edges
    # without replacement
    original_edges = []
    for originalEdge in multigraph5G.edges:
        original_edges.append(originalEdge)
    initialLen = len(original_edges)

    for i in range(0, initialLen):
        randLen = len(original_edges)
        next_int = random.randint(0, randLen)
        currentEdge = original_edges[next_int]

        # Prüfung ob u = v:
        if currentEdge[0] == currentEdge[1]:
            continue

        # prüfung ob (u,v) in irgendeiner Komponente (matrix zelle true):
        if components[list(supportGraph.nodes).index(currentEdge[0])][list(supportGraph.nodes).index(currentEdge[1])] == 1:
            continue

        # einfügen der neuen Kante (u,v)
        if supportGraph.nodes[currentEdge[0]]["pebbles"] + supportGraph.nodes[currentEdge[1]]["pebbles"] >= l + 1:
            supportGraph.add_edge(currentEdge[0], currentEdge[1])
            supportGraph.nodes[currentEdge[0]]["pebbles"] = supportGraph.nodes[currentEdge[0]]["pebbles"] - 1

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if supportGraph.nodes[currentEdge[0]]["pebbles"] + supportGraph.nodes[currentEdge[1]]["pebbles"] >= l + 1:
            continue

        # 2.) compute reach:
        else:
            # Definition eines u und v Knotens sowie zweier Listen für abgearbeitete Knoten und erkannte, noch nicht besuchte Knoten innerhalb des Reaches
            visited = []
            to_visit = []
            u_node = currentEdge[0]
            v_node = currentEdge[1]

            # initiale Befüllung der Listen mit direkten Nachfolgern von u und v
            visited.append(u_node)
            successors_of_u = supportGraph.successors(u_node)
            for successor in successors_of_u:
                to_visit.append(successor)
            if v_node not in to_visit:
                successors_of_v = supportGraph.successors(v_node)
                for successor in successors_of_v:
                    to_visit.append(successor)

            # iteratives Befüllen der Listen mit indirekten Nachfolgern, so lange es noch zu besuchende Knoten gibt:

            while len(to_visit) != 0:
                current_node = to_visit[-1]
                if current_node not in visited:
                    visited.append(to_visit[-1])
                    if len(supportGraph.successors(current_node)) == 0:
                        to_visit.pop(-1)

                    else:
                        successors = supportGraph.successors(current_node)
                        for successor in successors:
                            to_visit.append(successor)

            # 2.a) check for any free pebble within all elements of reach(u,v)
            for node in visited:
                if node["pebbles"] != 0:
                    break
                #       prüfen!!! ob der mit neuer Kante weitermacht

                # 2.b) DFS from nodes not in reach(u,v) in Supportgraph mit allen Kanten umgedreht:
                else:
                    # Reversed Graph erstellen
                    supportgraph_reversed = supportGraph.reverse(copy=True)

                    # Alle Knoten auflisten, welche nicht im Reach(u,v) liegen
                    not_in_reach = [node for node in supportGraph.nodes if node not in visited]
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
                                if len(supportGraph.successors(current_node)) == 0:
                                    to_visit.pop(-1)

                                else:
                                    successors = supportGraph.successors(current_node)
                                    for successor in successors:
                                        to_visit.append(successor)

                    identified_component.append(node for node in supportGraph.nodes if node not in visited)
                    # Update der n x n matrix
                    for i in range(0,len(identified_component)-1):
                        for j in range(i+1,len(identified_component)):
                            index_i = list(supportGraph.nodes).index(identified_component[i])
                            index_j = list(supportGraph.nodes).index(identified_component[j])

                            components[index_j][index_i] = 1
                            components[index_i][index_j] = 1





        original_edges.pop(currentEdge)
