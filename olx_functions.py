import requests
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
import numpy as np
from scrape_functions import *


categories = {"administracja-biurowa",
"badania-rozwoj",
"budowa-remonty",
"dostawca-kurier-miejski",
"e-commerce-handel-internetowy",
"edukacja",
"energetyka",
"finanse-ksiegowosc",
"franczyza-wlasna-firma",
"fryzjerstwo-kosmetyka",
"gastronomia",
"hr",
"hostessa-roznoszenie-ulotek",
"hotelarstwo",
"inzynieria",
"informatyka",
"kierowca",
"logistyka-zakupy-spedycja",
"marketing-pr",
"mechanika-lakiernictwo",
"montaz-serwis",
"kadra-kierownicza",
"praktyki-staze",
"praca-dodatkowa-sezonowa",
"zdrowie",
"sprzatanie",
"rolnictwo-i-ogrodnictwo",
"produkcja",
"pracownik-sklepu",
"prace-magazynowe",
"praca-za-granica",
"ochrona",
"obsulga-klienta-call-center"}

month_dict = {
    'stycznia': "01",
    'lutego': "02",
    'marca': "03",
    'kwietnia': "04",
    'maja': "05",
    'czerwca': "06",
    'lipca': "07",
    'sierpnia': "08",
    'września': "09",
    'października': "10",
    'listopada': "11",
    'grudnia': "12",
    
}

#class
ps = {
   # 'pay':'css-1sq4nww',
    'basic-info-pay' : 'css-1sq4nww',
    'basic-info-other-desc' : 'css-1kajzj',
    'basic-info-other' : 'css-1jy76qt',
     
}

divs = {
    'description' : 'css-19srbbu',
}

a_s = {
    'user-profile-link' : 'user-profile-link' # data-testid
}

spans = {
    'dodane-data':'css-hn8jea',
    'id' : 'css-12hdxwj er34gjf0',  # pierwsza linijka ID:
    'filters' : "css-zehgpe"
}

h1s = {
    'title':'css-tcqyb',
}

lis = {
    'category-tree-item':'css-7dfllt'
}



# function to remove Dodane from dodane-data
def remove_dodane(x):
    return x.replace('Dodane ', '')

# function to convert dodane-data to datetime
def convert_to_datetime(x):
    x = x.split()
    final_date = ""
    if x[0] == "Dzisiaj":
        final_date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        final_date = f"{x[2]}-{month_dict[x[1]]}-{x[0]}"  
    return final_date  

# function to remove ID: from id
def remove_id(x):
    return x.replace('ID:', '')

# function to remove OPIS from beginning of description (only check first 4 symbols)
def remove_opis(x):
    if x[:4] == 'OPIS' or x[:4] == 'Opis' or x[:4] == 'opis': 
        return x[4:]
    else:
        return x

# add "https://www.olx.pl" to link unless it starts with "https://" or "http://"
def add_olx(x):
    # break if x is None
    if x is None or x == "None" or x == "" or x == "NaN":
        return x
    if x[:8] == 'https://' or x[:7] == 'http://':
        return x
    else:
        return f"https://www.olx.pl{x}"

# funtion to hash url
def hash_url(x):
    return hash(x)

def replace_commas(x):
    return x.replace(',', '.')

def convert_str_to_float(x):
    return float(x)


