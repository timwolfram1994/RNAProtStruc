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
