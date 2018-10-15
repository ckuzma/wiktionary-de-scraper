## Built-in libraries
import json
import requests
import sys

## Additional libraries
from bs4 import BeautifulSoup

## Where we are finding our words
BASE_URL = 'https://de.wiktionary.org'
NEXT_WORD = 'nächste'
SAVE_LOCATION = './words_de.json'

## Word prefixes we want to ignore
IGNORE_PREFIXES = ['!', '\"', '$', '%', '%s', '&', '\'', '*', '-', '+', '.', '/']

def get_page_parsed(url_route):
    try:
        print('Opening page (' + BASE_URL + url_route + ')')
        page_html = requests.get(BASE_URL + url_route).text
        return BeautifulSoup(page_html, 'html.parser')
    except:
        print('ERROR: Unable to fetch and parse URL (' + BASE_URL + url_route + ')')
        return False

def scrape_words_from_index(soup):
    word_list = []
    try:
        for dictionary_entry in soup.find_all('ul', {'class': 'mw-allpages-chunk'}):
            for word in dictionary_entry.find_all('li'):
                if word.text[0] not in IGNORE_PREFIXES:
                    word_list.append(word.text)
    except:
        print('ERROR: Unable to extract words from page')
    print('Found ' + str(len(word_list)) + ' words on the page...')
    return word_list

def get_next_index_page(soup):
    try:
        next_link = None
        nav_links = soup.find("div", {"class": "mw-allpages-nav"})
        for link in nav_links.findAll('a'):
            if NEXT_WORD in link.text.lower():
                next_link = link['href']
                print(BASE_URL + next_link)
        return next_link
    except:
        print('ERROR: Unable to get next page')
        return False

def write_wordlist_to_file(wordlist):
    raw = open(SAVE_LOCATION, 'w')
    raw.write(json.dumps(wordlist, indent=2))
    raw.close()
    
if __name__ == '__main__':
    try:
        start_route = sys.argv[1]
        word_list = []
        get_next_page = True
        while get_next_page == True:
            soup = get_page_parsed(start_route)
            word_list += scrape_words_from_index(soup)
            write_wordlist_to_file(word_list)
            start_route = get_next_index_page(soup)
    except:
        print('\n\tERROR: Invalid input params given!')
        print('\n\tUsage:')
        print('\tpython3 ' + sys.argv[0] + ' <wiktionary_route>')
        print('\n\tExample:')
        print('\tpython3 ' + sys.argv[0] + ' /wiki/Spezial:Alle_Seiten\n')