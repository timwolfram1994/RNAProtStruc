import networkx as nx
import itertools


def pairwise(iterable):
    "s -> (s0, s1), (s1, s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def directed_dfs_edges(G, source=None, depth_limit=None):
    if not G.is_directed():
        raise ValueError("The graph must be directed for this function.")

    if source is None:
        nodes = G
    else:
        nodes = [source]

    visited = set()

    if depth_limit is None:
        depth_limit = len(G)

    for start in nodes:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, depth_limit, iter(G.successors(start)))]  # Only successors of the node
        while stack:
            parent, depth_now, children = stack[-1]
            try:
                child = next(children)
                if child not in visited:
                    yield parent, child
                    visited.add(child)
                    if depth_now > 1:
                        stack.append((child, depth_now - 1, iter(G.successors(child))))  # Only successors of the child
            except StopIteration:
                stack.pop()


if __name__ == '__main__':
    # Create a directed graph
    G = nx.MultiDiGraph()
    G.add_edges_from([(1, 2), (1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (6, 4)])

    # Use the modified function to perform directed DFS
    result = list(directed_dfs_edges(G, source=1))
    result2 = list(nx.dfs_edges(G, source=2))
    successors = nx.dfs_successors(G, source=1)

    # Print the result
    print(f'result with our selfmade traversal: {result}')
    print(f'result with inbuilt traversal: {result2}')
    print(f'successors: {successors}')

    a = 1
    b = a
    b = 2
    print(a)

    li = [1,2,3,4]
    print(li[0:3])



