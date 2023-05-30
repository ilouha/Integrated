import pandas as pd
import json

def Assumtions():
    
    def format_to_dollar_price(value):
        if isinstance(value, (int, float)):
            formatted_value = "${:,.2f}".format(value)
        elif isinstance(value, str):
            # Remove any non-numeric characters
            value = ''.join(filter(str.isdigit, value))
            if value:
                formatted_value = "${:,.2f}".format(float(value)/100)
            else:
                formatted_value = "$0.00"
        else:
            raise TypeError("Unsupported value type. Only int, float, and str are supported.")
        
        return formatted_value

    def float_to_percentage(number):
        percentage = number * 100
        formatted_percentage = "{:.2f}%".format(percentage)
        return formatted_percentage

    # Variable Declaration
    hard_soft_coef = 80  # Percentage of construction costs attributed to hard costs

    costruction_costs_per_sf = 350  # Construction cost per square foot
    costruction_costs_per_sf_parking = 175 # Construction cost per square foot for parking

    sale_price_per_sf = 800  # Price per square foot for unit sale
    rent_price_per_sf = 4  # Rent per square foot

    cap_rate = 5  # Capitalization rate
    net_coef = 70  # Percentage of average rent considered as net operating income

    #_______________________________________________________________________________________

    # Create a dictionary to store the calculated values

    data_dict = {

        'hard_vs_soft_coef': float_to_percentage(hard_soft_coef/100),
        'costruction_costs_per_sf': format_to_dollar_price(costruction_costs_per_sf),
        'costruction_costs_per_sf_parking': format_to_dollar_price(costruction_costs_per_sf_parking),
        'sale_price_per_sf': format_to_dollar_price(sale_price_per_sf),
        'rent_price_per_sf': format_to_dollar_price(rent_price_per_sf),
        'cap_rate': float_to_percentage(cap_rate/100),
        'net_vs_gross_coef': float_to_percentage(net_coef/100)
    }

    # Create a dataframe from the dictionary

    values = []

    keys_list = [

        'costruction_costs_per_sf',
        'costruction_costs_per_sf_parking',
        'sale_price_per_sf',
        'rent_price_per_sf',
        'cap_rate',
        'net_vs_gross_coef',
        'hard_vs_soft_coef'
    ]

    for item in keys_list:
        values.append(item + ': ' + str(data_dict[item]))

    with open('data.json') as f:
        data = json.load(f)

    data['json_schema']['assumptions'] = data_dict

    #save the json file
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
