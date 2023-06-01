#create an annuity formula to calculate appreciation over a term of months

def annuity_formula(principal, interest, term):
    numerator = principal * interest
    denominator = 1 - (1 + interest) ** (-term)
    return numerator / denominator

print(annuity_formula(1000000, 0.07, 360))