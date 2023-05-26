import pandas as pd
import networkx as nx
import itertools
from tqdm import tqdm

# Function to create a graph with weighted edges per Journal
def create_weight_graph(df_all, journal):
    df = df_all[df_all['journal.title'] == journal]

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

    print(journal)
    print(G)

    nx.write_graphml(G, f"oligarchies/graphs/{journal}.graphml")


# Main
df_raw = pd.read_csv('data_light/authors_journals.csv')[['pub_id', 'researcher_id', 'journal.title']]

# Remove repeated authors within the same paper
df = df_raw.drop_duplicates()
print(f"Removed {len(df_raw) - len(df)} repeated entries")

# Simplify Journals Titles
df['journal.title'].replace({'The BMJ':'BMJ',
                             'The Lancet':'Lancet',
                             'New England Journal of Medicine':'NEJM',
                             'Nature Medicine':'Nature',
                             'PLOS Medicine':'PLOS'},
                             inplace=True)

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in journal_names:
    create_weight_graph(df, journal)
