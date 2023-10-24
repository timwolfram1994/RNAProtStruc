import networkx as nx
import itertools
import random
from helper_functions import directed_dfs_edges
from helper_functions import pairwise
from collections import deque
import pebblegame_copy as pg
# import pdb_to_graph
import os
import pandas as pd
import numpy as np


# to do: graphen einfärben, steife komponententen in rigidty matrix testen
#

def pebble_collection(D, u, v):
    # depth first search from starting node
    successors_until_w = []
    for idx, _edge in enumerate(nx.dfs_edges(D, u)):  # iterate through edges in dfs manner
        if v in _edge or u == _edge[
            1]:  # avoid taking pebble from u or v !!! besser nochmal abgleichen, ob man das so machen kann
            continue
        successors_until_w.append(_edge)
        if D.nodes[_edge[1]]['pebbles'] > 0:  # first edge is (u, u+1)
            D.nodes[_edge[1]]['pebbles'] -= 1  # take pebble from node
            D.nodes[u]['pebbles'] += 1  # add pebble to starting node
            # nun die Kanten umdrehen
            # backtracking the path from w tu u
            path_to_w = []
            queue = deque(successors_until_w)
            while queue:
                edge = queue.pop()
                if len(path_to_w) == 0 or edge[1] == path_to_w[-1][
                    0]:  # if i am at first element or the second element of the predecessor is the first of the current
                    path_to_w.append(edge)
                if edge[0] == u:
                    break

            for __edge in path_to_w:  # reverse the directions of the edges, "pairwise" transforms nodelist to edgelist
                D.remove_edge(__edge[0], __edge[1])
                D.add_edge(__edge[1], __edge[0])
            break  # if we found a pebble we stop the dfs
    return D


def dfs_find_pebble(D, u, v):
    visited = []
    visited.append((u, v))
    to_visit = [(u, iter(D.successors(u)))]
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
                    to_visit.append((child, iter(D.successors(child))))
        except StopIteration:
            to_visit.pop(-1)
    return False


