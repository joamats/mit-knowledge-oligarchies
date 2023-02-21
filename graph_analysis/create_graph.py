import pandas as pd
import networkx as nx
import itertools
from tqdm import tqdm


def create_graph(df_all, journal):

    df = df_all[df_all['journal.title'] == journal]

    # Group researchers per publication
    groups = df.groupby('pub_id')['researcher_id'].apply(list)

    # create a list of all pairs of authors that have co-authored a paper
    coauthors = []
    for group in tqdm(groups):
        for pair in itertools.combinations(group, 2):
            coauthors.append(pair)

    # create the graph
    G = nx.Graph()

    # add the nodes
    for author in tqdm(df['researcher_id'].unique()):
        G.add_node(author)

    # add the edges
    G.add_edges_from(coauthors)

    print(journal)
    print(G)

    nx.write_graphml(G, f"graph_analysis/graphs/{journal}.graphml")


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
    create_graph(df, journal)
