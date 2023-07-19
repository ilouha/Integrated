import streamlit as st
import numpy as np
import pandas as pd
import locale
from PIL import Image

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

st.title('Layouts App - Your online SB09 Feasibility Calculator')
st.write("disclamer: this is a demo app based on singular data source and shall not be used for any real estate investment decisions")

#create a cover image
image = Image.open('Images/SB09 Diagrams-01.png')
st.image(image)

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


st.text('')
st.text('')
st.subheader('Remodel Proforma Calculator')

building_size = st.number_input('Building Size',value=1200)
purchase_price = st.number_input('Purchase Price',value=800000)
ppsf = st.number_input('Price per SF',value=650)
cpsf = st.number_input('Construction Cost per SF',value=75)

cap_rate = 5
hard_soft_coef = 70
net_coef = 80
occupancy_rate = 90
rpsf = 4

#_______________________________________________________________________________________
# New Development Proforma Calculator

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
    Gross_Profit = data['proforma']['profit']
    sale_value = data['proforma']['sale_value']
    
    profit_margin = data['proforma']['profit_margin']
    soft_cost = data['proforma']['soft_cost']
    construction_cost = data['proforma']['construction_cost']

    st.text('')
    st.text('')
    st.subheader('Outline Costs')
    
    col1,col2,col3= st.columns(3)

    col1.metric('Total Project Costs',total_project_cost)
    col2.metric('Construction Costs',construction_cost)
    col3.metric('Soft Costs',soft_cost)

    col1,col2,col3= st.columns(3)

    col1.metric('Sale Value',sale_value)
    col2.metric('Profit Margin',profit_margin)
    col3.metric('Gross Profit',sale_value)
else: 
    st.write('No underwriting data available')
#_______________________________________________________________________________________
# New Development Proforma Calculator

st.text('')
st.text('')
st.subheader('New development Proforma Calculator')

from Addition_Proforma import ProformaCalc

land_value = purchase_price
hard_soft_coef = 70
net_coef = 80
occupancy_rate = 90

units = st.number_input('Number of Units Added',value=1)
added_area = st.number_input('Added Area',value=600)
total_parking_area = st.number_input('Total Parking Area Added',value=600)
cpsf_adition = st.number_input('Construction Cost per SF for Added Area',value=175)
cpsf_parking = st.number_input('Construction Cost per SF for Parking Area',value=75)
rpsf = st.number_input('Estimated Rent per SF',value=4)

data = ProformaCalc(units,
                    added_area,
                    total_parking_area,
                    rpsf,
                    ppsf,
                    cpsf_adition,
                    cpsf_parking,
                    hard_soft_coef,
                    net_coef,
                    )

if data is not None:

    total_project_cost = data['total_cost']
    construction_cost = data['construction_cost']
    soft_cost = data['soft_costs']
    
    averae_unit_rent = data['average_unit_rent']
    average_unit_size = data['average_unit_size']
    gross_income = data['gross_income']
    
    st.text('')
    st.text('')
    st.subheader('Outline Costs')

    col1,col2,col3= st.columns(3)

    col1.metric('Total Project Costs',total_project_cost)
    col2.metric('Construction Costs',construction_cost)
    col3.metric('Soft Costs',soft_cost)

    st.text('')
    st.text('')
    st.subheader('Rental Proforma')
    
    col1,col2,col3= st.columns(3)

    col1.metric('Average Unit Size',average_unit_size)
    col2.metric('Average Unit Rent',averae_unit_rent)
    col3.metric('Annual Groos Income',gross_income)

#_______________________________________________________________________________________
#Provide Permit Reference for SB09 

from QueryApplicablePermits import readSB09Permits
st.text('')
st.text('')
st.subheader('See approved SB09 Permits in City of Los Angeles for Reference')
df = readSB09Permits()
st.dataframe(df)