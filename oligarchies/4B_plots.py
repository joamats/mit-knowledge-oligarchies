import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use('TKAgg')



df = pd.read_csv('oligarchies/centralities/results.csv')

# Filter the dataframe for LMIC values only
female_df = df[df['group'] == 'female']

# Group the data by journal and subset
grouped_df = female_df.groupby(['journal', 'subset']).mean().reset_index()

# Create the bar plot
fig, ax = plt.subplots()

bar_width = 0.35
opacity = 0.8

# Set colors and labels
colors = ['#1f77b4', '#ff7f0e']
labels = ['all authors', 'top 10% most central']

# Get unique journals and subsets
journals = grouped_df['journal'].unique()
subsets = grouped_df['subset'].unique()

# Calculate the bar positions with offset
offset = bar_width / 2
pos = np.arange(len(journals))

for i, subset in enumerate(subsets):
    subset_df = grouped_df[grouped_df['subset'] == subset]
    bar_pos = pos + (i * bar_width) - offset
    ax.bar(bar_pos, subset_df['value'], bar_width, alpha=opacity, color=colors[i], label=labels[i])

# Add labels and title
ax.set_xlabel('Journal')
ax.set_ylabel('Percentage of Female Authors')
ax.set_title('Female Authors: Top 10% Most Central Authors vs. All Authors')
ax.legend()

# Set x-axis ticks and labels
ax.set_xticks(pos)
ax.set_xticklabels(journals)

# Rotate x-axis labels if needed
plt.xticks(rotation=90)
plt.ylim(0, .6)

# Display the plot
plt.tight_layout()
plt.savefig('oligarchies/centralities/results_female.png')
