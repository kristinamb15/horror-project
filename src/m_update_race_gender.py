# Comparing character dataframe to actor database found at
# https://github.com/thomaslam/hollywood-diversity-dataviz

import pandas as pd

# Import data paths
from os import path
from utilities import (raw_data, proc_data, ext_data)

characters = pd.read_csv(path.join(raw_data, 'k_horror_characters_with_info.csv'), index_col=[0,1])
actor_db = pd.read_csv(path.join(ext_data, 'race_gender.csv'), index_col=0)

def compare(df, r=True, g=True):

    # For every character in character dataframe
    for m_ind, c_ind in characters.index.values:
        
        # Get actor name
        actor = characters.loc[(m_ind, c_ind), 'actor']
        
        # Check if actor in df
        if actor in df['name'].values:
            # If actor in df, get index
            i = df.loc[df['name'] == actor].index[0]
            # If updating race
            if r and characters.loc[(m_ind, c_ind), 'race'] == 'Unlisted':
                characters.loc[(m_ind, c_ind), 'race'] = df.loc[i, 'race']
            # If updating gender
            if g and characters.loc[(m_ind, c_ind), 'gender'] == 'Unlisted':
                characters.loc[(m_ind, c_ind), 'gender'] = df.loc[i, 'gender']

compare(actor_db)

# There are both 'Asian' and 'Asian/Indian' listed as races - we make all of those say 'Asian/Indian'
characters['race'].replace('Asian', 'Asian/Indian', inplace=True)

# Resave file
characters.to_csv(path.join(raw_data, 'm_horror_characters_updated.csv'))

# Save as processed data
characters.to_csv(path.join(proc_data, 'horror_characters.csv'))