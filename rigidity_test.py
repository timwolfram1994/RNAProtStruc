import pebblegame as pg
import networkx as nx


# Complete Graph (K5):
e_K5 = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
G = nx.from_edgelist(e_K5)

# laman Graph
e_Laman = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (2, 4), (2, 5)]
G = nx.from_edgelist(e_Laman)
#pg.pebblegame(G, 2, 3)

# complete octaeder

e_oct = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
G = nx.from_edgelist(e_oct)
G_5 = pg.create5Ggraph(G)
pg.pebblegame(G_5,5,6)



