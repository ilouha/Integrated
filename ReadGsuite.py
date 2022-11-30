from __future__ import print_function

import os.path
import google.auth
import pandas as pd 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 
from pprint import pprint
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 

def creds():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds
def get_values(spreadsheet_id, range_name,creds):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print(f"{len(rows)} rows retrieved")
        return rows

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
def update_values(spreadsheet_id, range_name, value_input_option, values, creds):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    creds = creds
    # pylint: disable=maybe-no-member
    try:

        service = build('sheets', 'v4', credentials=creds)
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def dataconversion(Range,Range_Name):

    cred = creds()
    data = get_values(SAMPLE_SPREADSHEET_ID,Range,cred) 

    df = pd.DataFrame(data)

    df.columns = df.iloc[0]
    df.drop(df.index[0], inplace=True)
    
    col_names = df.columns.values.tolist()


    for col in col_names:
        df[col] = pd.to_numeric(df[col], errors = 'ignore')

    # For the attributes inputs the function is replacing the strings into floats. 

    if col_names[1] == 'Attributes':
        for index,row in df.iterrows():
            m = row[1].replace(',', '')
            try:
                row[1] = float(m)
            except ValueError:

                row[1] = row[1]
            
            except TypeError:

                row[1] = row[1][0:]
                row[1] = float(m)


    df2 = df.set_index(col_names[0])

    JsonFilePath = '{}.json'.format(Range_Name)
    df2.to_json(JsonFilePath)

    return df

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1jTqrcL5glnUB_vw4OE9dPBrK6L6IYYCvPk22BobRHQY' 

Range_Attributes = 'Attributes!A1:B12'
Range_FinancialVariables = 'List Of Variables!A1:B4'
Range_HardCosts = 'List Of Variables!A6:B13'
Range_SoftCosts = 'List Of Variables!A15:B20'  
Range_Incentives = 'List Of Variables!A22:I27'


if __name__ == '__main__':

    #main()

    #Read the date from Gsuite and Converts it to a JSON

 
    
    dataconversion(Range_Attributes,'Attributes')
    dataconversion(Range_FinancialVariables,'FinancialVariables')
    dataconversion(Range_HardCosts,'HardCosts')
    dataconversion(Range_SoftCosts,'SoftCosts')
    dataconversion(Range_Incentives,'Incentives')



#___________________________________________________________________________________________________________
#Preloads the values from Gsheets and rewrites the variables for the json file

    from app import main

    values = main()

    cred = creds()
    service = build('sheets', 'v4', credentials=cred)
    body = {
            'values': values
    }

    request = service.spreadsheets().values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='Feasibility!B1')
    response = request.execute()

    response_date = service.spreadsheets().values().append(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        valueInputOption='RAW',
        range='Feasibility!B1',
        body=dict(
            majorDimension='ROWS',
            values=values.T.reset_index().T.values.tolist())
    ).execute()



    SAMPLE_RANGE_NAME_WRITE = 'Feasibility!A2'
    update_values(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME_WRITE,"USER_ENTERED",values,cred)