from graphein.protein.visualisation import plotly_protein_structure_graph
import PDB_to_Graphein as pdg

path = 'pdb_samples/2mgo.pdb'

G = pdg.pdb_to_graph(path, only_covalent=False)
comp = pdg.find_components(G)
G = pdg.assign_components(G, comp)


#attr_df = pdg.print_attributes(G)

#comp_df = pdg.print_component_dataframe(comp)



p = plotly_protein_structure_graph(
        G,
        colour_edges_by="component",
        colour_nodes_by="component",
        label_node_ids=False,
        plot_title="Peptide backbone graph. Nodes coloured by components",
        node_size_multiplier=1
    )
p.show()


#print(nx.get_edge_attributes(hiv1,'component'))
#print(nx.get_node_attributes(hiv1, "component"))


