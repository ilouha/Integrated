#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
import json

field_names = [
    "Assessor Book",
    "Assessor Page",
    "Assessor Parcel",
    "Tract",
    "Block",
    "Lot",
    "Reference # (Old Permit #)",
    "PCIS Permit #",
    "Status",
    "Status Date",
    "Permit Type",
    "Permit Sub-Type",
    "Permit Category",
    "Project Number",
    "Event Code",
    "Initiating Office",
    "Issue Date",
    "Address Start",
    "Address Fraction Start",
    "Address End",
    "Address Fraction End",
    "Street Direction",
    "Street Name",
    "Street Suffix",
    "Suffix Direction",
    "Unit Range Start",
    "Unit Range End",
    "Zip Code",
    "Work Description",
    "Valuation",
    "Floor Area-L.A. Zoning Code Definition",
    "# of Residential Dwelling Units",
    "# of Stories",
    "Contractor's Business Name",
    "Contractor Address",
    "Contractor City",
    "Contractor State",
    "License Type",
    "License #",
    "Principal First Name",
    "Principal Middle Name",
    "Principal Last Name",
    "License Expiration Date",
    "Applicant First Name",
    "Applicant Last Name",
    "Applicant Business Name",
    "Applicant Address 1",
    "Applicant Address 2",
    "Applicant Address 3",
    "Zone",
    "Occupancy",
    "Floor Area-L.A. Building Code Definition",
    "Census Tract",
    "Latitude/Longitude"
]

field_maintain = [

    "Assessor Book",
    "Assessor Page",
    "Assessor Parcel",
#    "Lot",
    "PCIS Permit #",
    "Status",
    "Status Date",
    "Permit Type",
    "Permit Sub-Type",
    "Permit Category",
#    "Project Number",
    "Issue Date",
    "Address Start",
    "Address Fraction Start",
    "Address End",
    "Address Fraction End",
    "Street Direction",
    "Street Name",
    "Street Suffix",
    "Suffix Direction",
    "Unit Range Start",
    "Unit Range End",
    "Zip Code",
    "Work Description",
    "Valuation",
    "Floor Area-L.A. Zoning Code Definition",
    "# of Residential Dwelling Units",
    "# of Stories",
    "Contractor's Business Name",
#    "Contractor Address",
#    "Contractor City",
#    "Contractor State",
#    "License Type",
#    "License #",
#    "Principal First Name",
#    "Principal Middle Name",
#    "Principal Last Name",
#    "License Expiration Date",
#    "Applicant First Name",
#    "Applicant Last Name",
#    "Applicant Business Name",
    "Zone",
#    "Occupancy",
    "Floor Area-L.A. Building Code Definition",
    "Latitude/Longitude"
]

#function to remove duplicate words in a string

def remove_duplicates(string):
    words = string.split()
    unique_words = list(dict.fromkeys(words))
    result = ' '.join(unique_words)
    return result

def concat_address(row):
    address = str(row['Address Start']) + ' ' + str(row['Address Fraction Start']) + ' ' + str(row['Address End']) + ' ' + str(row['Address Fraction End']) + ' ' + str(row['Street Direction']) + ' ' + str(row['Street Name']) + ' ' + str(row['Street Suffix']) + ' ' + str(row['Suffix Direction']) + ' ' + str(row['Unit Range Start']) + ' ' + str(row['Unit Range End'])
    
    #if address has string 'nan' then replace with empty string
    if 'nan' in address:
        address = address.replace('nan', '')
    
    #remove duplicate words in the address
    address = remove_duplicates(address)

    return address     

def add_zeros(string):
    while len(string) < 3:
        string = '0' + string
    return string

def concat_assessor(row):
    

    row['Assessor Page']  = add_zeros(str(row['Assessor Page']))
    row['Assessor Parcel'] = add_zeros(str(row['Assessor Parcel']))
    
    assessor = str(row['Assessor Book']) + ' ' + str(row['Assessor Page']) + ' ' + str(row['Assessor Parcel'])

    return assessor

def CreateExcel():
        
    #import csv file to a dataframe
    csv_file_path = r'D:/50_Layouts/03_Data/230709_Building_Permits_description_sb_above_100k.csv'
    df = pd.read_csv(csv_file_path)
    print(df.head())

    #filter the dataframe to only maintain the fields in field_maintain
    df = df[field_maintain]

    #concatenate the following fields: Address Start, Address Fraction Start, Address End, Address Fraction End, Street Direction, Street Name, Street Suffix, Suffix Direction, Unit Range Start, Unit Range End into on address using concat_address fields into one field
    df['Address'] = df.apply(lambda row: concat_address(row), axis=1)

    #drop from the data frame the following columns: Address Start, Address Fraction Start, Address End, Address Fraction End, Street Direction, Street Name, Street Suffix, Suffix Direction, Unit Range Start, Unit Range End
    df = df.drop(['Address Start', 'Address Fraction Start', 'Address End', 'Address Fraction End', 'Street Direction', 'Street Name', 'Street Suffix', 'Suffix Direction', 'Unit Range Start', 'Unit Range End'], axis=1)

    df['APN'] = df.apply(lambda row: concat_assessor(row), axis=1)
    df.drop(['Assessor Book', 'Assessor Page', 'Assessor Parcel'], axis=1, inplace=True)

    # remove all rows where 'Floor Area-L.A. Zoning Code Definition' is smaller than 400
    df = df[df['Floor Area-L.A. Zoning Code Definition'] >= 1000]

    #group data by zipcode
    df = df.groupby('Zip Code').agg({'Valuation': 'sum', 'Floor Area-L.A. Zoning Code Definition': 'sum', 'Floor Area-L.A. Building Code Definition': 'sum', 'Address': 'count'}).reset_index()

    print(df)

