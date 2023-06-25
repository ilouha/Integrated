import math 
from pprint import pprint

#Declaration of variables
total_program_area = 300000
total_achievable_units = 300

residential = True
total_area = total_program_area

percentage_studios = 35
percentage_one_bedrooms = 25
percentage_two_bedrooms = 35 

desired_area_studios = 300
desired_area_one_bedroom = 400
desired_area_two_bedroom = 600
desired_area_three_bedroom = 800

def format_to_sf_area(value):
    if isinstance(value, (int, float)):
        formatted_value = "{:,.2f} SF".format(value)
    else:
        raise TypeError("Unsupported value type. Only int and float are supported.")
    
    return formatted_value
    

def unit_program(total_area,
                 program_percentage,
                 proposed_unit_area,
                 total_achievable_units):

    total_program_area_for_unit_type = (total_achievable_units * (program_percentage/100))*proposed_unit_area
    total_units_of_type = total_achievable_units * (program_percentage/100)
    unit_of_type_average_area = round(total_program_area_for_unit_type / total_units_of_type,2)

    total_program_area = total_units_of_type * unit_of_type_average_area

    return total_units_of_type, unit_of_type_average_area,total_program_area

def unit_calcs(total_area,
               percentage_studios,
               percentage_one_bedrooms,
               percentage_two_bedrooms,
               desired_area_studios,
               desired_area_one_bedroom,
               desired_area_two_bedroom,
               desired_area_three_bedroom):

    percentage_three_bedrooms = 100 - (percentage_studios + percentage_one_bedrooms + percentage_two_bedrooms)
    
    studios = unit_program(total_area,percentage_studios,desired_area_studios,total_achievable_units)
    one_bedroom = unit_program(total_area,percentage_one_bedrooms,desired_area_one_bedroom,total_achievable_units)
    two_bedroom = unit_program(total_area,percentage_two_bedrooms,desired_area_two_bedroom,total_achievable_units)
    three_bedroom = unit_program(total_area,percentage_three_bedrooms,desired_area_three_bedroom,total_achievable_units)

    
    dic = {
        "unit_breakdown" : "----",
        "U.no_studios": studios[0],
        "U.avg_studio_area" : format_to_sf_area(studios[1]),
        "U.no_one_bedroom": one_bedroom[0],
        "U.avg_one_bedroom_area": format_to_sf_area(one_bedroom[1]),
        "U.no_two_bedroom": two_bedroom[0],
        "U.avg_two_bedroom_area": format_to_sf_area(two_bedroom[1]),
        "U.no_three_bedroom": three_bedroom[0],
        "U.avg_three_bedroom_area": format_to_sf_area(three_bedroom[1]),
        "U.total_net_area": format_to_sf_area(studios[2] + one_bedroom[2] + two_bedroom[2] + three_bedroom[2]),
        "U.total_units": studios[0] + one_bedroom[0] + two_bedroom[0] + three_bedroom[0]

    }

    return dic

if residential is True: 

    dic = unit_calcs(total_area,percentage_studios,percentage_one_bedrooms,percentage_two_bedrooms,desired_area_studios,desired_area_one_bedroom,desired_area_two_bedroom,desired_area_three_bedroom)
    
    resi_key_list = [
        
        "unit_breakdown",
        "U.no_studios",
        "U.avg_studio_area",
        "U.no_one_bedroom",
        "U.avg_one_bedroom_area",
        "U.no_two_bedroom",
        "U.avg_two_bedroom_area",
        "U.no_three_bedroom",
        "U.avg_three_bedroom_area",
        "U.total_units",
        "U.total_net_area"
    
    ]
    
    resi_info  = []
    for item in resi_key_list:
        resi_info.append(item + ': ' + str(dic[item]))
        
    resi_values  = []
    
    for key in resi_key_list:
        resi_values.append(dic[key])


pprint(resi_info)
    