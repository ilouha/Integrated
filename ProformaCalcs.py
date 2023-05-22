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

# Calculations
average_unit_size = total_area / units  # Average size of each unit in square feet
average_rent = float(rpsf) * total_area / units  # Average monthly rent per unit
unit_sale_value = average_unit_size * ppsf  # Sale value of each unit

project_valuation = (average_rent * units * (net_coef / 100) * 12) / (cap_rate / 100)  # Valuation of the project based on net operating income
construction_costs = total_area * cpsf  # Total construction costs for the project
soft_costs = construction_costs * ((100 - hard_soft_coef) / 100)  # Soft costs for the project
total_project_costs = land_value + construction_costs + soft_costs  # Total costs for the project

# Create a dictionary to store the calculated values
data_dict = {
    'total__buildbale_area': total_area,
    'total_parking_area': total_parking_area,
    'total_units': units,
    'average_unit_size': average_unit_size,
    'average_unit_rent': average_rent,
    'average_unit_sale_value': unit_sale_value,
    'land_value': land_value,
    'construction_cost': total_area * cpsf + total_parking_area * cpsf_parking,
    'soft_costs': soft_costs,
    'total_cost': total_project_costs,
    'sale_value': total_area * ppsf,
    'project_valuation': project_valuation,
    'gross_profit': total_area * ppsf - total_project_costs,
    'gross_margin': (total_area * ppsf - total_project_costs) / (total_area * ppsf),
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
df.to_csv('./test.csv', sep=',', encoding='utf-8')
