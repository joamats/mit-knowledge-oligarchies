import pandas as pd
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

journals = ['BMJ', 'JAMA', 'Lancet', 'NEJM', 'Nature', 'PLOS']

# Dataframe to store global measures from all journals
df_global = pd.DataFrame()


for journal in journals:
    # Load global measures
    df = pd.read_csv(f'graph_analysis/measures/{journal}.csv')

    # # normalize the measures DC, BC, CC (and their 95% CI) by the number of nodes
    # # to get the average degree, betweenness, closeness centrality
    # df['Avg DC'] = df['Avg DC'] / df['Number of nodes']
    # df['95% CI DC'] = df['95% CI DC'] / df['Number of nodes']
    # df['Avg BC'] = df['Avg BC'] / df['Number of nodes']
    # df['95% CI BC'] = df['95% CI BC'] / df['Number of nodes']
    # df['Avg CC'] = df['Avg CC'] / df['Number of nodes']
    # df['95% CI CC'] = df['95% CI CC'] / df['Number of nodes']

    # Add journal column
    df['journal'] = journal
    # Concatenate to the global dataframe
    df_global = df_global.append(df)

# Create columns with CI upper and lower bounds from the 95% CI DC column
df_global['DC_lower'] = df_global['Avg DC'] - df_global['95% CI DC']
df_global['DC_upper'] = df_global['Avg DC'] + df_global['95% CI DC']

# same for BC
df_global['BC_lower'] = df_global['Avg BC'] - df_global['95% CI BC']
df_global['BC_upper'] = df_global['Avg BC'] + df_global['95% CI BC']

# same for CC
df_global['CC_lower'] = df_global['Avg CC'] - df_global['95% CI CC']
df_global['CC_upper'] = df_global['Avg CC'] + df_global['95% CI CC']

# save the global dataframe
df_global.to_csv('graph_analysis/measures/global_measures.csv', index=False)

# Create a figure with 3 subplots: DC, BC, CC
# journal in the y axis, measures in the x axis
# error bar with the ci


lowers = ['DC_lower', 'BC_lower', 'CC_lower']
uppers = ['DC_upper', 'BC_upper', 'CC_upper']
labels = ['Degree centrality', 'Betweenness centrality', 'Closeness centrality']
avgs = ['Avg DC', 'Avg BC', 'Avg CC']

fig, axs = plt.subplots(1, 3, figsize=(12, 3.5), dpi=300)

for i in range(3):
    # Plot the error bars
    axs[i].errorbar(df_global[avgs[i]], df_global.journal, xerr=df_global[uppers[i]] - df_global[avgs[i]], fmt='o', capsize=5)
    # Set the labels
    axs[i].set_xlabel(labels[i])
    axs[i].set_ylabel('Journal')
    # Set the title
    axs[i].set_title(labels[i])

# Add super title
fig.suptitle('Global measures of centrality')#

plt.tight_layout()
plt.savefig('graph_analysis/measures/global_measures.png')

