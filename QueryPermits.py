#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:

def NewBuildingPermits(zipcode,zone):
    
    client = Socrata("data.lacity.org", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.lacity.org,
    #                  MyAppToken,
    #                  username="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.

    results = client.get("8cf2-izs5",limit=2000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    print(results_df.head())

    #select all the information where zipcode is 90012 and zone contains C2
    results_df = results_df.loc[(results_df['zip_code'] == zipcode) & (results_df['zone'].str.contains(zone))]

    #print all column names in the dataframe
    print(results_df.columns)

    list_columns_keep = [

        'zip_code',
        'floor_area_l_a_building_code_definition',
        'zone',
        'permit_sub_type',
        'pcis_permit',
        'permit_type',
        'occupancy',
        'valuation',
        'issue_date',
        'work_description'

    ]
    #keep only the columns from list_columns_keep in the dataframe
    results_df = results_df[list_columns_keep]

    return results_df


zipcode = '90043'
zone = 'C'

df = NewBuildingPermits(zipcode,zone)

print(df['pcis_permit'])
print(df['issue_date'])