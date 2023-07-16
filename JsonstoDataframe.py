import pandas as pd 
import json 
import os 
from pprint import pprint

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
df = df.round(2)

#drop the following column names from the dataframe: unique_ppst, unique_rpsf,top_ppst, top_rpsf
df = df.drop(['unique_ppsf', 'unique_rpsf', 'top_ppsf', 'top_rpsf','freq_ppsf','freq_rpsf'], axis=1)

print(df.head())

#save the dataframe as an excel file
df.to_excel('ZipcodeData.xlsx')




        