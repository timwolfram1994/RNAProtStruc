import json
import PDB_to_Graphein as pdg

path = "../pdb_samples/7vdn_Myoglobin_SpermWhale_CrystalStructure.pdb"
G = pdg.pdb_to_graph(path, only_covalent=False)
components = pdg.find_components(G)

with open("../components_json/myo.json", "w") as outfile:
    json.dump(components, outfile)