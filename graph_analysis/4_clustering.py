import numpy as np
from gensim.models import KeyedVectors
import hdbscan
from tqdm import tqdm

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def get_clusters(journal):

    # Load the saved node2vec model
    model = KeyedVectors.load('graph_analysis/embeddings/JAMA')

    # Get the shape of the word vectors matrix
    embedding_matrix = model.wv.vectors

    clusterer = hdbscan.HDBSCAN(min_cluster_size=50)

    # fit the data
    clusterer.fit(embedding_matrix)

    labels = clusterer.labels_

    # get the number of clusters
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print(f"Number of clusters found: {n_clusters}")

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(50, 50), dpi=400) 

    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # plot noise points in black
            col = [0, 0, 0, 1]
        class_member_mask = (labels == k)
        xy = embedding_matrix[class_member_mask]
        ax.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col), markeredgecolor='k', markersize=14)
    ax.set_title(f"{journal} no. clusters found {n_clusters}")

    fig.savefig(f'graph_analysis/clusters/{journal}_hdb.png')

    # Get the clusters to save them
    # get the unique labels (excluding noise points)
    cluster_labels = np.unique(labels[labels != -1])

    # create an empty list to hold the cluster arrays
    clusters = []

    # loop through the cluster labels and extract the data points for each cluster
    for cluster_label in cluster_labels:
        cluster = embedding_matrix[labels == cluster_label]
        clusters.append(cluster)

    # save the clusters as a numpy array
    np.save(f"graph_analysis/clusters/{journal}.npy", np.array(clusters))


# Main

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    get_clusters(journal)


