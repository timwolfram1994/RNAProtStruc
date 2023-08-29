import networkx as nx

# list of edges
if __name__ == "__main__":
        figure_3a = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"),
                     ("B", "D"), ("B", "D"), ("C", "D"), ("C", "D"), ("C", "D"),
                     ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]

        well_constraint = nx.MultiDiGraph(figure_3a)
        well_constraint.add_nodes_from(figure_3a, pebbles=5)

        # Change the amount of pebbles at node "D" to 4
        target_node = "D"
        new_pebbles_value = 4
        well_constraint.nodes[target_node]['pebbles'] = new_pebbles_value

        print(well_constraint.nodes[target_node])



