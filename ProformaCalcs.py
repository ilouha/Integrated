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

def ProformaCalc(units,total_area,total_parking_area,rpsf,ppsf,cpsf,cpsf_parking,cap_rate,hard_soft_coef,net_coef,land_value):

    # Variable Declaration
    units = units  # Number of units in the project
    total_area = total_area  # Total area of the project in square feet
    total_parking_area = total_parking_area # Total area of the parking in square feet
    rpsf = rpsf  # Rent per square foot
    ppsf = ppsf  # Price per square foot for unit sale
    cpsf = cpsf  # Construction cost per square foot
    cpsf_parking = cpsf_parking # Construction cost per square foot for parking
    cap_rate = cap_rate  # Capitalization rate
    hard_soft_coef = hard_soft_coef  # Percentage of construction costs attributed to hard costs
    net_coef = net_coef  # Percentage of average rent considered as net operating income
    land_value = land_value  # Value of the land

    #Functions

    #_______________________________________________________________________________________
    # Calculations
    average_unit_size = total_area / units  # Average size of each unit in square feet
    average_rent = float(rpsf) * total_area / units  # Average monthly rent per unit
    unit_sale_value = average_unit_size * ppsf  # Sale value of each unit

    project_valuation = (average_rent * units * (net_coef / 100) * 12) / (cap_rate / 100)  # Valuation of the project based on net operating income
    construction_costs = total_area * cpsf  # Total construction costs for the project
    soft_costs = construction_costs * ((100 - hard_soft_coef) / 100)  # Soft costs for the project
    total_project_costs = land_value + construction_costs + soft_costs  # Total costs for the project

    net_income = total_area * rpsf * net_coef * 12 

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
        'net_income' : format_to_dollar_price(net_income),
        'cap_rate' : float_to_percentage(net_income / total_project_costs)
    }

    return data_dict










