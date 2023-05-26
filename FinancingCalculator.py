from mortgage import Loan
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

#_______________________________________________________________________________________

def mortgage_calculator(principal, interest, term):
    loan = Loan(principal=principal, interest=interest, term=term)
    monthly_payment = loan.monthly_payment
    monthly_payment = float(monthly_payment)
    return monthly_payment

def insurance_calculator(principal):
    return (principal * .01) / 12


def property_tax_calculator(purchase_price):
    return (purchase_price * .01) / 12

def construction_loan_calculator():
    pass

#_______________________________________________________________________________________

#Calculations

purchase_price = 1000000
downpayment = 0.2
principal = purchase_price * (1 - downpayment)
interest = .07
term = 30

monthly_mortgage = mortgage_calculator(principal, interest, term)
monthly_insurance = insurance_calculator(principal)
monthly_property_tax = property_tax_calculator(purchase_price)

total_monthly_payment = monthly_mortgage + monthly_insurance + monthly_property_tax
total_annual_payment = total_monthly_payment * 12

#_______________________________________________________________________________________

#create a dictionary to store the calculated values

data_dict = {

    'purchase_price': format_to_dollar_price(purchase_price),
    'downpayment': format_to_dollar_price(downpayment),
    'principal': format_to_dollar_price(principal),
    'interest': float_to_percentage(interest),
    'term': term,
    'monthly_mortgage': format_to_dollar_price(monthly_mortgage),
    'monthly_insurance': format_to_dollar_price(monthly_insurance),
    'monthly_property_tax': format_to_dollar_price(monthly_property_tax),
    'total_monthly_payment': format_to_dollar_price(total_monthly_payment),
    'total_annual_payment': format_to_dollar_price(total_annual_payment)

}

pprint(data_dict)

