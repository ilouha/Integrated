import pandas as pd 
import json

#open data.json 
with open('data.json') as f:
    data = json.load(f)


#flatten the json file
df_statistics = pd.json_normalize(data['json_schema']['statistics'])
df_general_information = pd.json_normalize(data['json_schema']['general_information'])
df_proforma = pd.json_normalize(data['json_schema']['proforma'])
df_assumpmtions = pd.json_normalize(data['json_schema']['assumptions'])
df_zoning_information = pd.json_normalize(data['json_schema']['zoning_information'])

#transpose each dataframe
df_statistics = df_statistics.transpose()
df_general_information = df_general_information.transpose()
df_proforma = df_proforma.transpose()
df_assumpmtions = df_assumpmtions.transpose()
df_zoning_information = df_zoning_information.transpose()

#append each dataframe
df = df_statistics.append(df_general_information)
df = df.append(df_proforma)
df = df.append(df_assumpmtions)
df = df.append(df_zoning_information)

print(df)




