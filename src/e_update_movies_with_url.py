# Update horror movie list with horror wiki index

import pandas as pd

# Import data paths
from os import path
from utilities import (raw_data, proc_data)

movies = pd.read_csv(path.join(raw_data,'d_horror_movies_stripped.csv'), index_col=0)
h_urls = pd.read_csv(path.join(proc_data, 'horror_wiki_urls.csv'), index_col=0)

def get_wiki(title, year):

    # For IMDB entry, check if there is a matching movie in the Horror Wikis
    h_check = h_urls[(h_urls['Stripped Title'] == title) & (h_urls['Year'] == year)]

    if len(h_check) > 0:
        h_entry = h_check.iloc[0]
        h_index = int(h_entry.name)
        h_url = h_entry['Horror Wiki URL']
    else:
        h_index = None
        h_url = None

    return {'Horror Wiki Index': h_index, 'Horror Wiki URL': h_url}

# Find and add movie urls to movies dataframe
df = movies.apply(lambda x: get_wiki(x['Stripped Title'], x['Year']), axis=1, result_type='expand')
movies = pd.concat([movies, df], axis='columns')

# Resave files
# Optional: add index=False to not save index column
movies.to_csv(path.join(raw_data, 'e_horror_movies_with_url.csv'))

# This is the final form of this data we will work with
movies.to_csv(path.join(proc_data, 'horror_movies.csv'))