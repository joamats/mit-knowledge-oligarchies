import networkit as nk
import pandas as pd
import networkx as nx
from tqdm import tqdm


# Load the graph from the .graphml file
G = nk.graphio.readGraph(f"oligarchies/graphs/all.graphml", nk.Format.GraphML)

# Compute centralities
degree_centralities = nk.centrality.DegreeCentrality(G).run().scores()

# Create DataFrame to store the centrality measures
centrality_df = pd.DataFrame({
    'Degree Centrality': degree_centralities
})

# Read graph in different way to get the nodes' names
G = nx.read_graphml(f"oligarchies/graphs/all.graphml")

# Set the nodes as the index of the DataFrame
centrality_df.index = G.nodes()

# Save the DataFrame to a CSV file
centrality_df.to_csv(f"oligarchies/centralities/all.csv")
