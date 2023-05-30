import pandas as pd 
import json

zipcode = '90066'
#run comps app
#from CompsApp import process_zipcode_data
#process_zipcode_data(zipcode)

#run proforam app 
from ProformaCalcs import ProformaCalc
ProformaCalc()

#run assumptions app 
from Assumptions import Assumtions
Assumtions()

