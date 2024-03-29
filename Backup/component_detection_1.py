import networkx as nx
import itertools
import random
from helper_functions import directed_dfs_edges
from helper_functions import pairwise
from collections import deque
import pebblegame_copy as pg
# import pdb_to_graph
import os

# to do: graphen einfärben, steife komponententen in rigidty matrix testen
#

def pebble_collection(D, u, v):


      # depth first search from starting node
    successors_until_w = []
    for idx, _edge in enumerate(nx.dfs_edges(D, u)):  # iterate through edges in dfs manner
        if v in _edge or u == _edge[1]:  # avoid taking pebble from u or v !!! besser nochmal abgleichen, ob man das so machen kann
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
                if len(path_to_w) == 0 or edge[1] == path_to_w[-1][0]: # if i am at first element or the second element of the predecessor is the first of the current
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
    #print(f'randomized edgelist: {randomized_edgelist}')
    for edge in randomized_edgelist:  # try to append edges to D in a randomized manner
        u = edge[0]
        v = edge[1]
        if D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] >= l + 1:  # check whether u and v have enough pebbles
            D.add_edge(u, v)
            D.nodes[u]['pebbles'] -= 1 # remove one pebble from u

        else:  # collect pebbles
            while D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] < l + 1:
                compare1 = D.nodes[u]['pebbles'] + D.nodes[v]['pebbles']  # break out of while loop if pebbles didn't change

                if D.nodes[u]['pebbles'] < k: # vertices must not have more than k pebbles. so we don't do a dfs if we have already 5
                    dfs_find_pebble(D, u, v)

                if D.nodes[v]['pebbles'] < k: # vertices must not have more than k pebbles. so we don't do a dfs if we have already 5?
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

    #debug testrecke
    #print(f'number edges D: {D.number_of_edges()}')
    #print(f'number edges G: {G.number_of_edges()}')
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


