import requests
import pandas as pd 
import json

def getRentalDatePerZipcode(zipcode):

    url = "https://us-real-estate-listings.p.rapidapi.com/for-rent"
    #
    querystring = {"location":zipcode,"offset":"0","limit":"50"}
    #
    headers = {
        "X-RapidAPI-Key": "e46672b713mshd60dcfee7ec2085p1ea053jsn0b671ece2bc2",
        "X-RapidAPI-Host": "us-real-estate-listings.p.rapidapi.com"
    }

    #if there is a file with the name zipcode.json in the directory zipcodedata, read the file and return the data
    #check if file already exists in the directory



    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    #save the json file to a csv file
    with open('./APIData/RentalHomes.json', 'w') as f:
        json.dump(data, f)
    


    #flatten the json file
    data = data['listings']

    #create a dataframe with the following columns : address, city, zipcode, Home_sqft, lot_size, sold_price
    

    #iterate through the json file 
    rows = []
    for item in data:

        try:
            address = item['location']['address']['line']
            zipcode = item['location']['address']['postal_code']
            lot_size = item['description']['lot_sqft']
            Home_sqft = item['description']['sqft']
            rent_price = item['list_price']
            rpsf = rent_price/Home_sqft

            row = [address, zipcode, lot_size,Home_sqft, rent_price, rpsf]
            
            rows.append(row)


        except TypeError:
            pass

    df = pd.DataFrame(rows,columns=['address', 'zipcode', 'lot_sqft', 'Home_sqft', 'rent_price', 'rpsf'])

    #print(df)

    stats = df['rpsf'].describe()
    
    return stats
    




