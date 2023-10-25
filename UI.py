import pebblegame as pg
import networkx as nx
import numpy as np
import pdb_to_graph as ptg
import helper_functions as hp
import pandas as pd

print("Please type command.\n",
      "rigidity test from edgelist: e \n",
      "rigidity test from pdb-file: p")

command = input('>')

if command == 'e':
    print('please type path of your graph:')
    path = input()
    print('A k,l-pebble game will be run. Specifiy k:')
    k = int(input())
    print('Now please specify l:')
    l = int(input())


    fh = open(path, 'rb')
    G = nx.read_edgelist(fh)
    G = pg.create5Ggraph(G)
    comp_mat = pg.pebblegame(G, k, l)
    hp.count_components(comp_mat)


if command == 'p':
    print('please type path of your pdb-file')
    path = input('>')

    G = ptg.pdb_to_graph(path)
    G = pg.create5Ggraph(G)
    comp_mat = pg.pebblegame(G, 5, 6)
    hp.count_components(comp_mat)

print('Do you wan\'t to save the matrix?\n',
      'yes: y, no: n')
save = input()
if save == 'y':
    outpath = input('please type your destination path: ')
    df = pd.DataFrame(comp_mat)
    df.to_csv(outpath, index=False)











