print("Hello.. starting web scraping..")

import requests
from bs4 import BeautifulSoup

from query_reader import read_search_query_from_json_file
from scraper import scraper
 
# Making a GET request

HEADERS = ({'User-Agent':
           'Mozilla/5.0 (X11; Windows x86_64) ' +
           'AppleWebKit/537.36 (KHTML, like Gecko)' + 
                    'Chrome/44.0.2403.157 Safari/537.36',
                           'Accept-Language': 'en-US, en;q=0.5'})



def __main__():
    search_query = read_search_query_from_json_file()
    
    product_list = scraper(search_query, 20, HEADERS).scrape()

   
__main__()

