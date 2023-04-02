import pandas as pd
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

def cluster_lmics(journal):

    # read cluster measures
    df = pd.read_csv(f'graph_analysis/cluster_measures/{journal}.csv')

    # create 4 bins for quartils of the mean betweeness centrality of each cluster
    df["bc_bin"] = pd.qcut(df.avg_bc, 4, labels=["q1", "q2", "q3", "q4"])

    # calculate the percentage of LMICs in each bin
    df_final = df.groupby("bc_bin").agg({"LMICs": "sum", "total": "sum"})
    df_final["LMICs_perc"] = df_final.LMICs / df_final.total

    print(df_final)




journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    cluster_lmics(journal)