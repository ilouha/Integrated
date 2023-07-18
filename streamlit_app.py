import streamlit as st
import numpy as np
import pandas as pd

st.title('Layouts App - Analyze Real Estate Per Zipcode')
st.write("Here's our first attempt at using data to create a table:")

#read the the json file data/Price_Data_Per_Zipcode.json and store in a dataframe df 
df = pd.read_json('data/Price_Data_Per_Zipcode.json')

#swap rows and columns in the df
df = df.transpose()

# Create a new index column and move the current index to a column named 'zipcode'
df.reset_index(inplace=True)

# Rename the 'index' column to 'zipcode'
df.rename(columns={'index': 'zipcode'}, inplace=True)

#conevrt the zipcode column to string
df['zipcode'] = df['zipcode'].astype(str)

# Display the updated DataFrame
print(df)



zipcode = st.text_input('Enter your zipcode:')

if zipcode:

    #get the row from the dataframe where the zipcode is equal to the zipcode entered by the user
    row = df.loc[df['zipcode'] == str(zipcode)]
    row = row.transpose()
    #st.dataframe(row)
    #convert row to json
    row_json = row.to_json()

    #get the flip_feasibility value from the row
    flip_feasibility = row.loc['flip_feasibility']
    rent_feasibility_low = row.loc['rent_feasibility_low']
    rent_feasibility_high = row.loc['rent_feasibility_high']

    #print(flip_feasibility)

    st.metric('Zipcode Ranking for House Flipping',flip_feasibility)
    st.metric('Zipcode Ranking for Renting High end',rent_feasibility_low)
    st.metric('Zipcode Ranking for Renting Low end',rent_feasibility_high)



    columns_rpsf =[ 
        #    "count_rpsf",
        #    "mean_rpsf",
        #    "std_rpsf",
            "min_rpsf",
            "25%_rpsf",
            "50%_rpsf",
            "75%_rpsf",
            "max_rpsf",
        #    "count_ppsf"
            ]
    
    #from row select the columns_rpsf
    row_rpsf = row.loc[columns_rpsf]
    st.title('Rent Distribution')
    st.write('Statistics for Rent per Square Foot per Zipcode')
    st.bar_chart(row_rpsf)

    columns_ppsf =[ 
        #    "count_ppsf",
        #    "mean_ppsf",
        #    "std_ppsf",
            "min_ppsf",
            "25%_ppsf",
            "50%_ppsf",
            "75%_ppsf",
            "max_ppsf",
        #    "count_ppsf"
            ]
    
    #from row select the columns_rpsf
    row_ppsf = row.loc[columns_rpsf]
    st.title('Price Distribution')
    st.write('Statistics for Price per Square Foot per Zipcode')
    st.bar_chart(row_ppsf)

    st.json(row_json)


else:
    st.write('Not in database')


st.dataframe(df)