import pandas as pd 

#Variable Declaration 

units = 20
total_area = 20000
rpsf = 4
ppsf = 800
cpsf = 350
cap_rate = 5
hard_soft_coef = 80
net_coef = 70
land_value  = 1000000

#calcs

average_unit_size = total_area/units
average_rent = float(rpsf) * (total_area)/units
unit_sale_value = average_unit_size * ppsf

project_valuation = (average_rent * units * (net_coef/100)*12) / (cap_rate/100)
construction_costs = total_area*cpsf
soft_costs = construction_costs*((100-hard_soft_coef)/100)
total_project_costs = land_value + construction_costs + soft_costs

#____________________________________________________________

data_dict = {

    'total_area': total_area,
    'total_units': units,
    'average_unit_size': average_unit_size,
    'average_unit_rent': average_rent,
    'average_unit_sale_value': unit_sale_value,
    'land_value': land_value,
    'construction_cost': total_area * cpsf,
    'soft_costs': soft_costs,
    'total_cost': total_project_costs,
    'sale_value': total_area * ppsf,
    'project_valuation': project_valuation,
    'gross_profit': total_area * ppsf - total_project_costs,
    'gross_margin': (total_area * ppsf - total_project_costs) / (total_area * ppsf)
}

#iterate through the dictionary and create a string out the key and value

keys_list = [
    'total_area',
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
    'gross_margin'
]

#iterate through key_list and return the value from the data_dict

values = []
for item in keys_list:
    values.append(item + ': ' + str(data_dict[item]))


print(values)