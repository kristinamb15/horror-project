# Exploring Main Character Deaths in US Feature Film Horror Movies from 1970 to Present

Have you ever been curious about if and how race/ethnicity and gender of main characters relates to whether or not they survive a horror movie? I definitely am! I found that this data was not available on a large scale, so I decided to collect and analyze it.

**Language:** Python <br>
**Libraries for Scraping/Data Collection:** re, requests, bs4, pandas, numpy, os <br>
**Libraries for Data Visualization:** matplotlib, seaborn (optional), plotly (chart-studio), cufflinks

Data scraping initially began 2020-12-08.

## The Important Stuff

Here's the important stuff up front. If you want to read more about the methodology of the project, continue on!

To see the analysis of the data, you can view the [Analysis and Visualization notebook](https://nbviewer.jupyter.org/github/kristinamb15/horror-project/blob/main/notebooks/a_and_v.ipynb).

For super horror fans like myself, there is a bonus file of Christmas-related horror movies, created by querying the horror_movies dataframe for plots that include the word 'Christmas.' The script for this is not included, but it can be done as follows:

    movies = pd.read_csv('horror_movies.csv', index_col=0)
    xmas_movies = movies[movies['Plot'].str.contains('Christmas')]
    xmas_movies.to_csv('xmas_horror.csv')

### Licensing & Use

 - The files in this project are free for appropriate use under the MIT License (see [LICENSE.txt](LICENSE.txt)).
 - Public attribution is not required via the license, but if you use my code, it would be super rad to credit me for all this hard work.
 - You can download the .csv datasets if you wish to do your own analysis, rather than running the whole process to build the data.
 - If you wish to do so, you can run the scripts on your own, just be sure you have the appropriate libraries installed (see above). I found it best to run them one at a time to be sure that you have the datasets needed before moving on.

 ### Files

 The scripts and raw data files are prefixed with letters so that I could keep them in an organized order.

    📦HorrorProject
    ┣ 📂data
    ┃ ┣ 📂external                                  # Data files procured from external sources
    ┃ ┃ ┣ 📜casts.db
    ┃ ┃ ┗ 📜race_gender.csv                  
    ┃ ┣ 📂processed                                 # Final versions of data obtained from raw files
    ┃ ┃ ┣ 📜category_counts.csv                         # Killed vs not killed by category
    ┃ ┃ ┣ 📜death_list_urls.csv                         # List of Deaths Wikis information
    ┃ ┃ ┣ 📜horror_characters.csv                       # Main characters
    ┃ ┃ ┣ 📜horror_movies.csv                           # Big list of movies from IMDB
    ┃ ┃ ┣ 📜horror_wiki_deaths.csv                      # Character deaths obtained from Horror Wikis
    ┃ ┃ ┣ 📜horror_wiki_urls.csv                        # Horror Wikis information
    ┃ ┃ ┣ 📜list_wiki_deaths.csv                        # Character deaths obtained from List of Deaths Wikis
    ┃ ┃ ┗ 📜xmas_horror.csv                             # 🎄 Bonus file of Christmas-related horror movies
    ┃ ┗ 📂raw                                       # These files are numbered corresponding to the script that produced them
    ┃ ┃ ┣ 📜a_horror_movies_all.csv
    ┃ ┃ ┣ 📜b_horror_movies_clean_year.csv
    ┃ ┃ ┣ 📜c_death_list_urls_all.csv
    ┃ ┃ ┣ 📜c_horror_wiki_urls_all.csv
    ┃ ┃ ┣ 📜d_death_list_urls_stripped.csv
    ┃ ┃ ┣ 📜d_horror_movies_stripped.csv
    ┃ ┃ ┣ 📜d_horror_wiki_urls_stripped.csv
    ┃ ┃ ┣ 📜e_horror_movies_with_url.csv
    ┃ ┃ ┣ 📜f_horror_characters_all.csv
    ┃ ┃ ┣ 📜g_horror_characters_clean.csv
    ┃ ┃ ┣ 📜h_horror_wiki_deaths_all.csv
    ┃ ┃ ┣ 📜h_list_wiki_deaths_all.csv
    ┃ ┃ ┣ 📜i_horror_characters_stripped.csv
    ┃ ┃ ┣ 📜i_horror_wiki_deaths_stripped.csv
    ┃ ┃ ┣ 📜i_list_wiki_deaths_stripped.csv
    ┃ ┃ ┣ 📜j_horror_characters_with_deaths.csv
    ┃ ┃ ┣ 📜k_horror_characters_with_info.csv
    ┃ ┃ ┗ 📜m_horror_characters_updated.csv
    ┣ 📂notebooks                                       # Data analysis and visualizations
    ┃ ┗ 📜a_and_v.ipynb
    ┣ 📂src
    ┃ ┣ 📜a_scrape_imdb.py                             # Scrape horror movies from IMDB
    ┃ ┣ 📜b_clean_year.py                              # Remove movies with no year or year > 2020
    ┃ ┣ 📜c_scrape_horror_urls.py                      # Get horror wiki and list of death wiki urls
    ┃ ┣ 📜d_strip_titles.py                            # Strip movie titles for easier comparisons
    ┃ ┣ 📜e_update_movies_with_url.py                  # Update imbd movie list with horror wiki urls (where they exist)
    ┃ ┣ 📜f_create_char_df.py                          # Get all characters from horror wikis
    ┃ ┣ 📜g_clean_chars.py                             # Clean up character names
    ┃ ┣ 📜h_create_deaths_df.py                        # Collect all character deaths from horror wikis and list of death wikis
    ┃ ┣ 📜i_strip_chars.py                             # Strip character names for easier comparisons
    ┃ ┣ 📜j_check_deaths.py                            # Determine if characters were killed
    ┃ ┣ 📜k_scrape_race_gender.py                      # Find race/gender info of actors on NNDB
    ┃ ┣ 📜l_downloaded_data.py                         # Get race/gender information that exists elsewhere
    ┃ ┣ 📜m_update_race_gender.py                      # Update race/gender of actors
    ┃ ┣ 📜n_refactor_data.py                           # Get useful info for analysis
    ┃ ┣ 📜utilities.py                                  # Items that are used in other scripts
    ┃ ┗ 📜__init__.py
    ┣ 📜.gitattributes
    ┣ 📜.gitignore
    ┣ 📜LICENSE.txt
    ┗ 📜README.md
---

## Data Sources

 - Movie names and years:
     - [IMDB (custom search - see below)](www.imdb.com/search/title/?title_type=feature&release_date=1970-01-01,&genres=horror&countries=us&sort=release_date,asc&count=100)
 - Movie characters and death lists:
     - [Horror Film Wiki](https://horror.fandom.com/wiki/Horror_Film_Wiki)
     - [List of Deaths Wiki](https://listofdeaths.fandom.com/wiki/Category:Horror_films)
 - Actor race/ethnicity:
     - [NNDB](https://www.nndb.com/)
     - [Wikipedia - Category:Lists of actors by ethnicity](https://en.wikipedia.org/wiki/Category:Lists_of_actors_by_ethnicity)
 - Actor gender:
     - [NNDB](https://www.nndb.com/)
     - [Hollywood Diversity Git Repo](https://github.com/thomaslam/hollywood-diversity-dataviz)

---
## Data Collection
<br>

### **1. Collecting the Horror Movies**

    Files for this part of the process: 

        # Scrape movie data
        a_scrape_imdb.py
        >>  Creates file(s):
            a_horror_movies_all.csv
        
        # Remove movies with no year or year > 2020
        b_clean_year.py 
        >>  Creates file(s):
            b_horror_movies_clean_year.csv

- A search was performed on [IMDB](www.imdb.com/search/title/?title_type=feature&release_date=1970-01-01,&genres=horror&countries=us&sort=release_date,asc&count=100) with the following parameters:
    - Title Type: Feature Film
    - Release Date: 1970-01-01 to --
    - Genres: Horror
    - Countries: United States
    - Display: Detailed 100 per page sorted by Release Date Ascending

- Using requests and bs4 the following information for each movie was scraped (if available) from the search pages:
    - Title
    - Year
    - Plot
    - Director(s)
    - Star(s)

    **Note:** the plot given is a snapshot of the plot from the IMDB page of each movie and is generally not complete. Moreover, only Title and Year ended up being useful for our purposes.

- The scraped movie information was then put into a pandas dataframe with the columns named as above.

- Movies without a year listed and year greater than current year (2020) are removed.


### **2. Collecting Horror Wiki and List of Death Wiki Urls**

    Files for this part of the process: 

        # Find Horror Film Wiki/List of Death Wiki urls
        c_scrape_horror_urls.py
        >>  Creates file(s):
            c_horror_wiki_urls_all.csv
            c_death_list_urls_all.csv
        
        # Update movies and url dataframes with 'Stripped Title' column
        d_strip_titles.py             
        >>  Creates file(s):
            d_horror_wiki_urls_stripped.csv (horror_wiki_urls.csv)
            d_death_list_urls_stripped.csv (death_list_urls.csv)
            d_horror_movies_stripped.csv
        
        # Add Horror Wiki URLs to movie dataframe, in case character matching is desired
        e_update_movies_with_url.py             
        >>  Creates file(s):
            e_horror_movies_with_url.csv (horror_movies.csv)

- The [Horror Film Wiki](https://horror.fandom.com/wiki/Horror_Film_Wiki) was entirely scraped for movies from 1970 to 2020. A dataframe was created with the title, year, and url for the movie was created (horror_wiki_urls).

- The [List of Deaths Wiki](https://listofdeaths.fandom.com/wiki/Category:Horror_films) was entirely scraped (movies are arranged by title, not by year on this site). A data frame was created with the title and url for each movie (death_list_urls.

- Due to inconsistency in titles, a column of 'Stripped Title' was added to each the horror_wiki_urls, death_list_urls, and horror_movies. This will make comparing titles easier. For example, 'Leatherface: The Texas Chainsaw Massacre III' vs. 'Leatherface: Texas Chainsaw Massacre III.' The stripping process consisted of removing the year (if included), removing punctuation (except periods), removing the word 'the,' and returning the title lowercased. Since movies in the death_list_urls did not have a year associated to begin with, if a year was present in the title, it was included in a separate 'Year' column.

### **3. Collecting Movie Characters**

    Files for this part of the process: 

        # Collect actors/characters from each HorrorWiki
        f_create_char_df.py            
        >>  Creates file(s):
            f_horror_characters_all.csv
        
        # Clean up actor/character names
        g_clean_chars.py  
        >>  Creates file(s):
            g_horror_characters_clean.csv  

- The 'Cast' section of the Horror Wiki page for each film was scraped to collect characters. 

- The cast was generally list as '{actor} as '{character},' so the strings were split at 'as' and taken as actor and character, respectively. Due to inconsistency in formatting ('as' may have been replaced with '-' or '...' or other things), this data turned out to be pretty messy.

- For ease of organization, a new dataframe of characters was created. Since characters are taken exclusively from the horror wikis, the horror wiki index is included should joining of dataframes be desired.

- Actors with no character listed, and characters with no actor listed are removed. Actor/character names were also cleaned up. Some characters had desciptions attached, so attempted cleaning of those took place. <br>
An example from the movie *Dark Shadows (2012)*:

    > *Johnny Depp as Barnabas Collins, an 18th-century vampire who awakens...* <br>
    > was split to yield 'Johnny Depp' and 'Barnabas Collins'


### **4. Collecting Horror Movie Deaths**

    Files for this part of the process: 

        # Collect dead characters from each Horror Wiki and List of Deaths Wiki
        h_create_deaths_df.py
        >>  Creates file(s):
            h_horror_wiki_deaths_all.csv
            h_list_wiki_deaths_all.csv

        # Update death and character dataframes with 'stripped character' column
        i_strip_chars.py 
        >>  Creates file(s):
            i_horror_characters_stripped.csv
            i_horror_wiki_deaths_stripped.csv' (horror_wiki_deaths.csv)
            i_list_wiki_deaths_stripped.csv (list_wiki_deaths.csv)

- For ease of comparison, new dataframes for each of the horror wiki urls and list of death wiki urls were created, with all dead characters scraped from the pages. Indices from the corresponding url dataframes as well as stripped titles were included.

- In the list of death wiki, movies that are part of a series have all deaths on the same page, separated by movie title. For these pages, the movie titles were also scraped, stripped, and included.

- In every dataframe that includes character names, a column of stripped character names was included, in hopes that this will make comparison easier. The names were stripped similar to the titles (punctuation and 'the' removed).


### **5. Figuring out if the Character was Killed**

    Files for this part of the process: 

        # Compare characters to list of deaths on Horror Wiki
        j_check_deaths.py
        >>  Creates file(s):
            j_horror_characters_with_deaths.csv

- For each horror wiki index in the character dataframe, all deaths in the corresponding horror wiki deaths and list wiki deaths were collected, matched by stripped title and year.

- The list of deaths was then checked against the list of characters for that movie. A column for 'killed' was added to the character dataframe with a boolean value indicating if the character was killed or not.

- If a list of deaths did not exist for the movie, the 'killed' column was filled with 'N/A'.

- **Important Notes:**
    - It is assumed that those who are not explicitly found to be killed have survived.

    - It is important to note that this data may not be fully accurate. It's completely at the mercy of the language in the Horror Wikipedia. For example, in Friday the 13th (1980), the character name 'Mrs. Voorhees' was scraped, but 'Pamela Voorhees' is listed in the list of deaths. It was not adequate to check intersection of dead characters and character names, because in this instance, 'Jason Voorhees' was also a character. I personally edited this particular wiki entry to change 'Pamela Voorhees' to 'Mrs. Voorhees,' but I can't fix them all.

    - In the future, it would be fun to crowdsource the data to have a more complete picture - or to have a crew of horror aficionados diligently work on update the Horror Wiki.


### **6. Collecting Race and Gender of Actors**

    Files for this part of the process: 

        # Collect actor url/race/gender from NNDB (if available)      
        k_scrape_race_gender.py
        >>  Created file(s):
            k_horror_characters_with_info.csv

        # Obtaining and cleaning race/gender data found on GitHub
        l_downloaded_data.py
        >>  Created file(s):
            race_gender.csv

        # Missing race/gender added from obtained data (if available)
        m_update_race_gender.py
        >>  Created file(s):
            m_horror_characters_updated.csv (horror_characters.csv)

- Each actor was searched for on [NNDB](https://www.nndb.com/).

- A column for 'info url' was added to the character dataframe if the actor was found on NNDB.

- Columns for 'race' and 'gender' were added to the character dataframe. If an NNDB url was found for the actor, race and gender were found on that page. If not available, they were recorded as 'Unlisted.'

- I then found a wonderfully large database of actors with race/gender info from [a Git repo analyzing Hollywood diversity](https://github.com/thomaslam/hollywood-diversity-dataviz). This database was loaded as a dataframe and cleaned up (some races were listed as 'United States,' etc.). It is noted in the README file for the github repo that there are some challenges with this data (non-unique actor names, special characters, mismatched info from other sources), so this data may not be perfect.

- For actors in the character dataframe that have no NNDB url, the name was then compared to the downloaded information and updated accordingly.

- We make a critical assumption that each actor is portraying a character matching the race/gender that we have for that actor. This does not take into account actors that are playing 'movie monsters' that may have ambiguous genders, actors whose gender identities may have been changed or are not adequately reflected, and actors whose listed gender does not match the gender of their character.

- Until I found that race/gender database, I had planned to scrape IMDB and Wikipedia for this information. This could still be done for those that remain 'Unlisted.'

---

## Data Visualization

    Files for this part of the process: 

        # Preparing killed vs not killed by race and gender categories
        n_refactor_data.py
        >>  Created file(s):
            category_counts.csv
        
        # Discussion and visualizations
        analysis_and_visualization.ipynb

Data analysis and visualization was done in a Jupyter notebook, to easily see everything inline. See the [Analysis and Visualization notebook](https://nbviewer.jupyter.org/github/kristinamb15/horror-project/blob/main/notebooks/a_and_v.ipynb) for details.

---

## Conclusions

Is this project complete? Absolutely not!

This was my first solo jaunt into scraping and analyzing data - and I'm at the mercy of how well things match from one set of data to another.

There are many improvements to be made, but I learned a lot in the process!

In the end, I wound up with 1434 complete records (characters that had full information: race, gender, killed/not killed). Because there is still a lot of missing data, it's not fair to make general conclusions about all horror movies, but for a discussion of what I found in the data, see the link in the Data Visualization section above.

---

## Notes & Hindsight

 - Obviously, this process could have been shortened by just scraping the Horror Wiki Pages by year instead of starting with IMDB. However, I thought it would be nice to have larger data sets at the start, should other data on the movies be examined. For example, my original plan to get information on character deaths was to find the plot for each movie on Wikipedia and search the plot for specific words indicating character deaths. This would have been extremely challenging, and the idea was scrapped when I discovered that lists of horror movie deaths already existed.
 
 - The project evolved many times while in progress. Files changed, functions were added, so it's possible there is some unnecessarily repeated code that could be cleaned up.

 - Some functions and operations could be improved. I'm still new to data scraping, and while I found ways to get what I wanted, I'm sure there is plenty of room for improvement. A lot of cleaning happened as a response to browsing the data, noticing something strange, and adding a new line of code to deal with that issue.

 - Use of regex can be improved for better searching/cleaning of data. This data was very messy, due to inconsistency of source formatting. It's possible errors were introduced in data cleaning.

- There's no accounting for actors with the same name.

- While I did my best to match up movies by year, there could be some movies with the same title where errors were introduced in checking deaths. It's also possible that misspellings of actor/character/movie names resulted in matches not happening.

- It would be nice to write a script to update all the data files to add on titles for a specific year. This would be easy to do for IMDB and the Horror Wiki, but the List of Deaths Wiki was not sorted by year, so that could be challenging. 