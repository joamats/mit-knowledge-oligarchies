import networkit as nk
import pandas as pd
import networkx as nx
from tqdm import tqdm


def compute_centrality_measures(journal):
    # Load the graph from the .graphml file
    G = nk.graphio.readGraph(f"oligarchies/graphs/{journal}.graphml", nk.Format.GraphML)

    # Compute centralities
    degree_centralities = nk.centrality.DegreeCentrality(G).run().scores()
    closeness_centralities = nk.centrality.ApproxBetweenness(G).run().scores()
    betweenness_centralities = nk.centrality.ApproxBetweenness(G).run().scores()


    # Create DataFrame to store the centrality measures
    centrality_df = pd.DataFrame({
        'Degree Centrality': degree_centralities,
        'Closeness Centrality': closeness_centralities,
        'Betweenness Centrality': betweenness_centralities
    })

    # Read graph in different way to get the nodes' names
    G = nx.read_graphml(f"oligarchies/graphs/{journal}.graphml")

    # Set the nodes as the index of the DataFrame
    centrality_df.index = G.nodes()

    # Save the DataFrame to a CSV file
    centrality_df.to_csv(f"oligarchies/centralities/{journal}.csv")


journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    print(journal)
    compute_centrality_measures(journal)