import pandas as pd

authors = pd.read_csv("data/publications_authors.csv")
journals = pd.read_csv("data/publications_journals.csv")

# Join the journal name with the author (per publication)
authors_journals = authors.join(journals.set_index('id'), on='pub_id', rsuffix='_right')

authors_journals = authors_journals[['pub_id', 'researcher_id', 'author_name', 'aff_name', \
                                     'aff_id', 'aff_city_id', 'aff_country_code', 'journal.title']]

# Drop Authors without an ID
aj = authors_journals.dropna(subset=['researcher_id'])

print(f"Dropped {len(authors_journals) - len(aj)} that were null")

aj.to_csv("data_light/authors_journals.csv")
