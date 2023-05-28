#import Grasshopper as gh
import json
import math
from operator import truediv
from pprint import pprint
import pandas as pd


def listToTree(nestedList):
    
    """ Convert a nested python iterable to a datatree """
    
    dt = gh.DataTree[object]()
    for i,l in enumerate(nestedList):
        dt.AddRange(l,gh.Kernel.Data.GH_Path(i))
        
    return dt

def IncentiveMenu(incentive):

    # LADBS Ministerial ReviewA project requesting only a density bonus up to 35%, and/or reduced parking as 
    # specified by State Density Bonus law or LAMC§12.22 A.25, is considered by-right and reviewed through a 
    # ministerial building permit process. No CEQA review is conducted. These projects are not subject to an appeal.

    FilePath = "/Users/iliyamuzychuk/Documents/220929 Layouts Test/Incentives.json"
    f = open(FilePath)
    data = json.load(f)

    Incentive_Lib =  data[incentive]
    
    return Incentive_Lib

def flatteningJSON(b): 
    ans = {} 
    def flat(i, na =''):
        #nested key-value pair: dict type
        if type(i) is dict: 
            for a in i: 
                flat(i[a], na + a + '_')
        #nested key-value pair: list type
        elif type(i) is list: 
            j = 0  
            for a in i:                 
                flat(a, na + str(j) + '_') 
                j += 1
        else: 
            ans[na[:-1]] = i 
    flat(b) 
    return ans

#Loads Json
def LoadJson(name):

    FilePath = "/Users/iliyamuzychuk/Documents/220929 Layouts Test/{}".format(name)
    f = open(FilePath)
    data = json.load(f)
    
    return data

Attributes = LoadJson('Attributes.json')
FinancialVariables = LoadJson('FinancialVariables.json')
HardCosts = LoadJson('HardCosts.json')
softCosts = LoadJson('SoftCosts.json')
Incentives = LoadJson('Incentives.json')

#___________________________________________________________________________________________________________
#General Variables

Address = Attributes["Attributes"]["Address"]
LotArea = Attributes["Attributes"]["Lot Area"]
FAR = Attributes["Attributes"]["FAR"]
BuildableArea = Attributes["Attributes"]["Buildable Area"]
Story = Attributes["Attributes"]['Story Height']
UnitDensity = Attributes["Attributes"]["Unit Density"]
NetCoefficient = Attributes["Attributes"]["Net Area Coefficient"]
ParkingCoefficient = Attributes["Attributes"]["Parking Stall Area"]
HeightLimit = Attributes["Attributes"]["Height Limit"]
StallArea = Attributes["Attributes"]["Parking Stall Area"]
PercentageOfOccupancy = Attributes["Attributes"]["Percentage of Occupancy"]
LandCost = Attributes["Attributes"]["Land Cost"]


#___________________________________________________________________________________________________________
#Building Envelope Variables for testing the script

GrossFloorArea = 15000

#___________________________________________________________________________________________________________
#Financial Related Variables 

NetOperatingIncomeCoefficient = FinancialVariables["Financials Variables" ]["Net Operating Income Coefficient"]
AssumedCapRate = FinancialVariables["Financials Variables"]["Assumed Cap Rate"]
RentPerSF = FinancialVariables["Financials Variables"]["Rent Per SF"]

#___________________________________________________________________________________________________________

def constructionCost(GrossFloorArea,GrossParkingArea,OpenSpace,NRSF):
    
    #Load JSON with all parameters 
    FilePath = "/Users/iliyamuzychuk/Documents/220929 Layouts Test/HardCosts.json"
    f = open(FilePath)
    data = json.load(f)
    data = data["Hard Cost Per SF"]

    #Call all Parameters for calcualtions 
    ParkingCostSF = data["Subt Parking Cost per SF"]
    ResidentialNetAreaCostSF = data["Residential Net Area Cost per SF"]
    ResidentialAreaGrossCostSF = data["Residential Area Gross Cost per SF"]
    OpenSpaceCostSF = data["Open Space Cost per SF"]
    CommonAreaCostSF = data["Common Area Cost per SF"]
    GCCostSF = data["GC Cost per SF"]
    ContractorGIPercentage  = data["Contractor GI"]
 
    #Calculations
    SubParkingCost = GrossParkingArea * ParkingCostSF
    ServiceAreaCost = (GrossFloorArea - NRSF) * ResidentialAreaGrossCostSF
    NetResidnetialAreaCost = NRSF * ResidentialNetAreaCostSF
    OpenSpaceCost = OpenSpace * OpenSpaceCostSF
    
    HardCost = SubParkingCost + ServiceAreaCost + NetResidnetialAreaCost + OpenSpaceCost
    ContractorGI = HardCost * ContractorGIPercentage

    TotalHardCost = HardCost + ContractorGI

    return TotalHardCost
