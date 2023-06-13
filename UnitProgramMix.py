import math 
import json 

#Declaration of variables
total_area = 30000
total_units = 50 
percentage_one_bedrooms = 25
percentage_two_bedrooms = 25 
percentage_three_bedrooms = 100 - (percentage_one_bedrooms + percentage_two_bedrooms)

def unit_program(total_area,total_units,program_percentage):

    no_units = math.floor(total_units*(program_percentage/100))
    average_unit_area = (total_area * (program_percentage/100))/no_units

    return no_units, average_unit_area


print(unit_program(total_area,total_units,percentage_one_bedrooms))
    