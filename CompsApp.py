import json
import pandas as pd
import numpy as np
import requests
from pprint import pprint

import os

from ReadRentPricesData import getRentalDatePerZipcode
from ReadSoldPricesData import requestSoldHomesByZipcode

zipcode = '90035'

rental_stats = getRentalDatePerZipcode(zipcode)
sale_states = requestSoldHomesByZipcode(zipcode)

#merge two dataframes together
df = pd.concat([rental_stats, sale_states], axis=1)

# save the df to a json file under the folder Zipcodedata
if not os.path.exists('./ZipcodeData'):
    os.makedirs('./ZipcodeData')

#convert the df to json

json = df.to_json()

#add the json a key with the name zipcode and the value is the dataframe
json = '{"' + zipcode + '":' + json + '}'

#save the json to a file
with open('./ZipcodeData/' + zipcode + '.json', 'w') as f:
    f.write(json)

print(df)

#save the df to a csv file
df.to_csv('./ZipcodeData/' + zipcode + '.csv', sep=',', encoding='utf-8')
#save the df to a json file
df.to_json('./ZipcodeData/' + zipcode + '.json', orient='records')
