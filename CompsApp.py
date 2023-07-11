import json
import pandas as pd
import numpy as np
import requests
from pprint import pprint
import os

from ReadRentPricesData import getRentalDatePerZipcode
from ReadSoldPricesData import requestSoldHomesByZipcode

def format_to_dollar_price(value):
    if isinstance(value, (int, float)):
        formatted_value = "${:,.2f}".format(value)
    elif isinstance(value, str):
        # Remove any non-numeric characters
        value = ''.join(filter(str.isdigit, value))
        if value:
            formatted_value = "${:,.2f}".format(float(value)/100)
        else:
            formatted_value = "$0.00"
    else:
        raise TypeError("Unsupported value type. Only int, float, and str are supported.")
    
    return formatted_value

def process_zipcode_data(zipcode):
    
    rental_stats = getRentalDatePerZipcode(zipcode)
    sale_stats = requestSoldHomesByZipcode(zipcode)

    # Merge two dataframes together
    df = pd.concat([rental_stats, sale_stats], axis=1)

    # Save the df to a json file under the folder ZipcodeData
    if not os.path.exists('./ZipcodeData'):
        os.makedirs('./ZipcodeData')

    # Convert the df to json
    json_data = df.to_json()

    # Add the json as a key with the name 'zipcode' and the value is the dataframe
    json_data = '{"' + str(zipcode) + '":' + json_data + '}'

    # Save the json to a file
    with open('./ZipcodeData/' + str(zipcode) + '.json', 'w') as f:
        f.write(json_data)

    df_dict = df.to_dict(orient='index')

    dic = {

        "avg_rent_per_sf":  df_dict['mean']['rpsf'],
        "avg_sale_per_sf": df_dict['mean']['ppsf'],
        "high_tier_sale_per_sf": df_dict['75%']['ppsf'],
        "high_tier_rent_per_sf": df_dict['75%']['rpsf'],
        "mid_tier_sale_per_sf": df_dict['50%']['ppsf'],
        "mid_tier_rent_per_sf": df_dict['50%']['rpsf'],
        "low_tier_sale_per_sf": df_dict['25%']['ppsf'],
        "low_tier_rent_per_sf": df_dict['25%']['rpsf']

    }

    #for key, value in dic.items():
    #    dic[key] = format_to_dollar_price(value) 
    
    #open json file data.json in write mode

    #pprint(dic)

    #with open('data.json') as f:
    #    data = json.load(f)

    #data['json_schema']['statistics'] = dic
    #data['json_schema']['general_information']['zipcode'] = zipcode

    #save the json file
    #with open('data.json', 'w') as outfile:
    #    json.dump(data, outfile)

    return dic

if __name__ == "__main__":
# Example usage
    zipcode = '91325'
    print(process_zipcode_data(zipcode))
