import graphein
import networkx as nx
import pebblegame as pg
from graphein.protein.visualisation import plotly_protein_structure_graph
from graphein.protein.graphs import construct_graph
from graphein.protein.config import ProteinGraphConfig
from graphein.protein.edges.atomic import add_atomic_edges

'''22.09. Task: erstelle Dataframe oder PDB mit componente für jeden Knoten
visualisiere Komponenten für Kanten und evtl. Knoten
weitere Tasks: Disulfitbrücken, H-Brücken, Van-Der-Waals-Brücken'''



params_to_change = {"granularity": "atom"}


#oxy = pg.create5Ggraph(oxy)
#pg.pebblegame(oxy,5,6)

def pdb_to_graph(path):

    '''uses graphein to convert PDB-file to Graph'''
    params_to_change = {"granularity": "atom", "edge_construction_functions": [add_atomic_edges]}
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
    return component_list

def show_components(path):

    components_list = load_and_pebble(path)


    params_to_change = {"granularity": "atom", "edge_construction_functions": [add_atomic_edges]}
    config = ProteinGraphConfig(**params_to_change)
    G1 = construct_graph(config=config, path=path)
    print(G1)
    G = pg.create5Ggraph(G1)
    comp = pg.pebblegame(G, 5, 6)
    for node in G1.nodes:
        G1.nodes[node]['component'] = 0
    for node in G1.nodes:
        for c in comp:
            if len(c) > 2:
                for e in c:
                    if node in e:
                        G1.nodes[node]['component'] = 1
                        break

    p = plotly_protein_structure_graph(
        G1,
        colour_edges_by="kind",
        colour_nodes_by="component",
        label_node_ids=False,
        plot_title="Peptide backbone graph. Nodes coloured by degree.",
        node_size_multiplier=1
    )
    p.show()
    return G1




if __name__ == "__main__":

    path = "pdb_samples/2mgo.pdb"
    #G = load_and_show(path)
    #load_and_pebble(path)
    #G = show_components(path)


