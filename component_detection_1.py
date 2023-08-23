import networkx as nx
import pebblegame_copy as pg
# import pdb_to_graph
import os


def pebblegame(G, k, l):
    # zu berichtigende Zeilen: 32
    # gibt reach nur direkted pfade aus?

    k = k  # evtl. redundant?
    l = l
    D = nx.MultiDiGraph()
    D.add_nodes_from(G)
    nx.set_node_attributes(D, k, "pebbles")
    for edge in G.edges():  # zufallsordnung wichtig, angabe der dozenten !!!
        if D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
            'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
            D.add_edge(edge[0], edge[1])
            D.nodes[edge[0]]['pebbles'] -= 1

        else:  # collect pebbles
            while D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles'] < l + 1:
                compare1 = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles']

                dfslist_u = list(nx.dfs_edges(D, edge[0]))  # depth first search from u
                for idx, _edge in enumerate(dfslist_u):  # u of edge is starting node
                    if edge[1] in _edge or edge[0] == _edge[1]:  # avoid taking pebble from u or v
                        continue
                    if D.nodes[_edge[1]]['pebbles'] > 0:  # first edge is (u, u+1)
                        D.nodes[_edge[1]]['pebbles'] -= 1  # take pebble from node
                        D.nodes[edge[0]]['pebbles'] += 1  # add pebble to starting node
                        # nun die Kanten umdrehen
                        for __edge in dfslist_u[
                                      0:idx + 1]:  # reverse the directions of the edges !!! hier berichtigen: tiefensuche könnte auch Knoten enthalten die außerhalb des direkten Pfades liegen
                            D.remove_edge(__edge[0], __edge[1])
                            D.add_edge(__edge[1], __edge[0])
                        break  # if we found a pebble we stop the dfs

                dfslist_v = list(nx.dfs_edges(D, edge[1]))  # depth fist search from v
                for idx, _edge in enumerate(dfslist_v):  # v of edge is starting node
                    if edge[0] in _edge or edge[1] == _edge[1]:  # avoid taking pebble from u or v
                        continue
                    if D.nodes[_edge[1]]['pebbles'] > 0:  # first edge is (u, u+1)
                        D.nodes[_edge[1]]['pebbles'] -= 1  # take pebble from node
                        D.nodes[edge[0]]['pebbles'] += 1  # add pebble to starting node
                        # nun die Kanten umdrehen
                        for __edge in dfslist_v[0:idx + 1]:  # reverse the directions of the edges
                            D.remove_edge(__edge[0], __edge[1])
                            D.add_edge(__edge[1], __edge[0])
                        break  # if we found a pebble we stop the dfs

                compare2 = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
                    'pebbles']  # break out of while loop if pebbles didn't change
                if compare1 == compare2:
                    break

            if D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
                'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
                D.add_edge(edge[0], edge[1])  # insert directed edge uv in D
                D.nodes[edge[0]]['pebbles'] -= 1

    # debug testrecke
    print(f'number edges D: {D.number_of_edges()}')
    print(f'number edges G: {G.number_of_edges()}')

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


