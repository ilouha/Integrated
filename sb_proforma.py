import pandas as pd 

#_______________________________________________________________________________________
#Calculations of remodling proforma
def remodel_proforma_calcs(

    building_size,
    ppsf,
    cpsf,
    hard_soft_coef,     

    ):

    try: 

        construction_cost = building_size * cpsf
        soft_cost = construction_cost * (1 - (hard_soft_coef / 100))
        total_remodel_cost = construction_cost + soft_cost
        sale_value = building_size * ppsf


        data = {

            'construction_cost': construction_cost,
            'soft_cost': soft_cost,
            'total_remodel_cost': total_remodel_cost,
            'sale_value':sale_value,

        }

        return data
    
    except ZeroDivisionError:
        print("Error: Division by zero")
        return None
#_______________________________________________________________________________________
# Calculation of Addition Area 
def addition_proforma_calcs(units,
                 addition_area,
                 total_parking_area,
                 rpsf,ppsf,cpsf,
                 cpsf_parking,
                 hard_soft_coef):

    # Variable Declaration
    units = units  # Number of units in the project
    addition_area = addition_area  # Total area of the project in square feet
    total_parking_area = total_parking_area # Total area of the parking in square feet
    rpsf = rpsf  # Rent per square foot
    ppsf = ppsf  # Price per square foot for unit sale
    cpsf = cpsf  # Construction cost per square foot
    cpsf_parking = cpsf_parking # Construction cost per square foot for parking
    hard_soft_coef = hard_soft_coef  # Percentage of construction costs attributed to hard costs


    # Calculations
    average_unit_size = addition_area / units  # Average size of each unit in square feet
    average_rent = float(rpsf) * addition_area / units  # Average monthly rent per unit
    unit_sale_value = average_unit_size * ppsf  # Sale value of each unit

    #project_valuation = (int(average_rent) * int(units) * (net_coef / 100) * 12) / (cap_rate / 100)  # Valuation of the project based on net operating income
    construction_costs = addition_area * cpsf + total_parking_area * cpsf_parking # Total construction costs for the project
    soft_costs = construction_costs * ((100 - hard_soft_coef) / 100)  # Soft costs for the project
    total_project_costs = construction_costs + soft_costs  # Total costs for the project

    # Create a dictionary to store the calculated values
    data = {
        
        'total__buildbale_area': addition_area,
        'total_parking_area': total_parking_area,
        'total_units': units,
        'average_unit_size': average_unit_size,
        'average_unit_rent': average_rent,
        'average_unit_sale_value': unit_sale_value,
        'construction_cost': construction_costs,
        'soft_costs': soft_costs,
        'total_cost': total_project_costs,
        'sale_value': addition_area * ppsf,
        'gross_income' : addition_area * rpsf * 12
    }

    return data

#_______________________________________________________________________________________
# calculation of full scope of work 
def full_scope_of_work_calcs(
        
    building_size,
    ppsf_remodel,
    cpsf_remodel,
    hard_soft_coef,  
    units,
    addition_area,
    total_parking_area,
    rpsf,
    ppsf,
    cpsf,
    cpsf_parking,):

    data_remodel = remodel_proforma_calcs(building_size,ppsf_remodel,cpsf_remodel,hard_soft_coef)
    data_addition = addition_proforma_calcs(units,addition_area,total_parking_area,rpsf,ppsf,cpsf,cpsf_parking,hard_soft_coef)

    data_totals = {
        "total_project_cost" : data_remodel['total_remodel_cost'] + data_addition['total_cost'],
        "total_sale_value" : data_remodel['sale_value'] + data_addition['sale_value'],
        "total_construction_costs" : data_remodel['construction_cost'] + data_addition['construction_cost'],
        "total_soft_costs" : data_remodel['soft_cost'] + data_addition['soft_costs']
    }

    dic = {

        "data_remodel" : data_remodel,
        "data_addition" : data_addition,
        "data_totals" : data_totals

    }

    return dic

if __name__ == "__main__":

    building_size = 1000
    ppsf_remodel = 650
    cpsf_remodel = 175
    hard_soft_coef = 80
    units = 1
    addition_area = 600
    total_parking_area = 300
    rpsf_addition = 5
    ppsf_addition = 650
    cpsf_addition = 375
    cpsf_parking_addition = 75

    data = full_scope_of_work_calcs(building_size,ppsf_remodel,cpsf_remodel,hard_soft_coef,units,addition_area,total_parking_area,rpsf_addition,ppsf_addition,cpsf_addition,cpsf_parking_addition)

    from pprint import pprint
    pprint(data)
