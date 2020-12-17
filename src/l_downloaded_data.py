# Database of actor race/gender information found via
# https://github.com/thomaslam/hollywood-diversity-dataviz
# downloaded as 'casts.db'

import pandas as pd
import sqlite3

# Import data paths
from os import path
from utilities import ext_data

# Create connection to db file
cnx = sqlite3.connect(path.join(ext_data, 'casts.db'))

# Read data into dataframe
df = pd.read_sql_query("SELECT * FROM casts", cnx)

# Data needed some cleaning
# Select rows with only Male/Female/Other(s) as gender (there were some entries with country names as gender)
df = df[(df['gender'] == 'Male') |  (df['gender'] == 'Female') | (df['gender'] == 'Other') | (df['gender'] == 'Others')]

# Standardize by replacing 'Others' with 'Other'
for ind in df.index.values:
    if df.loc[ind, 'gender'] == 'Others':
        df.loc[ind, 'gender'] = 'Other'

# Save file
df.to_csv(path.join(ext_data, 'race_gender.csv'))