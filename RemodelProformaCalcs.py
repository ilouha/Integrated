import pandas as pd
import json
from pprint import pprint

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
def remodel_proforma_calcs(

    building_size,
    purchase_price,
    cap_rate,
    rpsf,
    ppsf,
    cpsf,
    hard_soft_coef,
    net_coef,
    occupancy_rate,        
    ):

    try: 

        construction_cost = building_size * cpsf
        soft_cost = construction_cost * (hard_soft_coef / 100)
        total_project_cost = purchase_price + construction_cost + soft_cost
        gross_monthly_rent = float(rpsf) * building_size * (occupancy_rate/100)
        net_motnhly_rent = gross_monthly_rent * (net_coef / 100)
        annual_rent = gross_monthly_rent * 12
        gross_income = annual_rent
        net_income = annual_rent * (net_coef / 100)
        valuation = (net_income / (cap_rate / 100))
        future_cap_rate = net_income / total_project_cost
        sale_value = building_size * ppsf
        profit = sale_value - total_project_cost
        profit_margin = (sale_value - total_project_cost) / total_project_cost

        dict_proforma = {
            'building_size': format_to_sf_area(building_size),
            'purchase_price': format_to_dollar_price(purchase_price),
            'construction_cost': format_to_dollar_price(construction_cost),
            'soft_cost': format_to_dollar_price(soft_cost),
            'total_project_cost': format_to_dollar_price(total_project_cost),
            'gross_monthly_rent': format_to_dollar_price(gross_monthly_rent),
            'net_monthly_rent': format_to_dollar_price(net_motnhly_rent),
            'gross_income': format_to_dollar_price(gross_income),
            'net_income': format_to_dollar_price(net_income),
            'valuation': format_to_dollar_price(valuation),
            'future_cap_rate': float_to_percentage(future_cap_rate),
            'sale_value': format_to_dollar_price(sale_value),
            'profit': format_to_dollar_price(profit),
            'profit_margin': float_to_percentage(profit_margin)
        }

        dict_assumptions = {

            "cap_rate": float_to_percentage(cap_rate / 100),
            "rent_per_sf": format_to_dollar_price(rpsf),
            "price_per_sf": format_to_dollar_price(ppsf),
            "construction_price_per_sf": format_to_dollar_price(cpsf),
            "soft_cost_allowance": float_to_percentage(hard_soft_coef / 100),
            "net_rental_coef": float_to_percentage(net_coef / 100),
            "occupancy_rate": float_to_percentage(occupancy_rate / 100)
        }

        data = {
            "proforma": dict_proforma,
            "assumptions" : dict_assumptions
        }

        return data
    
    except ZeroDivisionError:
        print("Error: Division by zero")
        return None

#_______________________________________________________________________________________