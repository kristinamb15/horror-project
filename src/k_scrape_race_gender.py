# Scraping race and gender information for stars

import pandas as pd
import bs4
import requests
import re

# Import data paths
from os import path
from utilities import (raw_data, proc_data)

# Load character and movie dataframes
characters = pd.read_csv(path.join(raw_data, 'j_horror_characters_with_deaths.csv'), index_col=[0,1])

# Search page for actor info
nndb_query = 'https://search.nndb.com/search/nndb.cgi?nndb=1&omenu=unspecified&query={}'

# Function to Find nndb actor page (if it exists)
def find_actor_page(name):

    # Splitting names for listings with two actors
    for p in [' and ', ' & ', ' a.k.a']:
        if p in name:
            name_spl = name.split(p)
            name = name_spl[0].strip()
            if len(name_spl) > 1:
                name2 = name_spl[1].strip()
            else:
                name2 = 0
        else:
            name2 = None

    # Search results for actor name
    search_page = requests.get(nndb_query.format(name))
    search_soup = bs4.BeautifulSoup(search_page.text, 'lxml')

    # Find name on page
    if search_soup.find('a', text=re.compile(name)):
        name_page = search_soup.find('a', text=re.compile(name, flags=re.IGNORECASE),).get('href')
    elif name2 and search_soup.find('a', text=re.compile(name2, flags=re.IGNORECASE)):
        name_page = search_soup.find('a', text=re.compile(name2, flags=re.IGNORECASE)).get('href')
    else:
        name_page = None

    return name_page

# Function to scrape actor url for race/ethnicity and gender
def get_info(info_url):
    if info_url is not None:
        # Get actor page
        page = requests.get(info_url)
        soup = bs4.BeautifulSoup(page.text, 'lxml')

        # Find gender
        if soup.find('b', text=re.compile('^Gender')):
            gender = soup.find('b', text=re.compile('^Gender')).next_sibling.strip()
        else:
            gender = 'Unlisted'
        
        # Find race
        if soup.find('b', text=re.compile('^Race')):
            race = soup.find('b', text=re.compile('^Race')).next_sibling.strip()
        else:
            race = 'Unlisted'

    else:
        race = 'Unlisted'
        gender = 'Unlisted'
        
    return {'race': race, 'gender': gender}


# Find actor url pages for entries in characters dataframe
characters['actor url'] = characters['actor'].apply(find_actor_page)

# Get race/gender and concat to dataframe
char_info = characters.apply(lambda x: get_info(x['actor url']), axis=1, result_type='expand')
characters = pd.concat([characters, char_info], axis='columns')

# Resave files
# Optional: add index=False to not save index column
characters.to_csv(path.join(raw_data, 'k_horror_characters_with_info.csv'))