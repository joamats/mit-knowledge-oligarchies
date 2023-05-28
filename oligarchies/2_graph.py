import pandas as pd
import networkx as nx
import itertools
from tqdm import tqdm

# Read data_clean
df = pd.read_csv("data_light/data_clean.csv")

# Group researchers per publication
groups = df.groupby('pub_id')['researcher_id'].apply(list)

# create a dictionary to store the collaboration count for each pair of authors
collaboration_count = {}

# count the collaborations among authors
for group in groups:
    for pair in itertools.combinations(group, 2):
        if pair in collaboration_count:
            collaboration_count[pair] += 1
        else:
            collaboration_count[pair] = 1

# create the graph
G = nx.Graph()

# add the nodes
for author in df['researcher_id'].unique():
    G.add_node(author)

# add the weighted edges
for pair, weight in collaboration_count.items():
    author1, author2 = pair
    G.add_edge(author1, author2, weight=weight)

# no edges and nodes
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

nx.write_graphml(G, f"oligarchies/graphs/all.graphml")

