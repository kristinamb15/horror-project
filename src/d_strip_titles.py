# Strip titles for better matching

import pandas as pd
import re

# Import data paths and strip_title function
from os import path
from utilities import (raw_data, proc_data, strip_title)

death_urls = pd.read_csv(path.join(raw_data, 'c_death_list_urls_all.csv'), index_col=0)
wiki_urls = pd.read_csv(path.join(raw_data, 'c_horror_wiki_urls_all.csv'), index_col=0)

# Add stripped titles to both URL dataframes and movie dataframe
new = death_urls.apply(lambda x: strip_title(x['Title'], True), axis=1, result_type='expand')
death_urls = pd.concat([death_urls, new], axis='columns')
death_urls.sort_values(by=['Stripped Title'], inplace=True)
death_urls.to_csv(path.join(raw_data, 'd_death_list_urls_stripped.csv'))

wiki_urls['Stripped Title'] = wiki_urls.apply(lambda x: strip_title(x['Title']), axis=1)
wiki_urls.sort_values(by=['Stripped Title'], inplace=True)
wiki_urls.to_csv(path.join(raw_data, 'd_horror_wiki_urls_stripped.csv'))

movies = pd.read_csv(path.join(raw_data, 'b_horror_movies_clean_year.csv'), index_col=0)
movies['Stripped Title'] = movies.apply(lambda x: strip_title(x['Title']), axis=1)
movies.to_csv(path.join(raw_data,'d_horror_movies_stripped.csv'))

# This is the final form of this data we will work with
death_urls.to_csv(path.join(proc_data, 'death_list_urls.csv'))
wiki_urls.to_csv(path.join(proc_data, 'horror_wiki_urls.csv'))