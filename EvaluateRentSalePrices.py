import pandas as pd 
import json 
import os 
from pprint import pprint


def map_to_1_100(column):
    # Step 1: Identify the minimum and maximum values in the column
    min_val = column.min()
    max_val = column.max()

    # Step 2: Use Min-Max scaling to map the values to 1-100 range
    scaled_column = 1 + ((column - min_val) / (max_val - min_val)) * 99
    
    return scaled_column

# iterate through the folder ZipcodeData and read each json file

folder_path = './ZipcodeData'

# Get a list of all files and directories in the folder
files = os.listdir(folder_path)

df_list = []
json_rpsf = {}
json_ppsf = {}

# Iterate through each file in the folder
for file_name in files:

    if file_name.endswith('.json'):

        #load the json file
        with open(folder_path + '/' + file_name) as f:
            data = json.load(f)
        
        #remove .json from the file_name
        file_name = file_name.replace('.json', '')

        try:
            data = data[file_name]
            data_rpsf = data['rpsf']
            data_ppst = data['ppsf']

            json_rpsf[file_name] = data_rpsf
            json_ppsf[file_name] = data_ppst

        except TypeError:
            print('TypeError: ' + file_name)
            continue

#conert the json to dataframe
df_rpsf = pd.DataFrame.from_dict(json_rpsf, orient='index')
df_ppsf = pd.DataFrame.from_dict(json_ppsf, orient='index')

#add a suffix for column names 'rpsf_'
df_rpsf = df_rpsf.add_suffix('_rpsf')
df_ppsf = df_ppsf.add_suffix('_ppsf')

#concatenate the two dataframes
df = pd.concat([df_rpsf, df_ppsf], axis=1)

#round all values to 2 decimal places
df = df.round(4)

#drop the following column names from the dataframe: unique_ppst, unique_rpsf,top_ppst, top_rpsf
df = df.drop(['unique_ppsf', 'unique_rpsf', 'top_ppsf', 'top_rpsf','freq_ppsf','freq_rpsf'], axis=1)


rent_feasibility_low = []
rent_feasibility_high = []
flip_feasibility = []

for index,row in df.iterrows():
    
    #calculate the gross cash on cash return per sf

    row['rent_feasibility_low'] = round(row['25%_rpsf']*12/row['25%_ppsf'],4)
    row['rent_feasibility_high'] = round(row['75%_rpsf']*12/row['75%_ppsf'],4)

    row['flip_feasibility'] = round(row['75%_ppsf']/row['25%_ppsf'],4)

    #add the information above to the dataframe
    
    rent_feasibility_low.append(row['rent_feasibility_low'])
    rent_feasibility_high.append(row['rent_feasibility_high'])
    flip_feasibility.append(row['flip_feasibility'])


df['rent_feasibility_low'] = rent_feasibility_low
df['rent_feasibility_high'] = rent_feasibility_high
df['flip_feasibility'] = flip_feasibility

#map the values to 1-100 range
df['flip_feasibility'] = map_to_1_100(df['flip_feasibility'])

print(df)

df.to_excel('./data/Price_Data_Per_Zipcode.xlsx')

#df to json
df.to_json('./data/Price_Data_Per_Zipcode.json', orient='index')




        