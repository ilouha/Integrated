from mortgage import Loan

def mortgage_calculator(principal, interest, term):
    loan = Loan(principal=principal, interest=interest, term=term)
    return loan.monthly_payment

def insurance_calculator():
    pass

def property_tax_calculator():
    pass

def construction_loan_calculator():
    pass

principal = 900000
interest = .07
term = 30

print(mortgage_calculator(principal, interest, term))


