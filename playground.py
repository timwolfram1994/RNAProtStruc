import networkx as nx

# list of edges
if __name__ == "__main__":

        test = [("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "E"), ("B", "D"), ("B", "D"), ("C", "D"),
        ("C", "D"), ("C", "D"),
        ("C", "E"), ("C", "F"), ("C", "F"), ("C", "F")]

        multigraph1G = nx.MultiDiGraph(test)
        print(multigraph1G.edges)

        print("after: ")
        counter = 0
        for edge in test:
                if "A" in edge:
                        print("found :",edge)


        # shortest_path = [("A","C"),("C","D")]
        # for edge in shortest_path:
        # #         while edge in multigraph1G.edges:
        # #                 multigraph1G.remove_edge("A","C")
        # #                 multigraph1G.add_edge("C","A")
        # #                 counter +=1
        # #
        # #         print(multigraph1G.edges)
        # #         print("edges replace :", counter)