def softCost(HardCost):

    #Load JSON with all parameters 
    FilePath = "/Users/iliyamuzychuk/Documents/220929 Layouts Test/SoftCosts.json"
    f = open(FilePath)
    data = json.load(f)
    data = data["Soft Cost Percentage"]

    SoftCost = float(sum(data.values())) * HardCost   
    
    return SoftCost
def BuildingDescripting(LotArea,FAR,BuildableArea,Story,HeightLimit,incentive):
    
    incentives = IncentiveMenu(incentive)

    allowableBuildingArea = LotArea * FAR * (1 + incentives["Area Increase"])

    Stories = round(allowableBuildingArea/BuildableArea,0) + incentives["Height Increase"]

    BldgHeight = (Stories * Story) 

    if HeightLimit < BldgHeight:
        
        Height = HeightLimit
        Stories = math.floor(HeightLimit/Story) + incentives["Height Increase"]
        Height = Stories * Story

    else:

        Height = BldgHeight

    GrossFloorArea = Stories * BuildableArea
    MaxArea = allowableBuildingArea

    if Stories*BuildableArea > MaxArea:
        
        GrossFloorArea = MaxArea

    lotCoverage = BuildableArea/LotArea

    dic = {

        "Lot_Area" : round(LotArea,2),
        "Buildable_Area" : round(BuildableArea,2),
        "Maximum_Building_Area" : round(MaxArea,2),
        "Gross_Floor_Area" : round(GrossFloorArea,2),
        "Number_Of_Stories" : Stories,
        "Building_Height" : Height,
        "Lot_Coverage" : round(lotCoverage,2)

    }

    return dic

def UnitDescription(LotArea,UnitDensity,GrossFloorArea,NetCoefficient,incentive):

    incentives = IncentiveMenu(incentive)

    NumberOfUnits = math.floor((LotArea/UnitDensity) * (1 + incentives["Density Increase"]))
    AverageUnitSize = round((GrossFloorArea*NetCoefficient)/NumberOfUnits)
    NRSF = AverageUnitSize * NumberOfUnits

    keys = ["Number Of Units","Average Unit Size","NRSF"]
    values = [NumberOfUnits,AverageUnitSize,NRSF]

    dic = dict(zip(keys, values))

    dic = {

        "Number_Of_Units" : NumberOfUnits,
        "Average_Unit_Size" : AverageUnitSize,
        "Net_Rentable_SF" : NRSF

    }

    return dic

def ParkingDescription(AverageUnitSize,NumberOfUnits,StallArea,LotArea,incentive):

    incentives = IncentiveMenu(incentive)

    if AverageUnitSize <= 500:
        
        ParkingMultiplier = 1 

    elif AverageUnitSize > 500 and AverageUnitSize <= 1000:

        ParkingMultiplier = 1.5
        
    else:
        
        ParkingMultiplier = 2    

    TotalNumberParkingStalls = (ParkingMultiplier * NumberOfUnits) * (1 + incentives["Parking Reduction"])
    TotalNumberParkingStalls = math.ceil(TotalNumberParkingStalls)
    ParkingRatio = TotalNumberParkingStalls/NumberOfUnits
    ParkingGrossArea = TotalNumberParkingStalls * StallArea
    ParkingLevels = math.ceil(ParkingGrossArea/LotArea)

    dic = {

        "Total_Number_of_Parking_Stalls" : TotalNumberParkingStalls, 
        "Parking_Ratio" : round(ParkingRatio,2),
        "Parking_Gross_Area" : ParkingGrossArea,
        "Parking_Levels" : ParkingLevels
    }

    return dic 

def OpenSpaceDescription(AverageUnitSize,NumberOfUnits,incentive):

    incentives = IncentiveMenu(incentive)

    if AverageUnitSize <= 500:
        
        OpenSpacePerUnit = 100

    elif AverageUnitSize > 500 and AverageUnitSize <= 1000:

        OpenSpacePerUnit = 125
        
    else:
        
        OpenSpacePerUnit = 150

    OpenSpaceRequirements = (NumberOfUnits * OpenSpacePerUnit) * (1 + incentives["Open Space Reduction"])

    dic = {

        "Required_Open_Space" : OpenSpaceRequirements

    }

    return dic


