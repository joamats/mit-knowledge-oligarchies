from node2vec import Node2Vec
import networkx as nx
import networkit as nk
import numpy as np
from tqdm import tqdm

def graph_measures(journal):

    print(f"\n{journal} Graph Measures")

    # Read graph from GraphML file
    G = nk.graphio.readGraph(f"graph_analysis/graphs/{journal}.graphml", nk.Format.GraphML)