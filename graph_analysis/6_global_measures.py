import pandas as pd
import networkit as nk
import numpy as np
from tqdm import tqdm

def graph_measures(journal):

    print(f"\n{journal} Graph Measures")

    # Read graph from GraphML file
    G = nk.graphio.readGraph(f"graph_analysis/graphs/{journal}.graphml", nk.Format.GraphML)

    N = G.numberOfNodes()

    # Compute clustering coefficient
    clc = nk.globals.clustering(G)

    # Compute degree centrality
    dc = nk.centrality.DegreeCentrality(G)#, normalized=True)
    dc_scores = dc.run().scores()

    avg_dc = np.mean(list(dc_scores))
    std_dc = np.std(list(dc_scores))
    ci_dc = 1.96 * std_dc / np.sqrt(len(dc_scores))
    np.save(f"graph_analysis/measures/dc_scores/{journal}.npy", dc_scores)

    # Compute betweenness centrality
    bc = nk.centrality.Betweenness(G)#, normalized=True)
    bc_scores = bc.run().scores()

    avg_bc = np.mean(list(bc_scores))
    std_bc = np.std(list(bc_scores))
    ci_bc = 1.96 * std_bc / np.sqrt(len(bc_scores))
    np.save(f"graph_analysis/measures/bc_scores/{journal}.npy", bc_scores)

    # Compute closeness centrality
    cc = nk.centrality.HarmonicCloseness(G)#, normalized=True)
    cc_scores = cc.run().scores()
    avg_cc = np.mean(list(cc_scores))
    std_cc = np.std(list(cc_scores))
    ci_cc = 1.96 * std_cc / np.sqrt(len(cc_scores))
    np.save(f"graph_analysis/measures/cc_scores/{journal}.npy", cc_scores)

    # Compute modularity
    communities = nk.community.detectCommunities(G)
    mod = nk.community.Modularity().getQuality(communities, G)

    # Create DataFrame with the measures
    df = pd.DataFrame({"Clustering coefficient": [clc],
                        "Avg DC": [avg_dc],
                        "95% CI DC": [ci_dc],
                        "Avg BC": [avg_bc],
                        "95% CI BC": [ci_bc],
                        "Avg CC": [avg_cc],
                        "95% CI CC": [ci_cc],
                        "Modularity": [mod],
                        "Number of nodes": [N]})
    
    print(df)

    df.to_csv(f"graph_analysis/measures/{journal}.csv", index=False)
    
# Main

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    graph_measures(journal)