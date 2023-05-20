import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np

def return_soup(url):
    start = time.time()
    response = requests.get(url)
    end = time.time()
    html_content = response.content
    print(f"czas requesta: {end - start}")
    print("")

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def save_url_to_html(url, filename):
    # current date and time
    
    # save to html
    soup = return_soup(url)
    with open(f'htmls/{datetime.datetime.now().date()}-{filename}.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))