def pebblegame(G, k, l):
    # zu berichtigendende zeilen:
    # gibt reach nur direkted pfade aus?
    # zufallsordnung für kantenbearbeitung

    D = nx.MultiDiGraph()
    D.add_nodes_from(G)
    nx.set_node_attributes(D, k, "pebbles")
    randomized_edgelist = list(G.edges)
    random.shuffle(randomized_edgelist)
    # print(f'randomized edgelist: {randomized_edgelist}')
    for edge in randomized_edgelist:  # try to append edges to D in a randomized manner
        u = edge[0]
        v = edge[1]
        if D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] >= l + 1:  # check whether u and v have enough pebbles
            D.add_edge(u, v)
            D.nodes[u]['pebbles'] -= 1  # remove one pebble from u

        else:  # collect pebbles
            while D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] < l + 1:
                compare1 = D.nodes[u]['pebbles'] + D.nodes[v][
                    'pebbles']  # break out of while loop if pebbles didn't change

                if D.nodes[u][
                    'pebbles'] < k:  # vertices must not have more than k pebbles. so we don't do a dfs if we have already 5
                    dfs_find_pebble(D, u, v)

                if D.nodes[v][
                    'pebbles'] < k:  # vertices must not have more than k pebbles. so we don't do a dfs if we have already 5?
                    dfs_find_pebble(D, v, u)  # v will now be handled as u

                compare2 = D.nodes[u]['pebbles'] + D.nodes[v][
                    'pebbles']  # break out of while loop if pebbles didn't change
                if compare1 == compare2:
                    break

            if D.nodes[u]['pebbles'] + D.nodes[v][
                'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
                D.add_edge(u, v)  # insert directed edge uv in D
                D.nodes[u]['pebbles'] -= 1

    # count the total pebbles
    totalPebbles = 0
    for u, node in D.nodes(data=True):
        totalPebbles += node["pebbles"]

    # debug testrecke
    # print(f'number edges D: {D.number_of_edges()}')
    # print(f'number edges G: {G.number_of_edges()}')
    print(f'Edges of D: {D.edges()}')
    print(f'remaining pebbles: {totalPebbles}')
    print(f'Edges G: {G.number_of_edges()}, Edges D: {D.number_of_edges()}')

    if totalPebbles == l:
        if D.number_of_edges() == G.number_of_edges():  # no edge rejection
            return "well constrained"
        else:
            return "over-constrained"
    elif totalPebbles > l:
        if D.number_of_edges() == G.number_of_edges():
            return "under-constrained"
        else:
            return "other"


def component_detection_1(multiDiGraph: nx.MultiDiGraph, k, l):
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

    # initiate directed pebble graph D with k pebbles and zero edges

    # initiiere n x n matrix aller knoten zur Darstellung bereits vorhandener Komponenten
    len_d_nodes = len(V)
    components = np.zeros((len_d_nodes, len_d_nodes), dtype=int)
    components_pd = pd.DataFrame
    component_list = []

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

            ### now let's start the component detection ###



    # jetzt habe ich zwar ne component aber weiß ich ob die component rigid ist oder nicht? doch: gibt steife komponenten aus

    # debug testrecke
    # print(f'number edges D: {D.number_of_edges()}')
    # print(f'number edges G: {G.number_of_edges()}')

    # count the total pebbles
    totalPebbles = 0
    for u, node in D.nodes(data=True):
        totalPebbles += node["pebbles"]

    if totalPebbles == l:
        if D.number_of_edges() == G.number_of_edges():  # no edge rejection
            return "well constrained"
        else:
            return "over-constrained"
    elif totalPebbles > l:
        if D.number_of_edges() == G.number_of_edges():
            return "under-constrained"
        else:
            return "other"

    return


if __name__ == '__main__':
    ### create Graph
    # filename = "2eso.pdb"
    # path = os.path.join(os.getcwd(), "pdb_samples", filename)

    # G = pdb_to_graph.pdb_to_graph(path)

    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edges_from([(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)])
    # print(f'edges: {G.edges()} type: {type(list(G.edges()))}, length: {len(G.edges())}')

    G_3 = nx.Graph()
    G_3.add_nodes_from([1, 2, 3])
    G_3.add_edges_from([(1, 2), (1, 3), (2, 3)])

    G_a = nx.MultiGraph()  # testing graph from Lee-Streinu Paper (well-constrained)
    G_a.add_nodes_from([1, 2, 3, 4, 5, 6])
    G_a.add_edges_from(
        [(1, 2), (1, 3), (1, 3), (1, 4), (1, 5), (1, 5), (2, 4), (2, 4), (3, 4), (3, 4), (3, 4), (3, 5), (3, 6), (3, 6),
         (3, 6)])

    G_b = nx.MultiGraph()  # testing graph from Lee-Streinu Paper (under-constrained)
    G_b.add_nodes_from([1, 2, 3, 4, 5, 6])
    G_b.add_edges_from(
        [(1, 2), (1, 3), (1, 3), (1, 4), (1, 5), (1, 5), (2, 4), (2, 4), (3, 4), (3, 4), (3, 4), (3, 5), (3, 6),
         (3, 6)])

    # print(G_a)
    print(f'Graph a) should be well-constraint. Here it is {pebblegame(G_a, 3, 3)}')

    # print(G)
    # print(pebblegame(G, 3, 3))
    # print(G_3)
    # print(pebblegame(G_3, 3, 3))

    # print(G_b)
    # print(f'Graph b) should be under-constraint. Here it is {pebblegame(G_b, 3, 3)}')
    print(component_detection_1(G_a, 3, 3))

    print(
        f'G_a reference edgelist:{[(1, 2), (2, 4), (2, 4), (3, 1), (3, 1), (3, 4), (4, 3), (4, 3), (4, 1), (5, 1), (5, 1), (5, 3), (6, 3), (6, 3), (6, 3)]}')

'''reach_uv += [edge[0], edge[1]]
for _node in reach_uv:
    for pred in D.predecessors(_node):
        if pred not in reach_uv:
            queue.append(pred)
            queue_memory.add(pred)'''

overconstrant_1 = [(0, 1), (0, 8), (0, 9), (0, 11), (1, 7), (1, 8), (1, 10), (1, 11), (1, 13), (2, 3), (2, 7),
                   (2, 8), (2, 14), (3, 6), (3, 14), (4, 5), (4, 8), (4, 9), (4, 11), (4, 12), (5, 6), (5, 7),
                  (5, 9), (5, 12), (5, 13), (6, 13), (6, 14), (7, 12), (7, 14), (8, 12), (8, 13), (8, 14), (9, 10),
                    (9, 12), (10, 11)]
over = nx.from_edgelist(overconstrant_1)
print(pebblegame(over, 2, 3))

     #
underconstraint = [(0, 6), (0, 11), (0, 12), (0, 14), (1, 6), (1, 7), (1, 8), (1, 9), (2, 12), (3, 6), (3, 7),
                       (3, 10), (4, 5), (4, 7), (4, 12), (4, 14), (5, 8), (7, 11), (7, 13), (9, 10), (9, 11), (9, 13),
                   (10, 12), (12, 14), (13, 14)]
    #
under = nx.from_edgelist(underconstraint)
print(pebblegame(under, 2, 3))

