# Scraping IMDB to find all US feature films of horror genre from 1970-01-01 to the present (2020-12-08)

import requests
import bs4
import pandas as pd
import re

from os import path
from utilities import raw_data

# IMDB base url and first page of search results
imdb_base_url = 'https://www.imdb.com'
page = '/search/title/?title_type=feature&release_date=1970-01-01,&genres=horror&countries=us&sort=release_date,asc&count=100'

# Initialize storage of data
horror_data = []

# Loop runs as long as 'Next page' link is available
while True:
    # Get the full page url
    res = requests.get(imdb_base_url + page)
    
    # Select page html
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # Select all movie containers on the page
    movies = soup.select('.lister-item-content')

    # Collect data for each movie on the page
    for movie in movies:
        #If data was not available, 'None' was collected
        # Collect title
        if movie.find('a', href=re.compile('^\/title')):
            title = movie.find('a', href=re.compile('^\/title')).text
        else:
            title = None

        # Collect year    
        if movie.find('span', class_='lister-item-year'):
            year_text = movie.find('span', class_='lister-item-year').text
            if re.search('\d{4}', year_text):
                year = re.search('\d{4}', year_text).group()
            else:
                year = None
        else:
            year = None
        
        # Collect plot
        if movie.select('p', class_='text-muted')[1]:
            plot = movie.select('p', class_='text-muted')[1].text.strip()
        else:
            plot = None
        
        # Collect director(s)
        # Director(s) and Star(s) were stored within the same tag with no identifying class/id names, so names before the word 'Stars' were colleced as directors, names after collected as stars
        if movie.find(text=re.compile('Directors?')) and movie.find(text=re.compile('Stars?')):
            directors = ', '.join([item.text for item in movie.find(text=re.compile('Stars?')).find_previous_siblings('a')])
        else:
            director = None
        
        # Collect Stars
        if movie.find(text=re.compile('Stars?')):
            stars = ', '.join([item.text for item in movie.find(text=re.compile('Stars?')).find_next_siblings('a')])
        else:
            stars = None

        # Compile movie info
        movie_data = [title, year, plot, directors, stars]

        # Append movie info to entire dataset
        horror_data.append(movie_data)
    
    # If a 'Next page' link is available, get the url and repeat loop, or end loop
    if soup.select('.next-page'):        
        page = soup.find(class_='next-page').get('href')
    else:
        break

# Create data frame from collected data
columns = ['Title', 'Year', 'Plot', 'Director(s)', 'Star(s)']
horror_movies = pd.DataFrame(horror_data, columns = columns)
horror_movies.index.names = ['Movie Index']

# Let's save this bad boy to file
# Optional: add index=False to not save index column
horror_movies.to_csv(path.join(raw_data, 'a_horror_movies_all.csv'))