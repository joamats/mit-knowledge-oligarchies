import numpy as np
from gensim.models import KeyedVectors
from sklearn.manifold import TSNE
from tqdm import tqdm

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def create_tSNE(journal):

    # Load the saved node2vec model
    model = KeyedVectors.load(f"graph_analysis/embeddings/{journal}")

    # Get the shape of the word vectors matrix
    embedding_matrix = model.wv.vectors

    # create TSNE model
    tsne = TSNE(n_components=2)

    # Fit and transform the data
    vector_tsne = tsne.fit_transform(embedding_matrix)

    np.save(f"graph_analysis/tSNE/{journal}.npy", vector_tsne)

    # Plot the result
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(50, 50), dpi=400) 
    ax.set_title(f"tSNE {journal}")
    ax.scatter(vector_tsne[:, 0], vector_tsne[:, 1])
    fig.savefig(f'graph_analysis/tSNE/{journal}_tsne.png')

# Main

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    create_tSNE(journal)

