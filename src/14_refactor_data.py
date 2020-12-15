# Refactoring data for easier analysis

import pandas as pd

# Import data paths
from os import path
from utilities import (raw_data, proc_data, ext_data)

# Load character data
characters = pd.read_csv(path.join(proc_data, 'horror_characters.csv'), index_col=[0,1])

# Get only characters whose killed status, gender, and race are known
df = characters[(characters['killed'].notna()) & (characters['gender'] != 'Unlisted') & (characters['race'] != 'Unlisted')]

# Get category counts
female = df[df['gender'] == 'Female']['killed'].value_counts()
male = df[df['gender'] == 'Male']['killed'].value_counts()
other = df[df['gender'] == 'Other']['killed'].value_counts()
hispanic = df[df['race'] == 'Hispanic']['killed'].value_counts()
asian_indian = df[df['race'] == 'Asian/Indian']['killed'].value_counts()
multiracial = df[df['race'] == 'Multiracial']['killed'].value_counts()
white = df[df['race'] == 'White']['killed'].value_counts()
black = df[df['race'] == 'Black']['killed'].value_counts()

# Create dataframes
cols = {False: 'Survived', True: 'Died'}
df1 = pd.DataFrame(female).transpose().rename(index={'killed': 'Female'}, columns=cols)
df2 = pd.DataFrame(male).transpose().rename(index={'killed': 'Male'}, columns=cols)
df3 = pd.DataFrame(other).transpose().rename(index={'killed': 'Other'}, columns=cols)
df4 = pd.DataFrame(hispanic).transpose().rename(index={'killed': 'Hispanic'}, columns=cols)
df5 = pd.DataFrame(asian_indian).transpose().rename(index={'killed': 'Asian/Indian'}, columns=cols)
df6 = pd.DataFrame(multiracial).transpose().rename(index={'killed': 'Multiracial'}, columns=cols)
df7 = pd.DataFrame(white).transpose().rename(index={'killed': 'White'}, columns=cols)
df8 = pd.DataFrame(black).transpose().rename(index={'killed': 'Black'}, columns=cols)

# Concatenate
main = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])

# Save to file
main.to_csv(path.join(proc_data, 'category_counts.csv'))