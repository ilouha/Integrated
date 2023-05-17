"create a table using panadas that has three columns and 6 rows and fill it with random numbers"
import pandas as pd
import numpy as np
import requests
from pprint import pprint
import requests
import json



def requestSoldHomesByZipcode(zipcode):

    url = "https://us-real-estate.p.rapidapi.com/v2/sold-homes-by-zipcode"

    querystring = {"zipcode":zipcode,"offset":"0","sort":"sold_date"}

    headers = {
        "X-RapidAPI-Key": "e46672b713mshd60dcfee7ec2085p1ea053jsn0b671ece2bc2",
        "X-RapidAPI-Host": "us-real-estate.p.rapidapi.com"
    }


    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    data = data['data']

    with open('./APIData/SoldHomes.json', 'w') as f:
        json.dump(data, f)

    #flatten the json file
    data = data['home_search']['results']

    #create a dataframe with the following columns : address, city, zipcode, Home_sqft, lot_size, sold_price
    

    #iterate through the json file 
    rows = []
    for item in data:

        try:
            address = item['location']['address']['line']
            city = item['location']['address']['city']
            zipcode = item['location']['address']['postal_code']
            Home_sqft = item['description']['sqft']
            lot_size = item['description']['lot_sqft']
            sold_price = item['description']['sold_price']
            ppsf = sold_price/Home_sqft

            #create a list of the variables above
            row = [address, city, zipcode, Home_sqft, lot_size, sold_price,ppsf]
            rows.append(row)

        except TypeError:
            #print('TypeError')
            pass

        # get the statistics of the sold price per square foot

    df = pd.DataFrame(rows,columns=['address', 'city', 'zipcode', 'Home_sqft', 'lot_size', 'sold_price','ppsf'])

    stats = df['ppsf'].describe()
    #convert stats which is a float64 to a json file
    #safe df as a csv file
    df.to_csv('./CompsCSV/SoldHomes.csv')
    return stats