def get_info_about_job_olx(url):
    soup = return_soup(url)

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


    for key, span in spans.items():
        try:
            if key == "filters":
                fils = soup.find_all('span', {'class': span})
                filters = []
                for fil in fils:
                    filters.append(fil.text)
                joined = '/'.join(filters)
                dict_[key] = joined
            else:
                dict_[key] = soup.find('span', {'class': span}).text
        except AttributeError:
            dict_[key] = None

    for key, h1 in h1s.items():
        try:
            dict_[key] = soup.find('h1', {'class': h1}).text
        except AttributeError:
            dict_[key] = None

    for key, li in lis.items():
        try:
            cat = soup.find_all('li', {'class': li})
            categories = []
            for c in cat:
                categories.append(c.text)

            categories = '/'.join(categories)
            dict_[key] = categories
        except AttributeError:
            dict_[key] = None

    for key, a in a_s.items():
        try:
            dict_[key] = soup.find('a', {'data-testid': a}).attrs['href']
        except (AttributeError, KeyError):
            dict_[key] = None

    for key, div in divs.items():
        try:
            dict_[key] = soup.find('div', {'class': div}).text
            
        except AttributeError:
            dict_[key] = None

    try:
        pay_ = soup.find('p', ps['basic-info-pay']).text
        pay_bracket = pay_.split('/')[0]
        pay_period = pay_.split('/')[1]
        pay_currency = pay_bracket.rstrip().split(" ")[-1]
        if "-" in pay_bracket:
            pay_low = ''.join(filter(lambda x: x.isdigit() or x in [',', '.'], pay_bracket.split("-")[0]))
            pay_high = ''.join(filter(lambda x: x.isdigit() or x in [',', '.'], pay_bracket.split("-")[1]))
        else:
            pay_low = ''.join(filter(str.isdigit, pay_bracket))
            pay_high = ''.join(filter(str.isdigit, pay_bracket))
        dict_['pay_low'] = pay_low
        dict_['pay_high'] = pay_high
        dict_['pay_currency'] = pay_currency
        dict_['pay_period'] = pay_period
    except AttributeError:
        pass
    try:


        descs = soup.find_all('p', ps['basic-info-other-desc'])
        others = soup.find_all('p', ps['basic-info-other'])
       # print(descs)
        #print(others)
        if len(descs) != len(others):
            descs = descs[1:]
        for desc, other in zip(descs, others):
            dict_[desc.text] = other.text
    except AttributeError as e:
        print(e)

   # return dict_

    dejtafrejm = pd.DataFrame(dict_, index=[0])
    return dejtafrejm
 


def adjust_olx_df(df):

    try:    # remove Dodane from dejtafrejm['dodane-data']
        df['dodane-data'] = df['dodane-data'].apply(remove_dodane)
    except:
        print('Error in removing Dodane from df["dodane-data"]')
    try: # convert dodane-data to datetime
        df['dodane-data'] = df['dodane-data'].apply(convert_to_datetime)
    except:
        print('Error in converting df["dodane-data"] to datetime')

    try:# remove ID: from dejtafrejm['id']
        df['id'] = df['id'].apply(remove_id)
    except:
        print('Error in removing ID: from df["id"]')

    try:# remove OPIS from beginning of description (only check first 4 symbols)
        df['description'] = df['description'].apply(remove_opis)
    except:
        print('Error in removing OPIS from df["description"]')

    try:
        df['user-profile-link'] = df['user-profile-link'].apply(add_olx)
    except:
        print('Error in adding olx.pl to df["user-profile-link"]')

    try:
        df['user-profile-link-hash'] = df['user-profile-link'].apply(hash_url)
    except:
        print('Error in hashing df["user-profile-link"]')

    try:
        df['pay_low'] = df['pay_low'].apply(replace_commas)
        df['pay_low'] = df['pay_low'].apply(convert_str_to_float)

        df['pay_high'] = df['pay_high'].apply(replace_commas)
        df['pay_high'] = df['pay_high'].apply(convert_str_to_float)
    except:
        print('Error in converting pay_low and pay_high to float')
    
    # add olx to beginning of id
    df['id'] = df['id'].apply(add_olx)
    
    return df

    




def scrape_olx_links():
    links = []

    for i in range(1, 26):
        url = f'https://www.olx.pl/praca/?page={i}'
        soup = return_soup(url)
        #print(soup)
        for link in soup.find_all('a', {'class': "css-rc5s2u"}):
            links.append(link.attrs['href'])
        
    for category in categories:
        for i in range(1, 26):
            print(category, i)
            url = f'https://www.olx.pl/praca/{category}/?page={i}'
            try:
                soup = return_soup(url)
            except:
                continue
            #print(soup)
            for link in soup.find_all('a', {'class': "css-rc5s2u"}):
                links.append(link.attrs['href'])

    # write to file
    links = set(links)
    with open('links_all.txt', 'w') as f:
        for link in links:
            f.write("%s\n" % link)




