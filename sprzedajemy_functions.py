import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
from scrape_functions import *


def scrape_sprzedajemy_links():
    #eta 35min
    keep_working = True
    offset=0
    offers_list = []
    while keep_working:
        url = f"https://sprzedajemy.pl/praca?offset={offset}"
        try:
            soup = return_soup(url)
            offers = soup.find_all("a", {"class" : "offerLink"})
            for offer in offers:
                offers_list.append(offer.attrs['href'])
            offset+=30
        except:
            keep_working=False

    with open('data/links_sprzedajemy.txt', 'w') as f:
        for link in list(set(offers_list)):
            f.write("%s\n" % link)


aas_ = {
    'Lokalizacja' : "locationName",
    "user-profile-link" : "user-offers-link"
}

spans = {
    "title" : "isUrgentTitle",
    "pay_period" : "grossNetLabel"
}

divs = {
    "description" : "offerDescription",
    "category-tree-item" : "cntPath clearfix"
}
itemprop = {
    "price" : "price",
}

dict_  = {
    'dodane-data' : '',
    'id' : '',
    'title' : '',
    'category-tree-item' : '',
    'user-profile-link' : '',
    'filters':'',
    'description' : '',
    'pay_low' : '',
    'pay_high' : '',
    'pay_currency' : '',
    'pay_period' : '',
    'Lokalizacja' : '',
    "Wymiar pracy" : '',
    "Typ umowy" : '',
}

def get_info_about_job_sprzedajemy(url):
    url = f"https://sprzedajemy.pl{url}"
    soup = return_soup(url)

    for key, value in aas_.items():
        try:
            if key == 'user-profile-link':
                dict_[key] = soup.find("a", {"class" : value}).attrs['href']
            else:
                dict_[key] = soup.find("a", {"class" : value}).text
        except Exception as e:
            dict_[key] = ''
            continue

    for key, value in spans.items():
        try:
            dict_[key] = soup.find("span", {"class" : value}).text
        except Exception as e:
            dict_[key] = ''
            continue
        
    for key, value in divs.items():
        try:
            if key == 'category-tree-item':
                children = soup.find("div", {"class" : value}).find_all("a")
                categories = []
                for child in children:
                    categories.append(child.attrs['title'])
                dict_[key] = "/".join(categories)

            else:
                dict_[key] = soup.find("div", {"class" : value}).text
        except Exception as e:
            dict_[key] = ''
            continue

    price_tag = "price"
    try:
        pay_bracket = soup.find("span", {"itemprop" : price_tag}).text.strip()
        pay_currency = pay_bracket.split(' ')[-1]
        if "-" in pay_bracket:
            pay_low = ''.join(filter(lambda x: x.isdigit() or x in [',', '.'], pay_bracket.split("-")[0]))
            pay_high = ''.join(filter(lambda x: x.isdigit() or x in [',', '.'], pay_bracket.split("-")[1]))
        else:
            pay_low = ''.join(filter(str.isdigit, pay_bracket))
            pay_high = ''.join(filter(str.isdigit, pay_bracket))
        dict_['pay_low'] = pay_low
        dict_['pay_high'] = pay_high
        dict_['pay_currency'] = pay_currency
    except Exception as e:
        dict_['pay_low'] = ''
        dict_['pay_high'] = ''
        dict_['pay_currency'] = ''

    try:
        wymiar_pracy = soup.find("ul", {"class" : "attribute-list"}).find_all("li")
        wymiary = []
        for wymiar in wymiar_pracy[1:]:
            try:
                wymiary.append(wymiar.find("strong").text.strip())
            except Exception as e:
                continue
        dict_["Wymiar pracy"] = "/".join(wymiary)
    except Exception as e:
        dict_["Wymiar pracy"] = ''

    offerAdditionalInfo = "offerAdditionalInfo"
    info = soup.find("ul", {"class" : offerAdditionalInfo}).find_all("li")
    try:
        dict_["dodane-data"] = info[-2].text
        dict_["id"] = int(''.join(filter(str.isdigit, info[-1].text)))
    except Exception as e:
        pass

    typ_umowy = "additional-parameters"
    umowa = soup.find("ul", {"class" : typ_umowy}).find_all("span")
    umowy = []
    for um in umowa:
        umowy.append(um.text.strip())
    "/".join(umowy)
    dict_["Typ umowy"] = "/".join(umowy)
    return pd.DataFrame(dict_, index=[0])

def sprzedajemy_date(data):
    date_dict = {
        "Sty": "01",
        "Lut": "02",
        "Mar": "03",
        "Kwi": "04",
        "Maj": "05",
        "Cze": "06",
        "Lip": "07",
        "Sie": "08",
        "Wrz": "09",
        "Paź": "10",
        "Lis": "11",
        "Gru": "12",
    }
    data = data.split(" ")
    data[1] = date_dict[data[1]]
    data[2] = str(datetime.datetime.now().year)
    data = "-".join(data)
    return data


def adjust_sprzedajemy_df(df):
    df["dodane-data"] = df["dodane-data"].apply(sprzedajemy_date)
    df["user-profile-link"] = df["user-profile-link"].apply(lambda x: f"https://sprzedajemy.pl{x}")
    return df