def component_detection_1(G, k, l):
    k = k
    l = l
    D = nx.MultiDiGraph()
    D.add_nodes_from(G)
    nx.set_node_attributes(D, k, "pebbles")
    component_list = []

    for edge in G.edges():
        edgeCount1 = D.number_of_edges()

        if D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
            'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
            D.add_edge(edge[0], edge[1])
            D.nodes[edge[0]]['pebbles'] -= 1

        else:  # collect pebbles
            while D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles'] < l + 1:
                compare1 = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles']

                dfslist_u = list(nx.dfs_edges(D, edge[0]))  # depth first search from u
                for idx, _edge in enumerate(dfslist_u):  # u of edge is starting node
                    if edge[1] in _edge or edge[0] == _edge[1]:  # avoid taking pebble from u or v
                        continue
                    if D.nodes[_edge[1]]['pebbles'] > 0:  # first edge is (u, u+1)
                        D.nodes[_edge[1]]['pebbles'] -= 1  # take pebble from node
                        D.nodes[edge[0]]['pebbles'] += 1  # add pebble to starting node
                        # nun die Kanten umdrehen
                        for __edge in dfslist_u[0:idx + 1]:  # reverse the directions of the edges
                            D.remove_edge(__edge[0], __edge[1])
                            D.add_edge(__edge[1], __edge[0])
                        break  # if we found a pebble we stop the dfs

                dfslist_v = list(nx.dfs_edges(D, edge[1]))  # depth fist search from v
                for idx, _edge in enumerate(dfslist_v):  # v of edge is starting node
                    if edge[0] in _edge or edge[1] == _edge[1]:  # avoid taking pebble from u or v
                        continue
                    if D.nodes[_edge[1]]['pebbles'] > 0:  # first edge is (u, u+1)
                        D.nodes[_edge[1]]['pebbles'] -= 1  # take pebble from node
                        D.nodes[edge[0]]['pebbles'] += 1  # add pebble to starting node
                        # nun die Kanten umdrehen
                        for __edge in dfslist_v[0:idx + 1]:  # reverse the directions of the edges
                            D.remove_edge(__edge[0], __edge[1])
                            D.add_edge(__edge[1], __edge[0])
                        break  # if we found a pebble we stop the dfs

                compare2 = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
                    'pebbles']  # break out of while loop if pebbles didn't change
                if compare1 == compare2:
                    break

            if D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]][
                'pebbles'] >= l + 1:  # check whether u and v have enough pebbles
                D.add_edge(edge[0], edge[1])  # insert directed edge uv in D
                D.nodes[edge[0]]['pebbles'] -= 1

        edgeCount2 = D.number_of_edges()

        ### now let's start the component detection ###
        components = []

        if edgeCount2 > edgeCount1:  # if edge has been inserted
            pebbleCount = D.nodes[edge[0]]['pebbles'] + D.nodes[edge[1]]['pebbles']
            if pebbleCount <= l and pebbleCount > 0:  # if we have not more than l pebbles in u and v
                # compute Reach(u,v) = Reach(u) U Reach(v)
                reach_u = list(nx.dfs_successors(D, source=edge[0]).keys())  # compute Reach(u)
                reach_v = list(nx.dfs_successors(D, source=edge[1]).keys())  # compute Reach(v)
                reach_uv = reach_u + reach_v
                pebbleCount = 0
                for node in reach_uv:
                    pebbleCount += D.nodes[node]['pebbles']
                if pebbleCount == 0:  # if any w in reach(u,v) has at least one pebble return empty set
                    queue = []
                    nodes_outside_reach = list(D.nodes.keys())
                    for _node in nodes_outside_reach:
                        if _node in reach_uv:
                            nodes_outside_reach.remove(_node)
                    for edge in D.edges():
                        if edge[0] in nodes_outside_reach and edge[1] in reach_uv:
                            queue.append(edge[0])
                    while len(queue) > 0:
                        w = queue.pop(0)
                        reach_w = list(nx.dfs_successors(D, source=w).keys())
                        pebbleCount = 0
                        for __node in reach_w:
                            if __node not in edge:  # check pebblecount in reach w (without u and v)
                                pebbleCount += D.nodes[__node]['pebbles']
                        if pebbleCount == 0:
                            V_prime = reach_uv + reach_w
                            nodes_outside_reach = list(D.nodes.keys())  # enqueue all nodes with edges in reach_w
                            for _node in nodes_outside_reach:
                                if _node in reach_w:
                                    nodes_outside_reach.remove(_node)
                            for edge in D.edges():
                                if edge[0] in nodes_outside_reach and edge[1] in reach_w:
                                    queue.append(edge[0])
                            components.append(V_prime)

                if l == 0:
                    V_prime = D.nodes.keys()
                    V_prime.remove(edge[0])
                    V_prime.remove(edge[1])
                    components.append(V_prime)

            # jetzt habe ich zwar ne component aber weiß ich ob die component rigid ist oder nicht?

    # debug testrecke
    print(f'number edges D: {D.number_of_edges()}')
    print(f'number edges G: {G.number_of_edges()}')

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

    print(G)
    print(pebblegame(G, 3, 3))
    print(G_3)
    print(pebblegame(G_3, 3, 3))
    print(G_a)
    print(pebblegame(G_a, 3, 3))
    print(G_b)
    print(pebblegame(G_b, 3, 3))
    print(component_detection_1(G_a, 3, 3))
