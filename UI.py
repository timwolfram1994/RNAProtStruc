import os
import pebblegame as pg
import networkx as nx
import numpy as np
import pandas as pd
import PDB_to_Graphein as ptg
import generic_pebblegame



print("Please type command. \n",
      "basic rigidity test: b \n",
      "detection of rigid components: c \n")
procedure = input('>')

print("Please type command.\n",
      "rigidity test from edgelist: e \n",
      "rigidity test from pdb-file: p")
source = input('>')

print('please type path of your graph:')
path = input('>')

if source == 'e':
    fh = open(path, 'rb')
    G = nx.read_edgelist(fh)
elif source == 'p':
    G = ptg.pdb_to_graph(path)

if procedure == 'b':

    print('A k,l-pebble game will be run. Specifiy k:')
    k = int(input())
    print('Now please specify l:')
    l = int(input())
    # if we have a 5,6-pebblegame, we perform a 3D-rigidity test, so we have to multiply the edges by five
    if k == 5 and l == 6:
        G = pg.create5Ggraph(G)

    generic_pebblegame.generic_pebblegame(G, k, l)


elif procedure == 'c':

    print('A k,l-pebble game will be run. Specifiy k:')
    k = int(input())
    print('Now please specify l:')
    l = int(input())
    # if we have a 5,6-pebblegame, we perform a 3D-rigidity test, so we have to multiply the edges by five
    if k == 5 and l == 6:
        G = pg.create5Ggraph(G)

    components = pg.pebblegame(G, k, l)
    G = ptg.assign_components(G, components)
    df = ptg.print_attributes(G)
    df.to_csv(os.path.basename(path).split('.')[0] + '_attributes' + '.csv')
    comp_df = ptg.print_component_dataframe(components)
    comp_df.to_csv(os.path.basename(path).split('.')[0] + '_components' + '.csv')












