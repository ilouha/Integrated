import pandas as pd

#read excel data into dataframe
df = pd.read_csv('data\ACSDP5Y2021.DP05-Data.csv')
print(df.head())

df = pd.read_csv('data\ACSST5Y2021.S1101-Data.csv')
print(df.head())

df = pd.read_csv('data\ACSST5Y2021.S1502-Data.csv')
print(df.head())

df = pd.read_csv('data\ACSST5Y2021.S1701-Data.csv')
print(df.head())

df = pd.read_csv('data\ACSST5Y2021.S1903-Data.csv')
print(df.head())

df = pd.read_csv('data\ACSST5Y2021.S2301-Data.csv')
print(df.head())