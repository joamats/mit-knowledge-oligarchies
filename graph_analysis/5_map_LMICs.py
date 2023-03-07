import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import seaborn as sb
from tqdm import tqdm

def plot_labelled(journal, df_all, lmics_codes):

    # Filter by journal
    df_journal = df_all[df_all['journal.title'] == journal]

    # Group by researcher_id to get one row per author
    df_journal = df_journal.groupby('researcher_id').agg({'journal.title': 'first', 'aff_country_code': 'first'}).reset_index()

    # Function to determine LMIC and use inside apply
    def is_lmic(x, lmics_codes):

        if x is np.nan:
            return 3
        elif x in lmics_codes:
            return 2
        else:
            return 1
        
    # Add LMIC column
    df_journal['LMIC'] = df_journal.aff_country_code.apply(lambda x: is_lmic(x, lmics_codes))

    # Assign labels
    labels = df_journal['LMIC'].values

    # Load the saved tSNE
    tsne = np.load(f'graph_analysis/tSNE/{journal}.npy')

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(30, 30), dpi=200) 
    sb.scatterplot(x=tsne[:, 0], y=tsne[:, 1], hue=labels, s=100, palette="tab10", ax=ax)
    ax.set_title(f"{journal}")

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ["HICs", "LMICs", "Unknown"])

    fig.savefig(f'graph_analysis/LMICs/{journal}_LMICs.png')


# Main

df_all = pd.read_csv('data_light/authors_journals.csv')[['researcher_id', 'journal.title', 'aff_country_code']]

# Remove repeated authors within the same paper
df_all = df_all.drop_duplicates()

# Simplify Journals Titles
df_all['journal.title'].replace({'The BMJ':'BMJ',
                                 'The Lancet':'Lancet',
                                 'New England Journal of Medicine':'NEJM',
                                 'Nature Medicine':'Nature',
                                 'PLOS Medicine':'PLOS'},
                                 inplace=True)

lmics_codes = pd.read_csv('data_light/lmics_codes.csv')['Code'].values

journal_names = ["BMJ", "JAMA", "Lancet", "NEJM", "Nature", "PLOS"]

for journal in tqdm(journal_names):
    plot_labelled(journal, df_all, lmics_codes)