from Bio.PDB.PDBParser import PDBParser
import networkx as nx

pdb_file = open("pdb_samples/1ubq.pdb")

parse_protein = PDBParser(PERMISSIVE=True, get_header=False, structure_builder=None, QUIET=False)
structure_ubiquitin = parse_protein.get_structure("test_ubi", pdb_file)
ubi_size = nx.path_graph(76)
ubi_graph = nx.Graph()
ubi_graph.add_notes_from(ubi_size)
