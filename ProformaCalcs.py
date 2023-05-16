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

total_area = 'Total Residential Area: {}'.format(total_area)
total_units = 'Total Residential Units: {}'.format(units)
average_unit_size = 'Average Unit Size: {}'.format(average_unit_size)
average_unit_rent = 'Average Unit Rent: {}'.format(average_rent)
average_unit_sale_value = 'Average Unit Sale Value: {}'.format(unit_sale_value)

land_value = 'Cost of Land: {}'.format(land_value)
construction_cost = 'Construction Cost (Residential): {}'.format(total_area*cpsf)
soft_costs = 'Soft cost: {}'.format(soft_costs)
total_cost = 'Total Project Cost {}'.format(total_project_costs)

sale_value = 'Sale Value (flip): {} '.format(total_area*ppsf)
project_valuation = 'Project Valuation (rentals) : {}'.format(project_valuation)

gross_profit = sale_value - total_project_costs
gross_margin = gross_profit/sale_value

