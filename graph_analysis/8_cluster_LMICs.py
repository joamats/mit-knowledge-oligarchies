import pandas as pd
from tqdm import tqdm
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np

def cluster_lmics(journal):

    # read cluster measures
    df = pd.read_csv(f'graph_analysis/cluster_measures/{journal}.csv')

    # transform LMICs percentage to %
    df.LMICs_perc = df.LMICs_perc * 100

    # drop the row with index 0
    df = df.drop(0)

    # create 4 bins for quartiles of the centrality scores
    df["bc_bin"] = pd.qcut(df["Avg BC"].rank(method='first'), 4, labels=["q1", "q2", "q3", "q4"])
    df["dc_bin"] = pd.qcut(df["Avg DC"].rank(method='first'), 4, labels=["q1", "q2", "q3", "q4"])
    df["cc_bin"] = pd.qcut(df["Avg CC"].rank(method='first'), 4, labels=["q1", "q2", "q3", "q4"])
    
    # calculate the percentage of LMICs in each bin
    df_final_bc = df.groupby("bc_bin").agg({"total": ["mean", "sum"], "Avg BC": ["min", "max"], "LMICs_perc": ["median", "std"]})
    df_final_dc = df.groupby("dc_bin").agg({"total": ["mean", "sum"], "Avg DC": ["min", "max"], "LMICs_perc": ["median", "std"]})
    df_final_cc = df.groupby("cc_bin").agg({"total": ["mean", "sum"], "Avg CC": ["min", "max"], "LMICs_perc": ["median", "std"]})
    
    # compute confidence intervals for LMIC percentage
    df_final_bc["lmic_ci"] = 1.96 * (df_final_bc["LMICs_perc"]["std"] / np.sqrt(df_final_bc["total"]["sum"]))
    df_final_dc["lmic_ci"] = 1.96 * (df_final_dc["LMICs_perc"]["std"] / np.sqrt(df_final_dc["total"]["sum"]))
    df_final_cc["lmic_ci"] = 1.96 * (df_final_cc["LMICs_perc"]["std"] / np.sqrt(df_final_cc["total"]["sum"]))

    # save the dataframe
    df_final_bc.to_csv(f'graph_analysis/cluster_LMICs/bc/{journal}.csv')
    df_final_dc.to_csv(f'graph_analysis/cluster_LMICs/dc/{journal}.csv')
    df_final_cc.to_csv(f'graph_analysis/cluster_LMICs/cc/{journal}.csv')

    # plot the results: bar plot, x axis is the bin, y axis is the average betweenness centrality
    # iterate over the 3 centrality measures

    score_types = ["bc", "dc", "cc"]
    centr_measures = ["Avg BC", "Avg DC", "Avg CC"]
    centr_labels = ["Betweenness Centrality", "Degree Centrality", "Closeness Centrality"]

    for i in range(3):
        if i == 0:
            df_final = df_final_bc
        elif i == 1:
            df_final = df_final_dc
        else:
            df_final = df_final_cc

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.bar(df_final.index, df_final.LMICs_perc["median"], yerr=df_final.lmic_ci, capsize=5, color="orange")
        ax.set_xlabel(f"{centr_labels[i]}, quartile of clusters")
        ax.set_ylabel("Median % of LMICs authors")
        #ax.set_xticklabels([f"{df_final[centr_measures[i]]['min'][i]:.0f} - {df_final[centr_measures[i]]['max'][i]:.0f}" for i in df_final.index])
        ax.set_title(f"{journal} - {centr_labels[i]}")
        plt.tight_layout()
        fig.savefig(f'graph_analysis/cluster_LMICs/{score_types[i]}/{journal}.png')

    # save figure
    fig.savefig(f'graph_analysis/cluster_LMICs/{journal}_nauthors.png')


journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in journal_names:
    cluster_lmics(journal)