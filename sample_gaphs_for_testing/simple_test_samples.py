import networkx as nx

'''Samples for Testing of the generic- and the component pebble game'''

'''01. well-constraint-Beispiel (figure_3a) aus Li-Streinu-Paper für 3,3 Pebblegame:'''
sample01 = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
            ("C", "D"),
            ("C", "D"), ("C", "D"),
            ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]
sample01_graph = nx.MultiDiGraph(sample01)

'''02. under-constraint-Beispiel (figure_3b) aus Li-Streinu-Paper für 3,3 Pebblegame:'''
sample02 = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"),
            ("C", "D"), ("C", "D"), ("C", "D"),
            ("C", "E"), ("C", "F"), ("C", "F",)]
sample02_graph = nx.MultiDiGraph(sample02)

'''03. well-constraint-Beispiel (Laman-Graph: "Moser spindle") für 2,3 Pebble Game'''
sample03 = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("B", "D"), ("D", "E"), ("D", "F"), ("E", "F"),
            ("E", "G"), ("F", "G"),
            ("G", "A")]
sample03_graph = nx.from_edgelist(sample03)

'''04. over-constrained-Beispiel für 2,3 Pebble Game'''
sample04 = [(0, 1), (0, 8), (0, 9), (0, 11), (1, 7), (1, 8), (1, 10), (1, 11), (1, 13), (2, 3), (2, 7),
            (2, 8), (2, 14), (3, 6), (3, 14), (4, 5), (4, 8), (4, 9), (4, 11), (4, 12), (5, 6), (5, 7),
            (5, 9), (5, 12), (5, 13), (6, 13), (6, 14), (7, 12), (7, 14), (8, 12), (8, 13), (8, 14), (9, 10),
            (9, 12), (10, 11)]
sample04_graph = nx.from_edgelist(sample04)

'''05. under-constrained-Beispiel für 2,3 Pebble Game'''
sample05 = [(0, 6), (0, 11), (0, 12), (0, 14), (1, 6), (1, 7), (1, 8), (1, 9), (2, 12), (3, 6), (3, 7),
            (3, 10), (4, 5), (4, 7), (4, 12), (4, 14), (5, 8), (7, 11), (7, 13), (9, 10), (9, 11), (9, 13),
            (10, 12), (12, 14), (13, 14)]

sample05_graph = nx.from_edgelist(sample05)

'''06. Other-Beispiel für 2,3 Pebble Game'''
sample06 = [(0, 4), (0, 6), (0, 11), (0, 13), (1, 4), (1, 5), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (2, 3),
            (3, 5), (3, 7), (3, 13), (4, 5), (4, 8), (4, 11), (5, 9), (5, 10), (5, 13), (6, 10), (6, 11), (6, 14),
            (7, 8), (7, 10), (7, 14), (8, 9), (8, 11), (9, 12), (11, 13), (12, 13)]
sample06_graph = nx.from_edgelist(sample06)

'''07. well-constraint-Beispiel (Laman-Graph mit 8 Knoten) für 2,3 Pebble Game'''
sample07 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"), ("A", "G"), ("B", "H"), ("C", "H"),
            ("D", "H"), ("E", "G"), ("F", "G"), ("G", "H")]
sample07_graph = nx.from_edgelist(sample07)

'''08. under-constraint-Beispiel (test-sample No 07 mit zusätzlichem Knoten und einzelner Kante zu diesem) für 2,3 Pebble Game'''
sample08 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"), ("A", "G"), ("B", "H"), ("C", "H"),
            ("D", "H"), ("E", "G"), ("F", "G"), ("G", "H"),("A","I")]
sample08_graph = nx.from_edgelist(sample08)


'''09. well-constraint-Beispiel (test-sample No 08 mit zusätzlicher Kante zu Knoten "I") für 2,3 Pebble Game'''
sample09 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"), ("A", "G"), ("B", "H"), ("C", "H"),
            ("D", "H"), ("E", "G"), ("F", "G"), ("G", "H"),("A","I"),("B","I")]
sample09_graph = nx.from_edgelist(sample09)

'''10. over-constraint-Beispiel (test-sample No 09 mit zusätzlicher Kante) für 2,3 Pebble Game'''
sample10 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A"), ("A", "G"), ("B", "H"), ("C", "H"),
            ("D", "H"), ("E", "G"), ("F", "G"), ("G", "H"),("A","I"),("B","I"),("C","I")]
sample10_graph = nx.from_edgelist(sample10)

'''11. under-constraint-Beispiel (test-sample aus 3 seperaten Komponenten) für 2,3 Pebble Game'''
sample11 = [("A", "B"), ("B", "C"), ("C", "D"),("A","C"),("B","D"), ("D", "E"), ("E", "F"), ("D", "F"), ("D", "G"), ("F", "G"), ("C", "J"),
            ("G", "H"), ("J", "H"), ("H", "I"), ("I", "J")]
sample11_graph = nx.from_edgelist(sample11)

# Define the vertices of the tetrahedron with explicit positions

sample12_graph = nx.Graph()

sample12_graph.add_nodes_from([

    ('A', {"pos": (1, 1, 1)}),
    ('B', {"pos": (1, -1, -1)}),
    ('C', {"pos": (-1, 1, -1)}),
    ('D', {"pos": (-1, -1, 1)}),

])

# Define the edges of the tetrahedron
edges = [('A', 'B'), ('A', 'C'), ('A', 'D'),
         ('B', 'C'), ('B', 'D'),
         ('C', 'D')]

# Add edges to the graph
sample12_graph.add_edges_from(edges)

print(sample12_graph)

