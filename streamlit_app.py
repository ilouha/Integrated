import streamlit as st
import numpy as np
import pandas as pd
import locale

def float_to_percentage(number):
    # Check if the input is a float or int
    if not isinstance(number, (float, int)):
        raise ValueError("Input must be a float or int.")
    
    # Convert the number to a percentage string
    percentage_string = "{:.2f}%".format(number * 100.0)
    return percentage_string

def float_to_dollars(amount):
    # Set the locale to the user's default, so the currency formatting is appropriate
    locale.setlocale(locale.LC_ALL, '')
    
    # Format the float as dollars
    dollars = locale.currency(amount, grouping=True)
    
    # If the locale is using a currency symbol after the amount, remove it
    if dollars.endswith(".00"):  # In some locales, ".00" might be added at the end
        dollars = dollars[:-3]
        
    return dollars

st.title('Layouts App - Analyze Real Estate Per Zipcode')
st.write("disclamer: this is a demo app based on singular data source and shall not be used for any real estate investment decisions")

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
    rent_feasibility_low = float(row.loc['rent_feasibility_low'])
    rent_feasibility_high = float(row.loc['rent_feasibility_high'])

    #print(flip_feasibility)

    col1,col2,col3 = st.columns(3)

    col1.metric('Zipcode Ranking for House Flipping',round(float(flip_feasibility),2))
    col2.metric('Cash on Cash per SF High End',float_to_percentage(rent_feasibility_low))
    col3.metric('Cash on Cash per SF Low End',float_to_percentage(rent_feasibility_high))

    st.text('')
    st.text('')
    st.subheader('Rental comparables based on US Listing API')

    columns_rpsf =[ 
            "count_rpsf",
        #    "mean_rpsf",
        #    "std_rpsf",
            "min_rpsf",
            "25%_rpsf",
            "50%_rpsf",
            "75%_rpsf",
            "max_rpsf",
            ]
    
    min_rent = row.loc['min_rpsf']
    low_rent = row.loc['25%_rpsf']
    mid_rent = row.loc['50%_rpsf']
    high_rent = row.loc['75%_rpsf']
    max_rent = row.loc['max_rpsf']
    sample_size = row.loc['count_rpsf']

    col1,col2,col3 = st.columns(3)

    col1.metric('25% percentile Rent',float_to_dollars(float(low_rent)))
    col2.metric('50% percentile Rent',float_to_dollars(float(mid_rent)))
    col3.metric('75% percentile Rent',float_to_dollars(float(high_rent)))

    col1,col2,col3 = st.columns(3)

    col1.metric('Minimum Rent',float_to_dollars(float(min_rent)))
    col2.metric('Maximum Rent',float_to_dollars(float(max_rent)))
    col3.metric('Sample Size',round(float(sample_size),0))

    st.text('')
    st.text('')
    st.subheader('Sales comparables based on US Listing API')

    columns_ppsf =[ 
            "count_ppsf",
            "mean_ppsf",
            "std_ppsf",
            "min_ppsf",
            "25%_ppsf",
            "50%_ppsf",
            "75%_ppsf",
            "max_ppsf",

            ]
    
    min_sale = row.loc['min_ppsf']
    low_sale = row.loc['25%_ppsf']
    mid_sale = row.loc['50%_ppsf']
    high_sale = row.loc['75%_ppsf']
    max_sale = row.loc['max_ppsf']
    sample_size = row.loc['count_ppsf']

    col1,col2,col3 = st.columns(3)

    col1.metric('25% percentile Sale',float_to_dollars(float(low_sale)))
    col2.metric('50% percentile Sale',float_to_dollars(float(mid_sale)))
    col3.metric('75% percentile Sale',float_to_dollars(float(high_sale)))

    col1,col2,col3 = st.columns(3)

    col1.metric('Minimum Sale',float_to_dollars(float(min_sale)))
    col2.metric('Maximum Sale',float_to_dollars(float(max_sale)))
    col3.metric('Sample Size',round(float(sample_size),0))


else:
    st.write('Not in database')

#st.text('')
#st.text('')
#st.subheader('Database for Reference')
#st.dataframe(df)

st.text('')
st.text('')
st.subheader('Remodel Proforma Calculator')


building_size = st.number_input('Building Size',value=1200)
purchase_price = st.number_input('Purchase Price',value=800000)
cap_rate = 5
rpsf = st.number_input('Rent per SF',value=4)
ppsf = st.number_input('Price per SF',value=650)
cpsf = st.number_input('Construction Cost per SF',value=75)
hard_soft_coef = 70
net_coef = 80
occupancy_rate = 90

from RemodelProformaCalcs import remodel_proforma_calcs

data = remodel_proforma_calcs(

    building_size,
    purchase_price,
    cap_rate,
    rpsf,
    ppsf,
    cpsf,
    hard_soft_coef,
    net_coef,
    occupancy_rate

)

print(data)
#st.dataframe(data)
if data is not None:

    total_project_cost = data['proforma']['total_project_cost']
    net_income = data['proforma']['net_income']
    cap_rate = data['proforma']['future_cap_rate']

    st.text('')
    st.text('')
    st.subheader('Proforma Results')
    
    col1,col2,col3= st.columns(3)

    col1.metric('Total Project Cost',total_project_cost)
    col2.metric('Expected Income Post Expenses',net_income)
    col3.metric('Cap Rate',cap_rate)



else: 
    st.write('No underwriting data available')