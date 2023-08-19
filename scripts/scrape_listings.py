import random
import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#options = webdriver.ChromeOptions()
#options.add_argument("--disable-popup-blocking")

def get_coords(site):
    user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
    r = requests.get(site, headers=user_agent)
    soup = BeautifulSoup(r.content, 'html.parser')
    listings = soup.find_all('div')
    listings = listings[0].find_all('script')[2:]
    lat = []
    long = []
    add = []
    for place in listings:
        list_listings = place.get_text().split(',')
        for item in list_listings:
            if re.search('latitude', item):        
                sub_list = item.split(':')
                lat.append(sub_list[1].strip(' \n"}'))
            if re.search('longitude', item):
                sub_list = item.split(':')
                long.append(sub_list[1].strip(' \n"}'))
            if re.search('streetAddress', item):
                sub_list = item.split(':')
                add.append(sub_list[1].strip(' \n}"'))
    return long, lat, add

def get_house_details_rentals(site):
    '''Gather housing details for rentals.ca'''
    #page_init = soup.find('li', {'class':'pagination__item pagination__item--active'}).get_text()
    current_page = 1
    houses_dict = {'price':[], 'address': [], 'beds':[], 'baths':[], 'size':[]}
    locs = {"longitude": [], 'latitude': [], 'address':[]}
    pages = []
    driver = webdriver.Chrome()
    driver.get(site)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    max_listings = soup.find('strong').get_text().split(" ")[0]
    max_pages = (int(str(max_listings))//10 + 1)
    for i in range(max_pages):
            page_url = str(site + "&p="+str(i))
            driver = webdriver.Chrome()
            driver.get(page_url)
            time.sleep(5)
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, 'html.parser')
            rows = soup.find_all('div', {'class':'listing-card__details'})
            for row in rows:
                add = row.find('h2', {'class':'listing-card__title'}).get_text().strip(" ON \n")[:-11]
                p = row.find('p', {'class':'listing-card__price'}).get_text().strip("$ \n")
                main_feat = row.find('ul', {'class':'listing-card__main-features'})
                traits = main_feat.find_all('li', {'class': ''})
                bed =  traits[0].get_text().strip("Bed \n")
                bath = traits[1].get_text().strip("Bath \n")
                try:
                    ft = traits[2].get_text().strip(" \n")[:-3]
                except:
                    ft = None
                houses_dict['price'].append(p)
                houses_dict['beds'].append(bed)
                houses_dict['address'].append(add)
                houses_dict['baths'].append(bath)
                houses_dict['size'].append(ft)
            long, lat, address = get_coords(page_url)
            locs['longitude']+= long
            locs['latitude']+= lat
            locs['address'] += address
    locations_df = pd.DataFrame(locs)
    houses = pd.DataFrame(houses_dict)
    return houses, locations_df
        
houses_df, locations_df = get_house_details_rentals('https://rentals.ca/toronto?bbox=-79.74518,43.53896,-79.10935,43.81359')
houses_df.to_csv("Listings.csv")
locations_df.to_csv('Locations.csv')                  
