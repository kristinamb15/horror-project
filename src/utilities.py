# Functions that get used in other files

import re

# Paths
from os import path
raw_data = path.abspath('data/raw')
proc_data = path.abspath('data/processed')
ext_data = path.abspath('data/external')

# Function to strip movie titles
def strip_title(title, yr=False, astup=False):
    ttl = title
    
    # Separate title and year if together
    # r is looking for a group of four digits, possibly enclosed in parentheses,
    # not at the beginning of a string, not followed by a word, not preceded by a '-', and not preceded/followed by a '/'
    pattern = re.compile(r'(?<!^)(?<!-\s)(?<!\/)(\(?\d{4}\)?)(?!\s\w+)(?!\/)')
    spl = re.split(pattern, ttl)
    ttl = spl[0].strip()
    if len(spl) > 1:
        year = spl[1].strip().strip('()').strip("'s")
    else:
        year = None
    
    # Strip apostrophes:
    ttl = ttl.replace("'", '')
    # Strip punctuation and 'the'
    ttl = ' '.join(re.findall(r'(?!the\b)\b\w+', ttl, re.IGNORECASE))

    if yr:
        return {'Stripped Title': ttl.lower(), 'Year': year}
    elif astup:
        return (ttl.lower(), year)
    else:
        return ttl.lower()

# Function to strip character names
def strip_name(name):
    name = str(name)
    
    # Remove periods and quotation marks
    name = re.sub(r'\.|"', '', name)

    # Remove apostrophes:
    name = name.replace("'", '')

    # Remove punctuation and 'the'
    name = ' '.join(re.findall(r'(?!the\b)\b\w+', name, re.IGNORECASE))

    return name.lower()