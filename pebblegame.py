import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import test_samples

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
    component_matrix = pd.DataFrame(columns=V, index=V)
    component_matrix.fillna(0, inplace=True)

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
        if component_matrix.at[u, v] == 1:
            print("Edge already in rigid component identified")
            continue

        # Tiefensuche nach pebbles für u und v

        peb_u = D.nodes[u]["pebbles"]
        peb_v = D.nodes[v]["pebbles"]
        while peb_u + peb_v < (l + 1):

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

        # (nach Tiefensuche) einfügen der neuen Kante (u,v)
        edge_inserted = False
        if peb_u + peb_v >= l + 1:
            D.add_edge(e[0], e[1])
            D.nodes[u]["pebbles"] = D.nodes[u]["pebbles"] - 1
            peb_u = peb_u - 1
            total_pebbles -= 1
            edge_inserted = True

        if not edge_inserted:
            continue

        # Component Detection V2:
        # 1.) check, whether there are still more than l pebbles on (u,v)
        if peb_u + peb_v >= l + 1:
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
            current_component = set(D.nodes)
            dfs_w = {*reach_uv}

            while not_reached:
                w = not_reached.pop()
                revered_reach_w = dfs_reach_reverse(D, w, dfs_w)
                dfs_w.update(revered_reach_w)
                for node in revered_reach_w:
                    if node in not_reached:
                        not_reached.remove(node)

            for reached_node_from_w in dfs_w:
                if reached_node_from_w in current_component:
                    current_component.remove(reached_node_from_w)

            current_component.update(reach_uv)

            # Update der n x n matrix
            current_component = list(current_component)
            component_nodes_len = len(current_component)

            '''alternativ als pd.DF; mit indizes/columns alle namen der d.notes knoten verwenden -> erspart umrechnung'''
            component_edges= []
            for i in range(0, component_nodes_len - 1):
                for j in range(i + 1, component_nodes_len):
                    node_i = current_component[i]
                    node_j = current_component[j]
                    component_matrix.at[node_i, node_j] = 1
                    component_matrix.at[node_j, node_i] = 1
                    component_edges.append((node_i,node_j))
            identified_components.append(component_edges)
    print("------------------------------------------------------------------------")
    print("REMAINING EDGES : ", len(edges_to_insert))
    print("INSERTED EDGES : ", len(D.edges))

    nx.draw(D, with_labels=True)
    plt.show()

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
    print("Matrix steifer Komponenten: \n", component_matrix)

if __name__ == "__main__":

    pebblegame(test_samples.sample10_graph,2,3)


'''zusätzliches pebble_game für l<k, wobei selbstreflexive Kanten erlaubt sind. hierbei sind Komponenten auch Knotendisjunkt. 
Ein Knoten existiert nur in einer Komponente. Eine Komponente, kann dabei eine andere Komponente schlucken'''

'''d.notes[index(x) vermeiden, hierbei pd.dataframe zurückgreifen und dabei node_index als Name verwenden '''


'''kl-sparsity eigenschaft'''
