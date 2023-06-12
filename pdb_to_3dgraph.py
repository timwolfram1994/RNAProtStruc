import matplotlib.pyplot as plt
import networkx as nx
import os
from Bio.PDB import PDBParser

filename = "2eso.pdb"
path = os.path.join(os.getcwd(),"pdb_samples", filename)

# Load the PDB file using BioPython's PDBParser
parser = PDBParser()
structure = parser.get_structure('protein', path)


# Create a NetworkX graph
G = nx.Graph()

# Iterate over the atoms in the structure
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                # Add nodes to the graph for each atom
                G.add_node(atom.get_id(), element=atom.get_name(), position=atom.get_coord())

# Iterate over the bonds in the structure
for model in structure:
    for chain in model:
        for residue in chain:
            for atom1 in residue:
                for atom2 in residue:
                    if atom1 != atom2:
                        # Add edges to the graph for connected atoms
                        G.add_edge(atom1.get_id(), atom2.get_id())

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw nodes
for node in G.nodes():
    x, y, z = G.nodes[node]['position']
    ax.scatter(x, y, z, color='red', s=50)

# Draw edges
for edge in G.edges():
    node1 = edge[0]
    node2 = edge[1]
    x1, y1, z1 = G.nodes[node1]['position']
    x2, y2, z2 = G.nodes[node2]['position']
    ax.plot([x1, x2], [y1, y2], [z1, z2], color='gray', alpha=0.5)

# Set plot options
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display the plot
plt.show()