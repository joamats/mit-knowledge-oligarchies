import pandas as pd
import numpy as np

df_all = pd.read_csv('data_light/authors_journals.csv')

# Remove repeated authors within the same paper
df_all = df_all.drop_duplicates()

# Assign LMICs
lmics_codes = pd.read_csv('data_light/lmics_codes.csv')['Code'].values

# Group by researcher_id to get one row per author
df_all = df_all.groupby('researcher_id').agg({'journal.title': 'first', 'aff_country_code': 'first'}).reset_index()

# Function to determine LMIC and use inside apply
def is_lmic(x, lmics_codes):

    if x is np.nan:
        return 3
    elif x in lmics_codes:
        return 2
    else:
        return 1
    
# Add LMIC column
df_all['LMIC'] = df_all.aff_country_code.apply(lambda x: is_lmic(x, lmics_codes))

# Assign gender
gender_df = pd.read_feather('data/high_impact_publications.feather')[['researcher_id', 'gender']]

# merge with authors_journals.csv
df_final = gender_df.merge(df_all, on='researcher_id').drop_duplicates()
df_final = df_final[['researcher_id', 'gender', 'LMIC']]

df_final.to_csv('data_light/authors_info.csv', index=False)