import math 
from pprint import pprint

#Declaration of variables
total_area = 30000
total_units = 50 
percentage_one_bedrooms = 25
percentage_two_bedrooms = 35 

desired_area_one_bedroom = 400
desired_area_two_bedroom = 600
desired_area_three_bedroom = 800


def unit_program(total_area,
                 program_percentage,
                 proposed_unit_area):

    total_program_area_for_unit_type = total_area * (program_percentage/100)
    total_units_of_type = math.floor(total_program_area_for_unit_type / proposed_unit_area)
    unit_of_type_average_area = round(total_program_area_for_unit_type / total_units_of_type,2)

    total_program_area = total_units_of_type * unit_of_type_average_area
    

    return total_units_of_type, unit_of_type_average_area,total_program_area

def unit_calcs(total_area,
               percentage_one_bedrooms,
               percentage_two_bedrooms,
               desired_area_one_bedroom,
               desired_area_two_bedroom,
               desired_area_three_bedroom):

    percentage_three_bedrooms = 100 - (percentage_one_bedrooms + percentage_two_bedrooms)

    one_bedroom = unit_program(total_area,percentage_one_bedrooms,desired_area_one_bedroom)
    two_bedroom = unit_program(total_area,percentage_two_bedrooms,desired_area_two_bedroom)
    three_bedroom = unit_program(total_area,percentage_three_bedrooms,desired_area_three_bedroom)

    
    dic = {

        "no_one_bedroom": one_bedroom[0],
        "avg_one_bedroom_area": one_bedroom[1],
        "no_two_bedroom": two_bedroom[0],
        "avg_two_bedroom_area": two_bedroom[1],
        "no_three_bedroom": three_bedroom[0],
        "avg_three_bedroom_area": three_bedroom[1],
        "total_net_area": one_bedroom[2] + two_bedroom[2] + three_bedroom[2]

    }

    return dic


dic = unit_calcs(total_area,percentage_one_bedrooms,percentage_two_bedrooms,desired_area_one_bedroom,desired_area_two_bedroom,desired_area_three_bedroom)

key_list = [

    "no_one_bedroom",
    "avg_one_bedroom_area",
    "no_two_bedroom",
    "avg_two_bedroom_area",
    "no_three_bedroom",
    "avg_three_bedroom_area"

]

values  = []

for key in key_list:
    values.append(dic[key])



    