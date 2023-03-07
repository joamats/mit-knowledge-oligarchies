from node2vec import Node2Vec
import networkx as nx
import numpy as np
from tqdm import tqdm

def graph_measures(journal):

    print(f"\n{journal} Graph Measures")

    G = nx.read_graphml(f"graph_analysis/graphs/{journal}.graphml")
    # Compute the clustering coefficient
    cc = nx.average_clustering(G)

    print(f"Clustering coefficient: {cc:.3f}")

    # Compute the betweenness centrality
    bc = nx.betweenness_centrality(G)

    # Compute the average betweenness centrality of the whole graph
    avg_bc = np.mean(list(bc.values()))

    # Compute the standard deviation of the betweenness centralities of the whole graph --> Takes too long
    std_bc = np.std(list(bc.values()))

    print(f"Avg BC of the whole graph: {avg_bc:.3f}")
    print(f"Std BC of the whole graph: {std_bc:.3f}")


# Main

journal_names = ["BMJ"]#, "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    graph_measures(journal)