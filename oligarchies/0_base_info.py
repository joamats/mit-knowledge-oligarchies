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
        return -1
    elif x in lmics_codes:
        return 1
    else:
        return 0
    
# Add LMIC column
df_all['LMIC'] = df_all.aff_country_code.apply(lambda x: is_lmic(x, lmics_codes))

# Assign gender
gender_df = pd.read_feather('data/high_impact_publications.feather')[['researcher_id', 'gender', 'current_organization_id']]

# merge with authors_journals.csv
df_final = gender_df.merge(df_all, on='researcher_id').drop_duplicates()
df_final = df_final[['researcher_id', 'gender', 'LMIC', 'current_organization_id']]

df_final.to_csv('data_light/authors_info.csv', index=False)

# Assign year
year_df = pd.read_feather('data/high_impact_publications.feather')[['pub_id', 'year']]
year_df = year_df.drop_duplicates()
year_df.to_csv('data_light/pubs_info.csv', index=False)
