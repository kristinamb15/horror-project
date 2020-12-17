# Collect character deaths from Horror Wiki and List of Deaths Wiki

import pandas as pd
import re
import requests
import bs4

# Import data paths and strip_title function
from os import path
from utilities import (raw_data, proc_data, strip_title)

horror_wiki = pd.read_csv(path.join(proc_data, 'horror_wiki_urls.csv'), index_col=0)
list_wiki = pd.read_csv(path.join(proc_data, 'death_list_urls.csv'), index_col=0)

def get_deaths(df, i, df_name):

    # Get page
    if df_name == 'horror_wiki':
        # Finding horror movie on Horror Fandom Wiki
        base_url = 'https://horror.fandom.com/'
        url = df.loc[i, 'Horror Wiki URL']
    elif df_name == 'list_wiki':
        # Finding horror movie on List of Deaths Wiki 
        base_url = 'https://listofdeaths.fandom.com/'
        url = df.loc[i, 'Death List URL']
    else:
        raise Exception('Invalid argument.')

    # Select page html
    res = requests.get(base_url + url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    if df_name == 'horror_wiki':

        # Get title
        title = df.loc[i, 'Stripped Title']

        # Find list of deaths table
        if soup.find(id='List_of_Deaths'):
            new_soup = soup.find(id='List_of_Deaths').find_next('tbody')

            # Get first column of table
            if new_soup:
                dead_chars = []
                # Check if first column of table is 'Segment' (for anthology movies)
                if ('Segment' in new_soup.find('tr').find_next().text) or (new_soup.find('td').text == '1.'):
                    col2 = True
                else:
                    col2 = False

                # Starting after the header row, loop through all rows in table    
                for row in new_soup.find_all('tr')[1:]:
                    # If first column of table is not 'Name' (i.e. table has a 'Segment' column), use second column to get names
                    if col2:
                        char = row.find('td').find_next('td').text.strip('\n').strip()
                    else:
                        char = row.find('td').text.strip('\n').strip()

                    # Instantiate character information
                    new_dict = {'Horror Wiki Index': i, 'Stripped Title': title, 'character': char}
                    dead_chars.append(new_dict)

                # Instantiate character dataframe for movie
                deaths_df = pd.DataFrame(dead_chars, columns=['Horror Wiki Index', 'Stripped Title', 'character'])
                deaths_df.index.names=['char index']
                deaths_df.set_index(['Horror Wiki Index', deaths_df.index], inplace=True)
            else:
                deaths_df = None    
        else:
            deaths_df = None

    elif df_name == 'list_wiki':

        # Get page title
        title = df.loc[i, 'Stripped Title']

        # Find categories list
        # For some reason, TV shows are included and we want to skip those
        cats = [li.text.strip('\n').strip() for li in soup.find(class_='page-header__categories').find_all('a')]
        if 'TV Shows' in cats or 'Youtube' in cats:
            go = False
        else:
            go = True

        # Find first headline of main content
        new_soup = soup.find(id='content').find(class_='mw-headline')
        
        # If not TV show and victims/deaths lists exist
        if go and new_soup:
            # Instantiate storage
            dead_chars = []
            # Loop through character lists
            while new_soup and new_soup.find_next('ol'):

                new_soup = new_soup.find_next('ol')

                # Skip list if title contains 'Before'/'Between' movies and 'Other'
                if not bool(re.match(r'^((before)|(between)|(other))', new_soup.find_previous(class_='mw-headline').text, re.IGNORECASE)):

                    # Get subtitle of list section - if it's a series of movies we want to capture the year
                    ttl = new_soup.find_previous(class_='mw-headline').text
                    ttl,yr = strip_title(ttl, False, True) 

                    # We only want to include the subtitle if it's the name of a movie or year of movie
                    excl = ['victims', 'deaths', 'during\sfilm', 'during\smovie', 'prior\sto']
                    if bool(re.search(r'|'.join(excl), ttl)):
                        ttl = None
                    
                    # Get characters
                    chars = new_soup.find_all('li')
                    for li in chars:
                        char = li.text
                        char = re.split('\s-', char)[0].strip()

                        # Instantiate character information
                        new_dict = {'Death List Index': i, 'Stripped Title (Page)':title, 'Stripped Title (Heading)': ttl, 'Year': yr, 'character': char}
                        dead_chars.append(new_dict)
                    
                    # Find next headline
                    new_soup = new_soup.find_next(class_='mw-headline')
                else:
                    # Find next headline
                    new_soup = new_soup.find_next(class_='mw-headline')
    
            # Instantiate character dataframe for movie
            deaths_df = pd.DataFrame(dead_chars, columns=['Death List Index', 'Stripped Title (Page)', 'Stripped Title (Heading)', 'Year', 'character'])
            deaths_df.index.names=['char index']
            deaths_df.set_index(['Death List Index', deaths_df.index], inplace=True)
        else:
            deaths_df = None

    return deaths_df

# Instantiate new characters dataframe for horror wiki
horror_deaths = pd.DataFrame()

# Append characters for each movie
for ind in horror_wiki.index.values:
    horror_deaths = pd.concat([horror_deaths, get_deaths(horror_wiki, ind, 'horror_wiki')])

# Add year column from horror_wiki_url dataframe and reorder columns
horror_deaths = horror_deaths.join(horror_wiki['Year'], on=['Horror Wiki Index'])
# Reorder columns
horror_deaths = horror_deaths[['Stripped Title', 'Year', 'character']]

# Instantiate new characters dataframe for list wiki
list_deaths = pd.DataFrame()

# Append characters for each movie
for ind in list_wiki.index.values:
    list_deaths = pd.concat([list_deaths, get_deaths(list_wiki, ind, 'list_wiki')])
    
# Save files
horror_deaths.to_csv(path.join(raw_data, 'h_horror_wiki_deaths_all.csv'))
list_deaths.to_csv(path.join(raw_data, 'h_list_wiki_deaths_all.csv'))