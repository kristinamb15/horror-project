# Getting stripped version of character names for easy comparison

import pandas as pd
import re

# Import data paths and strip_name function
from os import path
from utilities import (raw_data, proc_data, strip_name)

df1 = pd.read_csv(path.join(raw_data, 'g_horror_characters_clean.csv'), index_col=[0,1])
df1['stripped character'] = df1.apply(lambda x: strip_name(x['character']), axis=1)
df1.to_csv(path.join(raw_data, 'i_horror_characters_stripped.csv'))

df2 = pd.read_csv(path.join(raw_data, 'h_horror_wiki_deaths_all.csv'), index_col=[0,1])
df2['stripped character'] = df2.apply(lambda x: strip_name(x['character']), axis=1)
df2.to_csv(path.join(raw_data, 'i_horror_wiki_deaths_stripped.csv'))

df3 = pd.read_csv(path.join(raw_data, 'h_list_wiki_deaths_all.csv'), index_col=[0,1])
df3['stripped character'] = df3.apply(lambda x: strip_name(x['character']), axis=1)
df3.to_csv(path.join(raw_data, 'i_list_wiki_deaths_stripped.csv'))

# This is the final form of this data we will work with
df2.to_csv(path.join(proc_data, 'horror_wiki_deaths.csv'))
df3.to_csv(path.join(proc_data, 'list_wiki_deaths.csv'))