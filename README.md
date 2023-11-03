# Detection of rigid Components in Graphs applied to Proteins

Project on rigidity in RNA and protein structures for Advanced Methods in Bioinformatics course

Thank you for using our little pebble and component-detection game tool!

We designed it to determine rigid components in proteins and other graphs.
The algorithm for the pabblegame/component-detection is based on the research-paper "Pebble game algorithms and sparse graphs"
by Lee and Streinu

Additionally we established a pipeline to detect rigid components in Proteins using the graphein-library.

To just run a basic pebblegame you can use the function in generic_pebblegame.py.
To run a component detection use the functions in pebblegame.py

Functions wrapping the rigid-component-detection and Protein-Graph building and visualization you can find in PDB_to_Grphein.py

# A little introduction to the main functions of PDB_to_Graphein.py:

pdb_to_graph(path, only_covalent=True, gran="atom")

- output: networkX MultiGraph

- loads PDB-file and converts to graph
- setting only_covalent to False takes sidechain interactions such as H-bond or ionic interactions into account and makes them to edges
- gran="atom" sets the atoms of the Protein to nodes. Change to gran="centroid" to set aminoacids as nodes.

find_components(G, k=5, l=6)

- output: List of components as sets containing the edges as frozen sets

- performs k,l-pebblegame-based detection of rigid components
- default k=5 and l=6 to perform a k,l-pebblegame for 3D protein Graphs

assign_components(G, components)

- output: netwokX Multigraph with node-attibute component based on input components-list

- it makes only sense to use the components list as input which is generated based on the same graph as input of this function

print_attributes(G)

- output: pandas dataframe with the node attributes

print_component_dataframe(component_list):

- output: pandas dataframe with components as index and a column with nodes and one with edges contained in each component


## Example Pipeline to perform a Component-Detection based on a PDB-File

from graphein.protein.visualisation import plotly_protein_structure_graph

import PDB_to_Graphein as pdg

path = 'pdb_samples/2mgo.pdb'

G = pdg.pdb_to_graph(path, only_covalent=False, gran="atom")

comp = pdg.find_components(G)

G = pdg.assign_components(G, comp)

attr_df = pdg.print_attributes(G)

comp_df = pdg.print_component_dataframe(comp)




  



