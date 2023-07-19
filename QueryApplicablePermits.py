import pandas as pd
import csv 
import json

def readSB09Permits():

    path = './data/230709_Building_Permits_description_sb_above_100k.csv'

    #create pandas dataframe from the csv file
    df = pd.read_csv(path)

    #keep only the following columns APN, Assessor Map, PCIS Permit #, Permit URL, Address
    df = df[['Address','APN', 'Assessor Map', 'PCIS Permit #', 'Permit URL' ]]
    
    return df
