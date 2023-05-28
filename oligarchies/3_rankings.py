import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import seaborn as sns
matplotlib.use('TKAgg')

authors_info = pd.read_csv('data_light/authors_info.csv')

journal_names = ['BMJ', 'Lancet', 'NEJM', 'Nature', 'JAMA','PLOS']

results_df = pd.DataFrame(columns=['journal', 'subset', 'group', 'value'])

for journal in journal_names:

    centr = pd.read_csv(f'oligarchies/centralities/{journal}.csv')
    centr = centr.merge(authors_info, on='researcher_id')

    # limit to degree for now
    centr = centr[["researcher_id", "gender", "LMIC", "Degree Centrality"]]
    centr = centr.sort_values(by='Degree Centrality', ascending=False)

    # assign rank -> the lower the better, the more central
    centr['rank'] = centr['Degree Centrality'].rank(ascending=False, pct=True)

    # look at the top 10% most central
    centr_01 = centr[centr['rank'] <= 0.1]


    print(journal)
    # add to results_df
    results_df = results_df.append({'journal': journal,
                                    'subset': 'all',
                                    'group': 'LMIC',
                                    'value': centr['LMIC'].value_counts(normalize=True)[1]},
                                    ignore_index=True)
    results_df = results_df.append({'journal': journal,
                                    'subset': 'top_10%',
                                    'group': 'LMIC',
                                    'value': centr_01['LMIC'].value_counts(normalize=True)[1]},
                                    ignore_index=True)
    results_df = results_df.append({'journal': journal,
                                    'subset': 'all',
                                    'group': 'female',
                                    'value': centr['gender'].value_counts(normalize=True)[1]},
                                    ignore_index=True)
    results_df = results_df.append({'journal': journal,
                                    'subset': 'top_10%',
                                    'group': 'female',
                                    'value': centr_01['gender'].value_counts(normalize=True)[1]},
                                    ignore_index=True)
    

# save results_df
results_df.to_csv('oligarchies/centralities/results.csv')  

print(results_df)

    # print percentage of LMICs = 2 and gender = female
