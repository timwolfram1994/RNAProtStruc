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

'''22.09. Task: erstelle Dataframe oder PDB mit componente für jeden Knoten
visualisiere Komponenten für Kanten und evtl. Knoten
weitere Tasks: Disulfitbrücken, H-Brücken, Van-Der-Waals-Brücken'''



params_to_change = {"granularity": "atom"}


#oxy = pg.create5Ggraph(oxy)
#pg.pebblegame(oxy,5,6)

def sort_dict(original_dict):
    # Extract the values and sort them
    sorted_values = sorted(set(original_dict.values()))

    # Create a mapping from the original values to their sorted order
    value_to_order = {value: order for order, value in enumerate(sorted_values)}

    # Create a new dictionary with values replaced by their sorted order
    translated_dict = {key: value_to_order[value] for key, value in original_dict.items()}

    # Print the translated dictionary
    return translated_dict

def pdb_to_graph(path, only_covalent=True):

    '''uses graphein to convert PDB-file to Graph'''
    # decide if we construct edges only with covalent bonds or consider sidechain-interactions
    if only_covalent == True:
        params_to_change = {"granularity": "atom", "edge_construction_functions": [add_atomic_edges]}
    else:
        params_to_change = {"granularity": "atom", "edge_construction_functions": [
            add_hydrogen_bond_interactions,
            add_aromatic_interactions,
            add_disulfide_interactions,
            add_ionic_interactions,
            add_atomic_edges
        ],
                     "dssp_config": gp.DSSPConfig()
                     }

    config = ProteinGraphConfig(**params_to_change)
    G = construct_graph(config=config, path=path)

    return G



def load_and_show(path):

    params_to_change = {"granularity": "atom", "edge_construction_functions": [add_atomic_edges]}
    config = ProteinGraphConfig(**params_to_change)
    G = construct_graph(config=config, path=path)
    print(G)

    p = plotly_protein_structure_graph(
        G,
        colour_edges_by="kind",
        colour_nodes_by="degree",
        label_node_ids=False,
        plot_title="Peptide backbone graph. Nodes coloured by degree.",
        node_size_multiplier=1
    )
    p.show()
    return G

def load_and_pebble(path):

    '''uses Graphein to convert PDB-File to networkX Graph. Then performs 5,6-Pebblegame.'''

    params_to_change = {"granularity": "atom", "edge_construction_functions": [add_atomic_edges]}
    config = ProteinGraphConfig(**params_to_change)
    G = construct_graph(config=config, path=path)
    print(G)
    G = pg.create5Ggraph(G)
    component_list = pg.pebblegame(G,5,6)

    # Open a text file in write mode and export the list
    with open(os.path.basename(path).split('.')[0] + '.txt', 'w') as file:
        for item in component_list:
            file.write(str(item) + '\n')

    return component_list


def assign_components(G, components):
    '''assigns components to nodes and edges'''
    components = components

    for com in components:
        if len(com) == 1:
            components.remove(com)
    print(len(components))

    nodes = list(G.nodes)
    d = {}
    for node in nodes:
        for idx, c in enumerate(components):
            for e in c:
                if node in e:
                    if node in d:
                        if d[node] == 0:
                            d[node] = idx + 1
                            break
                        elif len(c) > len(components[d[node] - 1]):
                            d[node] = idx + 1
                        break  # stop bcs nodes appear more often in same components
                    else:
                        d[node] = 0

    d = sort_dict(d)
    nx.set_node_attributes(G, d, "component")

    # Here we want to assign to each edge its component. If node is not in component we assign 0 to it.
    edges = list(G.edges)
    d = {}
    for edge in edges:
        for idx, c in enumerate(components):
            if edge in d:
                if edge in c:
                    d[edge] = idx + 1  # die größeren komponenten sind weiter rechts
            else:
                d[edge] = 0

    d = sort_dict(d)
    nx.set_edge_attributes(G, d, name="component")

    return G



def print_attributes(G):

    # Get the node attributes as a dictionary
    node_attributes = dict(G.nodes(data=True))

    # Convert the dictionary to a Pandas DataFrame
    df = pd.DataFrame.from_dict(node_attributes, orient='index')
    return df




if __name__ == "__main__":

    path = "pdb_samples/2mgo.pdb"
    #G = load_and_show(path)
    components = load_and_pebble(path)
    G = pdb_to_graph(path, only_covalent=True)
    G = assign_components(G, components)
    df = print_attributes(G)
    df.to_csv('node_attributes/' + os.path.basename(path).split('.')[0] +'.csv', index=False)

    # Print node attributes
    '''for node in G.nodes():
        attributes = G.nodes[node]
        print(f"Node {node} attributes: {attributes}")'''


