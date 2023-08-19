import pandas as pd
import numpy as np

listings = pd.read_csv('Listings.csv')
locations = pd.read_csv("Locations.csv")
print(locations.info())
print(locations)
locations.drop_duplicates(inplace=True)
listings.drop_duplicates(inplace = True)
joined = pd.merge(listings, locations, how = 'inner')

joined.drop(['Unnamed: 0'], axis = 1, inplace = True)

split = [x.split('-') for x in joined['price']]
ids = []
count = 0
for item in split:
    if len(item)>1:
        ids.append(count)
    count +=1

reduced = joined.drop(ids)
reduced.drop_duplicates(inplace = True)
print(reduced)
print(reduced.info())
print(reduced.info())
reduced.to_csv("Listings_wlocations_full.csv")

