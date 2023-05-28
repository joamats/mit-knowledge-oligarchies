import pandas as pd
import networkx as nx

# read authors_info.csv
df = pd.read_csv('data_light/authors_info.csv')
G = nx.read_graphml(f"oligarchies/graphs/max_clique.graphml")

# get the number of nodes of the clique
print(len(G.nodes()))

# get the nodes of the clique
clique_nodes = G.nodes()

# merge the clique nodes with the authors_info.csv
clique_df = df[df['researcher_id'].isin(clique_nodes)]
print(clique_df.gender.value_counts(normalize=True))
print(clique_df.LMIC.value_counts(normalize=True))
print(clique_df.current_organization_id.value_counts()[:20])

# load authors_journals
df = pd.read_csv('data_light/authors_journals.csv')
df = df[df['journal.title'] != 'PLOS Medicine']

# get the publications of the clique
clique_pubs = df[df['researcher_id'].isin(clique_nodes)].pub_id.unique()
# get the number of publications of the clique
print(len(clique_pubs))
print(clique_pubs[:10])

# get authors information of the clique
clique_authors = df[df['researcher_id'].isin(clique_nodes)]
# save clique_authors
clique_authors.to_csv('data_light/clique_authors.csv', index=False)

# load pubs_info
df = pd.read_csv('data_light/pubs_info.csv')

# get the number of publications per year in the clique
print(df[df['pub_id'].isin(clique_pubs)].year.value_counts())