def main():

    # Call out incentives here before other calculations 
    # If incentives are true than increase the dictionary by the incetives. 
    
    data = LoadJson('Incentives.json')
    Incetives = data.keys()
    FullInfo = {}

    for item in Incetives:
    
        incentiveType = item 

        BuildingInfo = BuildingDescripting(LotArea,FAR,BuildableArea,Story,HeightLimit,incentiveType)
    
        GrossFloorArea = BuildingInfo["Gross_Floor_Area"]

        UnitInfo = UnitDescription(LotArea,UnitDensity,GrossFloorArea,NetCoefficient,incentiveType)
        
        NumberOfUnits = UnitInfo["Number_Of_Units"]
        AverageUnitSize = UnitInfo["Average_Unit_Size"]

        ParkingInfo = ParkingDescription(AverageUnitSize,NumberOfUnits,StallArea,LotArea,incentiveType)
        OpenSpaceInfo = OpenSpaceDescription(AverageUnitSize,NumberOfUnits,incentiveType)

        #Financial Calculations 
        OpenSpace = OpenSpaceInfo["Required_Open_Space"]
        GrossParkingArea = ParkingInfo["Parking_Gross_Area"]
        
        NRSF = UnitInfo["Net_Rentable_SF"]
        ProjectHardCost = round(constructionCost(GrossFloorArea,GrossParkingArea,OpenSpace,NRSF),2)
        ProjectSoftCost = round(softCost(ProjectHardCost),2)

        TotalCost = round((ProjectHardCost + ProjectSoftCost),2)
        
        TotalCost = TotalCost + LandCost
        CashFlow = round((NRSF * RentPerSF) * PercentageOfOccupancy,2)
        NetOperatingIncome = CashFlow * NetOperatingIncomeCoefficient

        ProjectValuation = round(((NetOperatingIncome*12) / AssumedCapRate),2)
        ProjectSpread = -(TotalCost - ProjectValuation)
        ProjectSpreadPercentage = ProjectSpread/TotalCost

        CashFlowInfo = {
            
            "Project_Hard_Cost" : ProjectHardCost,
            "Project_Soft_Cost" : ProjectSoftCost,
            "Total_Cost" : TotalCost,
            "Cash_Flow" : CashFlow,
            "Net_Operating_Income" : NetOperatingIncome,
            "Project_Valuation" : ProjectValuation,
            "Project_Spread" : ProjectSpread,
            "Project_Spread_Percetage": ProjectSpreadPercentage, 
            "Cost_Per_Unit" : round(TotalCost/NumberOfUnits,2),
            "Land_Cost_Per_Unit" : round(LandCost/NumberOfUnits)
            }

        FullInfo_Incentive = {
            
            "BI" : BuildingInfo,
            "UI" : UnitInfo, 
            "PI" : ParkingInfo, 
            "OI" : OpenSpaceInfo,
            "FI" : CashFlowInfo
        }

        MenuOfIncentive = '{}'.format(item)
        FullInfo[MenuOfIncentive] = flatteningJSON(FullInfo_Incentive)
    
    #Setting up dataframe file that can be dropped as json or csv

    col_values = {}

    for key in FullInfo:
        col_values[key] = list(FullInfo[key].values())


    #setup DF rows and cols names 
    col_names = list(FullInfo.keys())
    row_names = list(FullInfo[col_names[0]].keys())

    print(Address)

    JsonFilePath = '/Users/iliyamuzychuk/Documents/220929 Layouts Test/Database/{}.json'.format(Address)
    CSVFilePath = '/Users/iliyamuzychuk/Documents/220929 Layouts Test/Database/{}.csv'.format(Address)

    JsonInteroperablePath = '/Users/iliyamuzychuk/Documents/220929 Layouts Test/Interoperable.json'\

    df = pd.DataFrame(col_values, index = row_names)
    df.to_json(JsonFilePath, orient='index')
    df.to_json(JsonInteroperablePath)
    df.to_csv(CSVFilePath)

    return df

#___________________________________________________________________________________________________________


 
#This section of the code is to split in for grasshopper parameters. 
# These functions are call out within Grasshopper 

#BuildingInfo = [list(BuildingInfo.keys()),list(BuildingInfo.values())]
#UnitInfo = [list(UnitInfo.keys()),list(UnitInfo.values())]
#ParkingInfo = [list(ParkingInfo.keys()),list(ParkingInfo.values())]
#OpenSpaceInfo = [list(OpenSpaceInfo.keys()),list(OpenSpaceInfo.values())]
#BuildingInfo = listToTree(BuildingInfo)
#UnitInfo = listToTree(UnitInfo)
#ParkingInfo = listToTree(ParkingInfo)
#OpenSpaceInfo = listToTree(OpenSpaceInfo)
