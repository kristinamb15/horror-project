# Cleaning up character/actor entries

import pandas as pd
import re

# Import data paths
from os import path
from utilities import (raw_data, proc_data)

df = pd.read_csv(path.join(raw_data, 'f_horror_characters_all.csv'), index_col=[0,1])

# Remove entries that have no character/actor
df = df[(df['character'].notna()) & (df['actor'].notna())]

# Removing some strange actor entries I noticed by keywords
# Actor name is set to 'None' so it will be removed in the next step
def remove_strange_ac(char_df):
    words = ['(in\sher\s)', '(raped\s)', '(\swhile\s)', '(rape\s)', '(\sknown)']

    for mov_ind, ind in char_df.index.values:
        actor = char_df.loc[(mov_ind, ind), 'actor']

        if bool(re.search(r'|'.join(words), actor, flags=re.IGNORECASE)):
            char_df.loc[(mov_ind, ind), 'actor'] = None
        else:
            pass

# Apply to dataframe
remove_strange_ac(df) 

# Remove entries that have no character/actor again
df = df[(df['character'].notna()) & (df['actor'].notna())]

# Function to clean messy character names
def clean_char_name(actor_name, char_name):
    
    # Replacing character names of him/herself with actor name
    if bool(re.search('(himself)|(herself)', char_name, flags=re.IGNORECASE)):
        char_return = actor_name
    
    # For longer character names that include descriptions, we attempt to split off just the name
    else:
        char_return = char_name

        breaks = [',', '(?:\sa\s)', '(?:\san\s)', ':', ';', '\(', '(?:\smakes\s)', '(?:\scharacter\s)', '(?:\sshe\s)', '\[']
        char_spl = re.split(r'|'.join(breaks), char_return, maxsplit=1, flags=re.IGNORECASE)
        #char_spl = re.split(',| a | an |:| the |;|(| makes', char_return)
        char_return = char_spl[0]

    # Remove leading/trailing whitespaces
    char_return = char_return.strip()
    
    return char_return

# Function to clean messy actor names
# Some actor names have '(uncredited)' or other extra junk to be removed
def clean_actor_name(actor_name):
    breaks = ['(?:\swho\s)', '\(', '(?:\salso\s)']

    ac_spl = re.split('|'.join(breaks), actor_name, maxsplit=1, flags=re.IGNORECASE)
    ac_return = ac_spl[0]

    # Remove leading/trailing whitespaces
    ac_return = ac_return.strip()
    
    return ac_return

# Function to clean character/actor names in dataframe
def clean_char_df(char_df):
    for mov_ind, ind in char_df.index.values:
        
        # Clean actor name
        actor = char_df.loc[(mov_ind, ind), 'actor']
        ac_name = clean_actor_name(actor)
        char_df.loc[(mov_ind, ind), 'actor'] = ac_name

        # Clean character name
        character = char_df.loc[(mov_ind, ind), 'character']
        char_name = clean_char_name(ac_name, character)
        char_df.loc[(mov_ind, ind), 'character'] = char_name

# Apply to dataframe
clean_char_df(df)

# Resave file
# Optional: add index=False to not save index column
df.to_csv(path.join(raw_data, 'g_horror_characters_clean.csv'))