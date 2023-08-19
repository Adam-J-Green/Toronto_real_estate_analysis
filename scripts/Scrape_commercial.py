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


user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
commercial_dict = {'address':[], 'price':[], 'size':[], 'longitude':[], 'latitude':[]}
url1 = 'https://www.zolo.ca/toronto-real-estate/commercial-office'
driver1 = webdriver.Chrome()
driver1.get(url1)
content1 = driver1.page_source.encode('utf-8').strip()
bs1 = BeautifulSoup(content1, 'html.parser')
max_listings = bs1.find_all('strong')[1].get_text()
max_pages = (int(max_listings)//36)+1
for page in range(1, max_pages):
    url2 = 'https://www.zolo.ca/toronto-real-estate/commercial-office/page-' +str(page)
    driver2 = webdriver.Chrome()
    driver2.get(url2)
    content2 = driver2.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content2, 'html.parser')
    first_test = soup.find_all('div', {'class':'card-listing--details'})
    for item in first_test:
        commercial_dict['address'].append(item.find('span', {'class': 'street'}).get_text())
        try:
            commercial_dict['size'].append(item.find_all('li', {'class': 'xs-inline xs-mr1'})[1].get_text()).strip('sqft')
        except:
            commercial_dict['size'].append(None)
        try:
            commercial_dict['price'].append(item.find('span', {'itemprop':'price'}).get_text())
        except:
            commercial_dict['price'].append(None)
        commercial_dict['longitude'].append(item.find('meta', {'itemprop':'longitude'}).get('content'))
        commercial_dict['latitude'].append(item.find('meta', {'itemprop':'latitude'}).get('content'))

df = pd.DataFrame(commercial_dict)
df.to_csv('Commercial_listings.csv')
    








