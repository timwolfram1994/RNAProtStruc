import networkx as nx
import os
from biopandas.pdb import PandasPdb
import biopandas as bp
import MDAnalysis as mda
from MDAnalysis import analysis
from MDAnalysis.analysis import hbonds
from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis

#from IPython.display import display
#import matplotlib.pyplot as plt

filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)



def pdb_to_graph(path):
    # Load the PDB file using Biopandas
    df = PandasPdb().read_pdb(path)

    # Create a NetworkX graph
    G = nx.MultiGraph()

    # Iterate over the atoms in the DataFrame
    for i, row in df.df['ATOM'].iterrows():
        atom_serial = row['atom_number']
        atom_element = row['element_symbol']

        # Add nodes to the graph for each atom
        G.add_node(atom_serial, element=atom_element, pos=(row['x_coord'], row['y_coord'], row['z_coord']))

        # Add edges to the graph between adjacent atoms in the residue
        residue_id = row['residue_number']
        chain_id = row['chain_id']

        if i > 0:
            prev_row = df.df['ATOM'].iloc[i - 1]
            prev_residue_id = prev_row['residue_number']
            prev_chain_id = prev_row['chain_id']

            if (residue_id == prev_residue_id) and (chain_id == prev_chain_id):
                prev_atom_serial = prev_row['atom_number']

                # Calculate bond type based on interatomic distance
                distance = ((row['x_coord'] - prev_row['x_coord']) ** 2 +
                            (row['y_coord'] - prev_row['y_coord']) ** 2 +
                            (row['z_coord'] - prev_row['z_coord']) ** 2) ** 0.5

                bond_type = 1
                if distance <= 1.5:  # Adjust this threshold for your specific case
                    bond_type = 2

                G.add_edge(atom_serial, prev_atom_serial, bond_type)
    return G

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

    filename = "2eso.pdb"
    path = os.path.join(os.getcwd(), "pdb_samples", filename)

    G = pdb_to_graph(path)

    counter = 0
    for i in G.edges:
        if i[2] == 2:
            counter += 1

    #G2 = pdb_to_graph_extended(path)

    print(G.edges()) # irgendwas ist komisch mit dem outputgraphen. es scheint, als ob nicht alle atome als atome miteinander verbunden wurden
                     # es sieht wie eine große perlenkette aus
                    # vermutlich verbindet der code von chatGPT nur die nachfolgenden Atome in der PDB-Tabelle, aber man müsste
                    # alle Abstände berechnen







