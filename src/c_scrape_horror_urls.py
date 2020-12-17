# Scraping all Horror Film Wiki urls and all List of Deaths urls

import pandas as pd
import bs4
import requests
import re

# Import data paths
from os import path
from utilities import raw_data

# Collect all urls
# For Horror wikis: base = 'horror'
# For List of Death wikis: base = 'deaths'
def get_urls(base):
    
    # Instantiate data storage
    data = []

    if base == 'horror':
        pages = range(1970, 2021)
        # Finding horror movie list on Horror Fandom Wiki by year
        base_url = 'https://horror.fandom.com/'
        page_url = 'wiki/Category:{}_films'
    elif base == 'deaths':
        # Finding horror movie list on List of Deaths Wiki by first letter
        pages = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z', 'OTHER']
        base_url = 'https://listofdeaths.fandom.com/'
        page_url = 'wiki/Category:Horror_films?from={}'
    else:
        raise Exception('Invalid argument.')

    for page in pages:
        url = page_url.format(page)
        res = requests.get(base_url + url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Find all movies on the page
        cat_soup = soup.find_all(class_='category-page__member')
        
        # Collect title and url for each movie
        for item in cat_soup:
            txt = item.text.strip()
            lnk = item.find('a').get('href')

            if base == 'horror':
                new_dict = {'Title': txt, 'Year': page, 'Horror Wiki URL': lnk}
            elif base == 'deaths':
                new_dict = {'Title': txt, 'Death List URL': lnk}
            data.append(new_dict)
    
    df = pd.DataFrame(data)
    return df

# Collect URLS
death_list_urls = get_urls('deaths')
death_list_urls.index.names = ['Death List Index']
death_list_urls.to_csv(path.join(raw_data, 'c_death_list_urls_all.csv'))

horror_wiki_urls = get_urls('horror')
horror_wiki_urls.index.names = ['Horror Wiki Index']
horror_wiki_urls.to_csv(path.join(raw_data, 'c_horror_wiki_urls_all.csv'))