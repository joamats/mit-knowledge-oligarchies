from node2vec import Node2Vec
import networkx as nx
import networkit as nk
import numpy as np
from tqdm import tqdm
import pandas as pd
import pickle

def cluster_measures(journal):

    print(f"\n{journal} Cluster Measures")

    # Read cluster with pickle
    with open(f'graph_analysis/clusters/{journal}.pkl', 'rb') as f:
        clusters = pickle.load(f)

    print(f"Number of clusters: {len(clusters)}")

    # Load bc scores
    bc_scores = np.load(f"graph_analysis/bc_scores/{journal}.npy")[:500]
    print(f"Number of bc scores: {len(bc_scores)}")

    # create empty dataframe to accomodate the average betweenness centrality score for each cluster, mean and std
    df = pd.DataFrame(columns=["avg_bc", "std_bc", "median_bc", "min_bc", "max_bc", "q1_bc", "q3_bc"])

    # iterate through the clusters
    for i, cluster in enumerate(clusters):

        nodes = [node for node in cluster]
        cluster_bc_scores = bc_scores[nodes]

        # save the agg metrics for betweenness centrality score for the cluster
        df.loc[i, "avg_bc"] = np.mean(cluster_bc_scores)
        df.loc[i, "std_bc"] = np.std(cluster_bc_scores)
        df.loc[i, "median_bc"] = np.median(cluster_bc_scores)
        df.loc[i, "min_bc"] = np.min(cluster_bc_scores)
        df.loc[i, "max_bc"] = np.max(cluster_bc_scores)
        df.loc[i, "q1_bc"] = np.quantile(cluster_bc_scores, 0.25)
        df.loc[i, "q3_bc"] = np.quantile(cluster_bc_scores, 0.75)

    # save dataframe
    df.to_csv(f"graph_analysis/cluster_measures/{journal}.csv")

journal_names = ["BMJ"]

for journal in tqdm(journal_names):
    cluster_measures(journal)
