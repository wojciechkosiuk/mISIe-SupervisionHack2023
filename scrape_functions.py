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