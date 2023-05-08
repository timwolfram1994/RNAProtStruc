import networkx as nx
from Bio.PDB import PDBParser

# Instantiate a PDB parser
parser = PDBParser()

# Parse the PDB file
structure = parser.get_structure('example', 'example.pdb')

# Create a graph
G = nx.Graph()

# Iterate over all atoms in all models in the structure
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                # Add nodes to the graph for each atom
                G.add_node(atom.get_serial_number(), element=atom.element)

                # Add edges to the graph between adjacent atoms in the residue
                if residue.get_resname() not in ['HOH', 'WAT']: # exclude water molecules
                    for neighbor in residue.get_unpacked_list():
                        if atom - neighbor <= 5.0:
                            G.add_edge(atom.get_serial_number(), neighbor.get_serial_number())

print(nx.info(G))
