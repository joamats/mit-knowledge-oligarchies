from node2vec import Node2Vec
import networkx as nx
import numpy as np
import gensim

def create_embedding(journal):


    G = nx.read_graphml(f"graph_analysis/graphs/{journal}.graphml")

    # Create a Node2Vec object with 64-dimensional embeddings
    node2vec = Node2Vec(G, dimensions=256)

    # Learn node embeddings using the node2vec.fit() method
    model = node2vec.fit(window=10, min_count=1)

    print(journal)

    # Save model
    model.save(f"graph_analysis/embeddings/{journal}")

# Main

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in journal_names:
    create_embedding(journal)