def Comps(zipcode):

    from CompsApp import process_zipcode_data


    data = process_zipcode_data(zipcode)

    #row['Low Tier Sale per SF'] = data['low_tier_sale_per_sf']
    #row['Mid Tier Sale per SF'] = data['mid_tier_sale_per_sf']
    #row['High Tier Sale per SF'] = data['high_tier_sale_per_sf']
    #row['Low Tier Rent per SF'] = data['low_tier_rent_per_sf']
    #row['Mid Tier Rent per SF'] = data['mid_tier_rent_per_sf']
    #row['High Tier Rent per SF'] = data['high_tier_rent_per_sf']

    return data

def collectURL_permit_assessors():

    #open excel file as a pandas dataframe
    excel_file_path = r'D:/50_Layouts/03_Data/230709_Building_Permits_description_sb_above_100k_edited.xlsx'

    #url format for permit data https://www.ladbsservices2.lacity.org/OnlineServices/PermitReport/PcisPermitDetail?id1=22010&id2=20000&id3=05242
    #url format for assessor map data https://maps.assessor.lacounty.gov/Geocortex/Essentials/PAIS/REST/sites/PAIS/VirtualDirectory/AssessorMaps/ViewMap.html?val=2625-003

    #create a dataframe from the excel file
    df = pd.read_excel(excel_file_path)
    #iterate through the dataframe

    #create an empty dataframe to store the updated rows at

    for index, row in df.iterrows():

        #create a permit number variable
        permit_no = row['PCIS Permit #'].split('-')
        apn = row['APN'].split(' ')


        permit_url = 'https://www.ladbsservices2.lacity.org/OnlineServices/PermitReport/PcisPermitDetail?id1={}&id2={}&id3={}'.format(permit_no[0], permit_no[1], permit_no[2])
        assessor_map_url = 'https://maps.assessor.lacounty.gov/Geocortex/Essentials/PAIS/REST/sites/PAIS/VirtualDirectory/AssessorMaps/ViewMap.html?val={}-{}'.format(apn[0], apn[1])

        #add the urls to the dataframe
        df.at[index, 'Permit URL'] = permit_url
        df.at[index, 'Assessor Map'] = assessor_map_url

    #append the row to a new dataframe

    print(df.head())
    #export the dataframe to an excel file
    df.to_excel(r'D:/50_Layouts/03_Data/230709_Building_Permits_description_sb_above_100k_edited.xlsx', index=False)

def zipcode_analysis():

        #create a dataframe from a csv located at "D:\50_Layouts\03_Data\230709_LA_County_ZIP_Codes.csv"
        df = pd.read_csv(r'D:\50_Layouts\03_Data\230709_LA_County_ZIP_Codes.csv')

        #create new dataframe with the columns of df
        column_names = ['ZIPCODE', 'Low Tier Sale per SF', 'Mid Tier Sale per SF', 'High Tier Sale per SF', 'Low Tier Rent per SF', 'Mid Tier Rent per SF', 'High Tier Rent per SF']
        df_new = pd.DataFrame(columns=column_names)

        #iterate through the dataframe
        for index, row in df.iterrows():

            try:

                #remove the leading zeros from the zipcode
                zipcode = str(row['ZIPCODE'])
                zipcode = zipcode.split('.')
                zipcode = zipcode[0]

                #data = Comps(zipcode)

                row['zipcode'] = zipcode
                row['Low Tier Sale per SF'] = data['low_tier_sale_per_sf']
                row['Mid Tier Sale per SF'] = data['mid_tier_sale_per_sf']
                row['High Tier Sale per SF'] = data['high_tier_sale_per_sf']
                row['Low Tier Rent per SF'] = data['low_tier_rent_per_sf']
                row['Mid Tier Rent per SF'] = data['mid_tier_rent_per_sf']
                row['High Tier Rent per SF'] = data['high_tier_rent_per_sf']

                #append the row to a new dataframe
                df_new = df_new.append(row, ignore_index=True)

            except KeyError:
                pass


        print(df_new)
        df_new.to_excel(r'D:\50_Layouts\03_Data\230709_LA_County_ZIP_Codes_edited.xlsx', index=False)

if __name__ == "__main__":

    #open the json file 230711_LA_County_Zipcodes.geojson
    with open(r'D:\50_Layouts\03_Data\230711_LA_County_Zipcodes .geojson') as f:
        data = json.load(f)
    
    #open the excel file from the following path "D:\50_Layouts\03_Data\230709_LA_County_ZIP_Codes_edited.xlsx" as a dataframe
    df = pd.read_excel(r'D:\50_Layouts\03_Data\230709_LA_County_ZIP_Codes_edited.xlsx')
    df = df.fillna('missing')
    #iterate through the json file
    for feature in data['features']:

        properties = feature['properties']
        zipcode = properties['ZIPCODE']

        #find the row in the dataframe where the cell value under column equals the value of zipcode
        row = df.loc[df['ZIPCODE'] == int(zipcode)]

        #convert the row to a dicitionary  
        row = row.to_dict('records')

        try: 
            row = row[0]

            #add the dictionary to the properties dictionary from the json file

            for key,value in row.items():
                print(value)
                if value != 'missing':

                    properties[key] = float(value)
                
                else:
                    properties[key] = 0
                    print(value)

        #convert the row to a dictionary and add it to the properties dictionary from the json file
        
        except IndexError:
            pass
    #save the json file
    with open(r'D:\50_Layouts\03_Data\230711_LA_County_Zipcodes_edited.geojson', 'w') as f:
        json.dump(data, f)

    
    