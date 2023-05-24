import pandas as pd

# Variable Declaration
units = 20  # Number of units in the project
total_area = 20000  # Total area of the project in square feet
total_parking_area = 3000 # Total area of the parking in square feet
rpsf = 4  # Rent per square foot
ppsf = 800  # Price per square foot for unit sale
cpsf = 350  # Construction cost per square foot
cpsf_parking = 175 # Construction cost per square foot for parking
cap_rate = 5  # Capitalization rate
hard_soft_coef = 80  # Percentage of construction costs attributed to hard costs
net_coef = 70  # Percentage of average rent considered as net operating income
land_value = 1000000  # Value of the land

#Functions

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

def format_to_sf_area(value):
    if isinstance(value, (int, float)):
        formatted_value = "{:,.2f} SF".format(value)
    else:
        raise TypeError("Unsupported value type. Only int and float are supported.")
    
    return formatted_value

#_______________________________________________________________________________________
# Calculations
average_unit_size = total_area / units  # Average size of each unit in square feet
average_rent = float(rpsf) * total_area / units  # Average monthly rent per unit
unit_sale_value = average_unit_size * ppsf  # Sale value of each unit

project_valuation = (average_rent * units * (net_coef / 100) * 12) / (cap_rate / 100)  # Valuation of the project based on net operating income
construction_costs = total_area * cpsf  # Total construction costs for the project
soft_costs = construction_costs * ((100 - hard_soft_coef) / 100)  # Soft costs for the project
total_project_costs = land_value + construction_costs + soft_costs  # Total costs for the project

net_income = total_area * rpsf * 0.7 * 12 

# Create a dictionary to store the calculated values
data_dict = {
    'total__buildbale_area': format_to_sf_area(total_area),
    'total_parking_area': format_to_sf_area(total_parking_area),
    'total_units': units,
    'average_unit_size': format_to_sf_area(average_unit_size),
    'average_unit_rent': format_to_dollar_price(average_rent),
    'average_unit_sale_value': format_to_dollar_price(unit_sale_value),
    'land_value': format_to_dollar_price(land_value),
    'construction_cost': format_to_dollar_price(total_area * cpsf + total_parking_area * cpsf_parking),
    'soft_costs': format_to_dollar_price(soft_costs),
    'total_cost': format_to_dollar_price(total_project_costs),
    'sale_value': format_to_dollar_price(total_area * ppsf),
    'project_valuation': format_to_dollar_price(project_valuation),
    'gross_profit': format_to_dollar_price(total_area * ppsf - total_project_costs),
    'gross_margin': float_to_percentage((total_area * ppsf - total_project_costs) / (total_area * ppsf)),
    'gross_income' : format_to_dollar_price(total_area * rpsf * 12) ,
    'net_income' : format_to_dollar_price(net_income)
}

# Create a list of keys to iterate through
keys_list = [
    'total__buildbale_area',
    'total_parking_area',
    'total_units',
    'average_unit_size',
    'average_unit_rent',
    'average_unit_sale_value',
    'land_value',
    'construction_cost',
    'soft_costs',
    'total_cost',
    'sale_value',
    'project_valuation',
    'gross_profit',
    'gross_margin',
    'gross_income',
    'net_income'
]

# Iterate through the keys_list and retrieve corresponding values from the data_dict
values = []
for item in keys_list:
    values.append(item + ': ' + str(data_dict[item]))

# Print the values
print(values)

# Create a dataframe from the data_dict
df = pd.DataFrame(data_dict, index=[0])
#flip df
df = df.transpose()
#save the df to a csv file
df.to_csv('./proforma.csv', sep=',', encoding='utf-8')
