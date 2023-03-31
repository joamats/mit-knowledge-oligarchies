from node2vec import Node2Vec
import networkx as nx
import networkit as nk
import networkx.algorithms.community as nx_comm
import numpy as np
from tqdm import tqdm

def graph_measures(journal):

    print(f"\n{journal} Graph Measures")

    # Read graph from GraphML file
    G = nk.graphio.readGraph(f"graph_analysis/graphs/{journal}.graphml", nk.Format.GraphML)

    # Compute clustering coefficient
    cc = nk.globals.clustering(G)

    # Compute betweenness centrality
    bc = nk.centrality.Betweenness(G)
    bc_scores = bc.run().scores()

    # save the betweenness centrality scores
    np.save(f"graph_analysis/bc_scores/{journal}.npy", bc_scores)

    # Compute the average betweenness centrality of the whole graph
    avg_bc = np.mean(list(bc_scores))
    std_bc = np.std(list(bc_scores))

    G = nx.read_graphml(f"graph_analysis/graphs/{journal}.graphml")

    mod = nx_comm.modularity(G, nx_comm.label_propagation_communities(G))


    with open(f"graph_analysis/measures/{journal}.txt", "w") as f:
        print(f"Clustering coefficient: {cc:.3f}", file=f)
        print(f"Avg BC of the whole graph: {avg_bc:.3f}", file=f)
        print(f"Std BC of the whole graph: {std_bc:.3f}", file=f)
        print(f"Modularity: {mod:.3f}", file=f)

# Main

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    graph_measures(journal)