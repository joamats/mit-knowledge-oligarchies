import pandas as pd
from tqdm import tqdm
import pickle

def cluster_lmics(journal):

    # read LMICs
    df_lmic = pd.read_csv(f'graph_analysis/LMICs/{journal}_LMICs.csv')
    print(f"Number of Authors: {df_lmic.shape}")

    # Read cluster with pickle
    with open(f'graph_analysis/clusters/{journal}.pkl', 'rb') as f:
        clusters = pickle.load(f)

    # count to total of authors in all clusters
    counter = 0
    for c in clusters:
        counter += len(c)
    

    print(f"Number of authors clusters: {counter}")


journal_names = ["BMJ"]#, "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    cluster_lmics(journal)