# Scraping character names and creating a new table

import pandas as pd
import bs4
import requests
import re

# Import data paths
from os import path
from utilities import (raw_data, proc_data)

horror_base_url = 'https://horror.fandom.com/'

def get_characters(df, i):

    url = df.loc[i]['Horror Wiki URL']
    
    # Get Horror Wiki for movie
    res = requests.get(horror_base_url + url)

    # Select page html
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # Find cast list (some are tables, some are just)
    if soup.find(id='Cast'):

        char_list = soup.find(id='Cast').find_next('ul').find_all('li')

        # If the list is part of a table, get the next list in the table
        if soup.find(id='Cast').find_next('ul').parent.name == 'td':
            char_list_2 = soup.find(id='Cast').find_next('ul').find_next('ul').find_all('li')
        else:
            char_list_2 = []
        
        char_list.extend(char_list_2)

        # Collect characters
        chars = []

        # Cast list is generally in the form '{actor} as {character}'
        # In some cases, 'as' is replaced by other special characters
        # We search for these breakpoints between character and actor to split them
        for li in char_list:
            
            # Get text of list element
            txt = li.text

            # Remove &nbsp; and tabs in text
            if '\xa0' in txt:
                txt = txt.replace('\xa0', ' ')
            if '\t' in txt:
                txt = txt.replace('\t', ' ')           

            # Split into actor and character at specific breakpoints.
            breaks = ['(?:-\s)', '(?:\/)', '(?:\.\.\.)', ',', '(?:—\s)', '(?:–\s)', '(?:\sportrays\s)', '(?:\splays\s)', '(?:\sas)', '(?:\sa\s)']

            spl = re.split(r'|'.join(breaks), txt, 1)              
            
            # Split into actor and character
            actor = spl[0]
            if len(spl) > 1:
                character = spl[-1]
            else:
                character = None

            # Instantiate character information
            new_dict = {'Horror Wiki Index': i, 'actor': actor, 'character': character}

            chars.append(new_dict)

        # Instantiate character dataframe for movie
        chars_df = pd.DataFrame(chars)
        chars_df.index.names=['char index']
        chars_df = chars_df.set_index(['Horror Wiki Index', chars_df.index])

    else:
        chars_df = None
    
    return chars_df    

# Instantiate new characters dataframe
horror_characters = pd.DataFrame()

# Append characters for each movie
df = pd.read_csv(path.join(proc_data, 'horror_wiki_urls.csv'), index_col=0)
for ind in df.index.values:
    horror_characters = pd.concat([horror_characters, get_characters(df, ind)])

# Save to file
# Optional: add index=False to not save index column
horror_characters.to_csv(path.join(raw_data, '06_horror_characters_all.csv'))  