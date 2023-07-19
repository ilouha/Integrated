import pandas as pd
import json


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

def ProformaCalc(units,addition_area,total_parking_area,rpsf,ppsf,cpsf,cpsf_parking,hard_soft_coef,net_coef):

    # Variable Declaration
    units = units  # Number of units in the project
    addition_area = addition_area  # Total area of the project in square feet
    total_parking_area = total_parking_area # Total area of the parking in square feet
    rpsf = rpsf  # Rent per square foot
    ppsf = ppsf  # Price per square foot for unit sale
    cpsf = cpsf  # Construction cost per square foot
    cpsf_parking = cpsf_parking # Construction cost per square foot for parking
    hard_soft_coef = hard_soft_coef  # Percentage of construction costs attributed to hard costs
    net_coef = net_coef  # Percentage of average rent considered as net operating income

    #Functions

    #_______________________________________________________________________________________
    # Calculations
    average_unit_size = addition_area / units  # Average size of each unit in square feet
    average_rent = float(rpsf) * addition_area / units  # Average monthly rent per unit
    unit_sale_value = average_unit_size * ppsf  # Sale value of each unit

    #project_valuation = (int(average_rent) * int(units) * (net_coef / 100) * 12) / (cap_rate / 100)  # Valuation of the project based on net operating income
    construction_costs = addition_area * cpsf + total_parking_area * cpsf_parking # Total construction costs for the project
    soft_costs = construction_costs * ((100 - hard_soft_coef) / 100)  # Soft costs for the project
    total_project_costs = construction_costs + soft_costs  # Total costs for the project

    # Create a dictionary to store the calculated values
    data_dict = {
        
        'total__buildbale_area': format_to_sf_area(addition_area),
        'total_parking_area': format_to_sf_area(total_parking_area),
        'total_units': units,
        'average_unit_size': format_to_sf_area(average_unit_size),
        'average_unit_rent': format_to_dollar_price(average_rent),
        'average_unit_sale_value': format_to_dollar_price(unit_sale_value),
        'construction_cost': format_to_dollar_price(construction_costs),
        'soft_costs': format_to_dollar_price(soft_costs),
        'total_cost': format_to_dollar_price(total_project_costs),
        'sale_value': format_to_dollar_price(addition_area * ppsf),
        'gross_income' : format_to_dollar_price(addition_area * rpsf * 12) 
    }

    return data_dict



if __name__ == '__main__':
    from pprint import pprint
    pprint(ProformaCalc(1,600,600,2.5,300,150,75,0.2,0.5))




