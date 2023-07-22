from pprint import pprint
import math 

#useful code for mortage calculation:
#https://medium.com/personal-finance-analytics/mortgage-calculator-python-code-94d976d25a27

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

#_______________________________________________________________________________________

def calc_mortgage(principal, interest, years):
    '''
    given mortgage loan principal, interest(%) and years to pay
    calculate and return monthly payment amount
    '''
    # monthly rate from annual percentage rate
    interest_rate = interest/(100 * 12)
    # total number of payments
    payment_num = years * 12
    # calculate monthly payment
    payment = principal * \
        (interest_rate/(1-math.pow((1+interest_rate), (-payment_num))))
    return payment

def insurance_calculator(principal):
    return (principal * .01) / 12

def property_tax_calculator(purchase_price):
    return (purchase_price * .01) / 12

#_______________________________________________________________________________________

#Mortgage Calculator



def financing_calculator(purchase_price,downpayment,interest,term,permit_length):
#_______________________________________________________________________________________

    purchase_price = purchase_price
    downpayment =  downpayment/100

    interest = interest
    term = term
    permit_length = permit_length

    principal = purchase_price * (1 - downpayment)
    required_downpayment = purchase_price * downpayment

    monthly_mortgage = calc_mortgage(principal, interest, term)
    monthly_insurance = insurance_calculator(principal)
    monthly_property_tax = property_tax_calculator(purchase_price)

    total_monthly_payment = monthly_mortgage + monthly_insurance 
    total_annual_payment = total_monthly_payment * 12
    holding_cost = total_monthly_payment * permit_length
    #_______________________________________________________________________________________

    #create a dictionary to store the calculated values

    data_dict = {

        'purchase_price': format_to_dollar_price(purchase_price),
        'downpayment': float_to_percentage(downpayment),
        'principal': format_to_dollar_price(principal),
        'interest': float_to_percentage(interest/100),
        'term': term,
        'monthly_mortgage': format_to_dollar_price(monthly_mortgage),
        'monthly_insurance': format_to_dollar_price(monthly_insurance),
        'monthly_property_tax': format_to_dollar_price(monthly_property_tax),
        'total_monthly_payment': format_to_dollar_price(total_monthly_payment),
        'total_annual_payment': format_to_dollar_price(total_annual_payment),
        'required_downpayment': format_to_dollar_price(required_downpayment),
        'holding_cost': format_to_dollar_price(holding_cost),

    }


    return data_dict

