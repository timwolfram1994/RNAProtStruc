import networkx as nx
import os
from biopandas.pdb import PandasPdb
import biopandas as bp
import MDAnalysis as mda
from MDAnalysis import analysis
from MDAnalysis.analysis import hbonds
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis
from proteingraph import read_pdb
import pickle


#from IPython.display import display
#import matplotlib.pyplot as plt

filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)

def pdb_to_graph_ver1(path):


    # Load the PDB file using Biopandas
    df = PandasPdb().read_pdb(path)

    # Create a NetworkX graph
    G = nx.Graph()

    # Iterate over the atoms in the DataFrame
    for i, row in df.df['ATOM'].iterrows():
        atom_serial = row['atom_number']
        atom_element = row['element_symbol']

        # Add nodes to the graph for each atom
        G.add_node(atom_serial, element=atom_element)

    # Calculate bond distances and add edges to the graph
    for i, row1 in df.df['ATOM'].iterrows():
        for j, row2 in df.df['ATOM'].iterrows():
            if i < j:  # Avoid duplicate pairs
                atom1_coords = row1[['x_coord', 'y_coord', 'z_coord']]
                atom2_coords = row2[['x_coord', 'y_coord', 'z_coord']]

                # Calculate the Euclidean distance between atoms
                distance = ((atom1_coords - atom2_coords) ** 2).sum() ** 0.5

                # Define a threshold for bond distance (adjust as needed)
                bond_threshold = 1.5

                # Determine bond type based on distance
                bond_type = 1  # Default to single bond
                if distance <= bond_threshold:
                    bond_type = 2  # Double bond

                # Add an edge to the graph if it's a bond
                if bond_type > 1:
                    atom1_serial = row1['atom_number']
                    atom2_serial = row2['atom_number']
                    G.add_edge(atom1_serial, atom2_serial, bond_type=bond_type)

    return G


def pdb_to_graph(path):

    ''' input: PDB-file
    returns: Graph '''

    # Load the PDB file using Biopandas
    df = PandasPdb().read_pdb(path)

    # Create a NetworkX graph
    G = nx.MultiGraph()

    # Iterate over the atoms in the DataFrame
    for i, row in df.df['ATOM'].iterrows():
        atom_serial = row['atom_number']
        atom_element = row['element_symbol']
        atom_coords = row[['x_coord', 'y_coord', 'z_coord']]

        # Add nodes to the graph for each atom
        G.add_node(atom_serial, element=atom_element, coords=atom_coords)

    # Iterate through atoms to identify covalent bonds and add edges to the graph
    for idx, atom1 in enumerate(G.nodes()):
        for atom2 in list(G.nodes)[idx+1:-1]:
            if atom1 != atom2:
                coords1 = G.nodes[atom1]['coords']
                coords2 = G.nodes[atom2]['coords']
                distance = sum((coords1 - coords2) ** 2) ** 0.5

                # Define a threshold for bond length (e.g., for C-C bonds)
                threshold = 1.54  # Adjust as needed
                threshold_CN_double = 1.30

                if 0 < distance < threshold:
                    G.add_edge(atom1, atom2)
                if 0 < distance < threshold_CN_double:
                    G.add_edge(atom1, atom2)



    return G

def count_doubles(G):
    counter = 0
    for i in G.edges:
        if i[2] == 2:
            counter += 1
    return counter


def pdb_to_graph_extended(path):

    '''considers H-Bonds and Van der waals forces additionally'''

    # Load the PDB file using Biopandas
    df = PandasPdb().read_pdb(path)

    # Create a NetworkX graph
    G = nx.Graph()

    # Iterate over the atoms in the DataFrame
    for i, row in df.df['ATOM'].iterrows():
        atom_serial = row['atom_number']
        atom_element = row['element_symbol']

        # Add nodes to the graph for each atom
        G.add_node(atom_serial, element=atom_element)

    # Load the PDB file using MDAnalysis
    u = mda.Universe(path)

    # Calculate hydrogen bonds using MDAnalysis
    Hbonds = HydrogenBondAnalysis(u, between=['protein', 'protein'])

    # Add edges to the graph for hydrogen bonds
    for hb in Hbonds.results.hbonds:
        atom1_serial = hb[1]
        atom2_serial = hb[3]
        G.add_edge(atom1_serial, atom2_serial, bond_type='H-bond')

    # Calculate van der Waals interactions using MDAnalysis
    vdw_pairs = mda.analysis.contacts.Contacts(u, 'protein and not name H*',
                                               method='vdw', radius=3.5)

    # Add edges to the graph for van der Waals interactions
    for i, j in vdw_pairs.contact_pairs:
        atom1_serial = i + 1
        atom2_serial = j + 1
        G.add_edge(atom1_serial, atom2_serial, bond_type='Van-der-Waals')

    return G

def dump_graphml(G, filename, targetfolder="graphs"):

    outpath = os.path.join(os.getcwd(), targetfolder, filename+".edgelist")
    fh = open(outpath, "wb")
    nx.write_edgelist(G, fh)
    fh = open(outpath, "rb")
    graph = nx.read_edgelist(outpath)
    fh.close()
    print(graph)
    outpath = os.path.join(os.getcwd(), targetfolder, filename + ".graphml")
    nx.write_graphml_lxml(graph, outpath)
    print(f"created edgelist and graphml with {len(list(graph.nodes))} nodes and {len(list(graph.edges))} edges")





# Draw the graph
'''pos = nx.spring_layout(G)  # Positions for all nodes
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
nx.draw_networkx_edges(G, pos, edge_color='gray')
nx.draw_networkx_labels(G, pos)

# Show the graph
plt.axis('off')
plt.show()
'''

if __name__ == '__main__':

    filename = "2mgo.pdb"  #"alt: 2eso.pdb", "hiv1_homology_model.pdb"
    path = os.path.join(os.getcwd(), "pdb_samples", filename)
    #testGraph = nx.complete_graph(5)
    oxy = pdb_to_graph(path)
    dump_graphml(oxy, "2mgo")



   # G = pdb_to_graph(path)
    '''e_K5 = [(1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)]
    G = nx.from_edgelist(e_K5)'''

    '''with open("graphs/outgraph.pickle", 'wb') as pickle_file:
        pickle.dump(G, pickle_file)'''

    '''counter = 0
    for i in G.edges:
        if i[2] == 2:
            counter += 1'''

    #G2 = pdb_to_graph_extended(path)

    #G = read_pdb(path)


    #print(f'Number of Doublebonds:{count_doubles(G)}')







