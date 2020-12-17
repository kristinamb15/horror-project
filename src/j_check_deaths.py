# Checking characters vs deaths

import numpy as np
import pandas as pd
import bs4
import requests
import re

# Import data paths
from os import path
from utilities import (raw_data, proc_data)

# Load dataframe
characters = pd.read_csv(path.join(raw_data, 'i_horror_characters_stripped.csv'), index_col=[0,1])
h_wiki_urls = pd.read_csv(path.join(proc_data, 'horror_wiki_urls.csv'), index_col=0)
l_wiki_deaths = pd.read_csv(path.join(proc_data, 'list_wiki_deaths.csv'), index_col=[0,1])
h_wiki_deaths = pd.read_csv(path.join(proc_data, 'horror_wiki_deaths.csv'), index_col=[0,1])

# Initialize 'killed' column
characters['killed'] = None

# Function to collect all movies and character indices for each movie (for easy looping)
def get_movie_chars(df):
    movie_dict = dict()
    for m_ind, c_ind in df.index.values:
        movie_dict.setdefault(m_ind, []).append(c_ind)
    return movie_dict

# Function to get list of deaths from horror wiki for a particular movie
def get_horror_wiki_deaths(m_ind):
    title = h_wiki_urls.loc[m_ind, 'Stripped Title']
    year = h_wiki_urls.loc[m_ind, 'Year']

    # Filter by title and year
    h_deaths = h_wiki_deaths[(h_wiki_deaths['Stripped Title'] == title) & (h_wiki_deaths['Year'] == year)]

    # Collect characters
    deaths = h_deaths['stripped character'].values
    return deaths

# Function to get list of deaths from list of deaths wiki for a particular movie
# This one is a little trickier because the year is not included for all of the movies
def get_list_wiki_deaths(m_ind):
    title = h_wiki_urls.loc[m_ind, 'Stripped Title']
    year = h_wiki_urls.loc[m_ind, 'Year']

    # Check subheadings first (to capture movies that were on a series page)
    l_deaths = l_wiki_deaths[l_wiki_deaths['Stripped Title (Heading)'] == title]

    # If the subheading isn't found, check the page title
    if len(l_deaths.values) == 0:
        l_deaths = l_wiki_deaths[l_wiki_deaths['Stripped Title (Page)'] == title]
    
    # If year is available, filter further by year
    if len(l_deaths['Year'].values) != 0:
        l_deaths = l_deaths[l_deaths['Year'] == year]

    # Collect character names
    deaths = l_deaths['stripped character'].values
    return deaths

# Function to check one character against a list of deaths
def check_death(deaths, char):  
    # Check horror wiki deaths    
    if len(deaths) > 0:
        # Use regex to search for character name in list of deaths
        char_pattern = re.compile(f'{char}')
        matches = list(filter(lambda x: re.search(char_pattern, str(x)), deaths))
        # Check if at least one match
        is_killed = len(matches) > 0
        return is_killed
    else:
        return 'N/A'

# Function to update deaths
def update_deaths(movie_dict):
    for m_ind in movie_dict.keys():
        # Get deaths from both wikis
        deaths1 = get_horror_wiki_deaths(m_ind)
        deaths2 = get_list_wiki_deaths(m_ind)
        deaths = np.concatenate((deaths1, deaths2))

        # Check characters
        for c_ind in movie_dict[m_ind]:
            char = characters.loc[(m_ind, c_ind), 'stripped character']
            is_killed = check_death(deaths, char)        
            characters.loc[(m_ind, c_ind), 'killed'] = is_killed

# Apply to dataframe
movie_dict = get_movie_chars(characters)
update_deaths(movie_dict)

# Resave files
# Optional: add index=False to not save index column
characters.to_csv(path.join(raw_data, 'j_horror_characters_with_deaths.csv'))