def component_detection_1(G, k, l):
    k = k
    l = l
    D = nx.MultiDiGraph()
    D.add_nodes_from(G)
    nx.set_node_attributes(D, k, "pebbles")
    edgeCount1 = len(D.edges())
    components = []
    randomized_edgelist = list(G.edges)
    randomized_edgelist = random.sample(randomized_edgelist, len(randomized_edgelist))
    # print(f'randomized edgelist: {randomized_edgelist}')
    for edge in randomized_edgelist:  # try to append edges to D in a randomized manner
        u = edge[0]
        v = edge[1]
        uv_in_same_comp = False
        for comp in components:
            if u in comp and v in comp:
                uv_in_same_comp = True
                break

        if not uv_in_same_comp:
            if D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] >= l + 1:  # check whether u and v have enough pebbles
                D.add_edge(u, v)
                D.nodes[u]['pebbles'] -= 1  # remove one pebble from u

            else:  # collect pebbles
                while D.nodes[u]['pebbles'] + D.nodes[v]['pebbles'] < l + 1:
                    compare1 = D.nodes[u]['pebbles'] + D.nodes[v][
                        'pebbles']  # break out of while loop if pebbles didn't change

                    if D.nodes[u][
                        'pebbles'] < k:  # vertices must not have more than k pebbles. so we don't do a dfs if we have already 5
                        dfs_u = dfs_find_pebble(D, u, v)

                    if dfs_u:
                        continue
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

            if D.nodes[u]['pebbles'] + D.nodes[v][
                'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
                D.add_edge(u, v)  # insert directed edge uv in D
                D.nodes[u]['pebbles'] -= 1



        ### now let's start the component detection ###

            edgeCount2 = len(D.edges())
            if edgeCount2 > edgeCount1:  # if edge has been inserted
                pebbleCount = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles']
                if pebbleCount <= l and pebbleCount > 0:  # if we have not more than l pebbles in u and v
                    # compute Reach(u,v) = Reach(u) U Reach(v)
                    reach_u = []
                    reach_v = []
                    for succ in nx.dfs_successors(D, source=u):
                        if succ != u and succ != v:
                            reach_u.append(succ)
                    for succ in nx.dfs_successors(D, source=v):
                        if succ != u and succ != v:
                            reach_v.append(succ)

                    # compute Reach(v)
                    reach_uv = reach_u + reach_v
                    pebbleCount = 0
                    for node in reach_uv:
                        pebbleCount += D.nodes[node]['pebbles']
                    if pebbleCount == 0:  # if any w in reach(u,v) has at least one pebble return empty set
                        queue = []
                        queue_memory = set() # to check if a node has ever put in queue before
                        '''nodes_outside_reach = list(D.nodes.keys())
                        for _node in nodes_outside_reach:
                            if _node in reach_uv:
                                nodes_outside_reach.remove(_node)
                        for edge in D.edges():
                            if edge[0] in nodes_outside_reach and edge[1] in reach_uv:
                                queue.append(edge[0])
                                queue_memory.add(edge[0])'''
                        reach_uv += [edge[0], edge[1]]      #Nicolas Vorschlag
                        for _node in reach_uv:
                            for pred in D.predecessors(_node):
                                if pred not in reach_uv:
                                    queue.append(pred)
                                    queue_memory.add(pred)
                        V_prime = reach_uv
                        while len(queue) > 0:
                            w = queue.pop(0)
                            print(f'queue-length: {len(queue)}')
                            reach_w = list({node for listing in nx.dfs_successors(D, source=w).values() for node in listing}) + [w]
                            while u in reach_w: reach_w.remove(u)
                            while v in reach_w: reach_w.remove(v)
                            pebbleCount = 0
                            for __node in reach_w:
                                if __node not in edge:  # check pebblecount in Reach(w) (without u and v)
                                    pebbleCount += D.nodes[__node]['pebbles']
                            if pebbleCount == 0:
                                V_prime += reach_w

                                for _node in V_prime:
                                    for pred in D.predecessors(_node):
                                        if pred not in V_prime and pred not in queue_memory:
                                            queue.append(pred)
                                            queue_memory.add(pred)
                                '''nodes_outside_reach = list(D.nodes.keys())  # enqueue all nodes with edges in reach_w
                                for _node in nodes_outside_reach:
                                    if _node in reach_w:
                                        nodes_outside_reach.remove(_node)'''
                                '''for edge in D.edges():
                                    if edge[0] in nodes_outside_reach and edge[1] in reach_w and edge[0] not in queue_memory:
                                        queue.append(edge[0])
                                        queue_memory.add(edge[0])'''
                        components.append(list(set(V_prime)))

                    '''if l == 0:
                        V_prime = D.nodes.keys()
                        V_prime.remove(edge[0])
                        V_prime.remove(edge[1])
                        components.append(V_prime)'''
    print(components)


            # jetzt habe ich zwar ne component aber weiß ich ob die component rigid ist oder nicht? doch: gibt steife komponenten aus

    # debug testrecke
    #print(f'number edges D: {D.number_of_edges()}')
    #print(f'number edges G: {G.number_of_edges()}')

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
    #print(f'edges: {G.edges()} type: {type(list(G.edges()))}, length: {len(G.edges())}')

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

    #print(G_a)
    print(f'Graph a) should be well-constraint. Here it is {pebblegame(G_a, 3, 3)}')

    #print(G)
    #print(pebblegame(G, 3, 3))
    #print(G_3)
    #print(pebblegame(G_3, 3, 3))

   # print(G_b)
    #print(f'Graph b) should be under-constraint. Here it is {pebblegame(G_b, 3, 3)}')
    print(component_detection_1(G_a, 3, 3))

    print(f'G_a reference edgelist:{[(1,2),(2,4),(2,4),(3,1),(3,1),(3,4),(4,3),(4,3),(4,1),(5,1),(5,1),(5,3),(6,3),(6,3),(6,3)]}')


'''reach_uv += [edge[0], edge[1]]
for _node in reach_uv:
    for pred in D.predecessors(_node):
        if pred not in reach_uv:
            queue.append(pred)
            queue_memory.add(pred)'''

