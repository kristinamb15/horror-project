# Remove entries that have no year listed or year greater than current (2020) - as this will be important for searching character info

import pandas as pd

# Import data paths
from os import path
from utilities import raw_data

df = pd.read_csv(path.join(raw_data, '01_horror_movies_all.csv'), index_col=0)

df = df[(df['Year'].notna()) & (df['Year'] <= 2020)]

# Resave files
# Optional: add index=False to not save index column
df.to_csv(path.join(raw_data, '02_horror_movies_clean_year.csv'))