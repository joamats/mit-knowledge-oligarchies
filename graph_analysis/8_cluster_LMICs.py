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

    # create 4 bins for quartiles of the LMICs percentage
    df["bc_bin"] = pd.qcut(df.LMICs_perc.rank(method='first'), 4, labels=["q1", "q2", "q3", "q4"])

    # calculate the percentage of LMICs in each bin
    df_final = df.groupby("bc_bin").agg({"total": ["mean", "std", "sum"], "LMICs_perc": ["min", "max", "mean"],
                                         "avg_bc": ["mean", "std"]})
    
    # compute confidence intervals for the betweenness centrality
    df_final["bc_ci"] = 1.96 * (df_final["avg_bc"]["std"] / np.sqrt(df_final["total"]["sum"]))

    # compute confidence intervals for the total number of authors
    df_final["total_ci"] = 1.96 * (df_final["total"]["std"] / np.sqrt(df_final["total"]["sum"]))

    # df_final['avg_bc'] = pooled_mean
    # df_final['std_bc'] = pooled_std
    # df_final['bc_ci'] = ci

    # save the dataframe
    df_final.to_csv(f'graph_analysis/cluster_LMICs/{journal}.csv')

    print(df_final)

    plt.tight_layout()
    # plot the results: bar plot, x axis is the bin, y axis is the average betweenness centrality
    fig, ax = plt.subplots(nrows=1, ncols=1)#, figsize=(10, 10), dpi=200)
    ax.bar(df_final.index, df_final["avg_bc"]["mean"], yerr=df_final["bc_ci"], capsize=5, color="orange")
    ax.set_xlabel("% of LMICs authors, per quartile of clusters")
    ax.set_ylabel("Betweenness Centrality")
    # set x ticks to be the percentage of LMICs in each bin, min-max
    ax.set_xticklabels([f"{df_final['LMICs_perc']['min'][i]:.0f} - {df_final['LMICs_perc']['max'][i]:.0f}" for i in df_final.index])
    ax.set_title(f"{journal} Clusters' Betweenness Centrality")

    # save figure
    fig.savefig(f'graph_analysis/cluster_LMICs/{journal}_bc.png')

    # plot the results: bar plot, x axis is the bin, y axis is the total number of authors
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.bar(df_final.index, df_final["total"]["mean"], yerr=df_final["total_ci"], capsize=5, color="green")
    ax.set_xlabel("% of LMICs authors, per quartile of clusters")
    ax.set_ylabel("Total number of authors")
    # set x ticks to be the percentage of LMICs in each bin, min-max
    ax.set_xticklabels([f"{df_final['LMICs_perc']['min'][i]:.0f} - {df_final['LMICs_perc']['max'][i]:.0f}" for i in df_final.index])
    ax.set_title(f"{journal} Clusters' Total number of authors")

    # save figure
    fig.savefig(f'graph_analysis/cluster_LMICs/{journal}_nauthors.png')


journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in journal_names:
    cluster_lmics(journal)