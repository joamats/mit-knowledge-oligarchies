from node2vec import Node2Vec
import networkx as nx
import networkit as nk
import numpy as np
from tqdm import tqdm
import pandas as pd
import pickle

def cluster_measures(journal):

    #print(f"\n{journal} Cluster Measures")

    # Read cluster with pickle
    with open(f'graph_analysis/clusters/{journal}.pkl', 'rb') as f:
        clusters = pickle.load(f)

    # Load bc scores
    bc_scores = np.load(f"graph_analysis/measures/bc_scores/{journal}.npy")
    dc_scores = np.load(f"graph_analysis/measures/dc_scores/{journal}.npy")
    cc_scores = np.load(f"graph_analysis/measures/cc_scores/{journal}.npy")

    # Load LMICs
    df_lmic = pd.read_csv(f'graph_analysis/LMICs/{journal}_LMICs.csv')
    # ["HICs", "LMICs", "Unknown"]

    # get the indexes where the LMICs are
    hics = df_lmic[df_lmic.LMIC == 1].index
    lmics = df_lmic[df_lmic.LMIC == 2].index
    unknw = df_lmic[df_lmic.LMIC == 3].index

    # create empty dataframe to accomodate the average betweenness centrality score for each cluster, mean and std
    df = pd.DataFrame(columns=["total",
                               "LMICs", "LMICs_perc","HICs", "Unknown",
                               "Avg BC", "Avg DC", "Avg CC",
                               "Min BC", "Min DC", "Min CC",
                               "Max BC", "Max DC", "Max CC"])

    # iterate through the clusters
    for i, cluster in enumerate(clusters):

        nodes = [node for node in cluster]
        
        df.loc[i, "total"] = len(bc_scores[nodes])

        # create list from the indexes of the LMICs
        n_lmic = [node for node in nodes if node in lmics]
        df.loc[i, "LMICs"] = len(n_lmic)
        df.loc[i, "LMICs_perc"] = len(n_lmic) / len(bc_scores[nodes])
        df.loc[i, "HICs"] = len([node for node in nodes if node in hics])
        df.loc[i, "Unknown"] = len([node for node in nodes if node in unknw])

        # save the agg metrics for betweenness centrality score for the cluster
        df.loc[i, "Avg BC"] = np.mean(bc_scores[nodes])
        df.loc[i, "Avg DC"] = np.mean(dc_scores[nodes])
        df.loc[i, "Avg CC"] = np.mean(cc_scores[nodes])

        df.loc[i, "Min BC"] = np.min(bc_scores[nodes])
        df.loc[i, "Min DC"] = np.min(dc_scores[nodes])
        df.loc[i, "Min CC"] = np.min(cc_scores[nodes])
        
        df.loc[i, "Max BC"] = np.max(bc_scores[nodes])
        df.loc[i, "Max DC"] = np.max(dc_scores[nodes])
        df.loc[i, "Max CC"] = np.max(cc_scores[nodes])

    # save dataframe
    df.to_csv(f"graph_analysis/cluster_measures/{journal}.csv")

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    cluster_measures(journal)
