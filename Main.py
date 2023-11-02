import os
import graphein
import pandas as pd
import networkx as nx
import pebblegame as pg
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.graphs import construct_graph
from graphein.protein.config import ProteinGraphConfig
from graphein.protein.edges.atomic import add_atomic_edges
import logging
import networkx as nx
import matplotlib.pyplot as plt
import graphein.protein as gp
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("graphein").setLevel(logging.INFO)
from graphein.protein.config import ProteinGraphConfig
from graphein.protein.graphs import construct_graph
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.edges.atomic import add_atomic_edges
from graphein.protein.edges.distance import add_hydrogen_bond_interactions
from graphein.protein.edges.distance import add_aromatic_interactions
from graphein.protein.edges.distance import add_disulfide_interactions
from graphein.protein.edges.distance import add_ionic_interactions
import PDB_to_Graphein as pdg


### hiv1 Atom-Level with intramolecular bindings

path = 'pdb_samples/hiv1_homology_model.pdb'

hiv1 = pdg.pdb_to_graph(path, only_covalent=False)
comp = pdg.find_components(hiv1, path)
hiv1 = pdg.assign_components(hiv1, comp)
df = pdg.print_attributes(hiv1)
df.to_csv('node_attributes/hiv1_intra.csv')



p = plotly_protein_structure_graph(
        hiv1,
        colour_edges_by="component",
        colour_nodes_by="component",
        label_node_ids=False,
        plot_title="Peptide backbone graph. Nodes coloured by components",
        node_size_multiplier=1
    )
p.show()


#print(nx.get_edge_attributes(hiv1,'component'))
print(nx.get_node_attributes(hiv1, "component"))


