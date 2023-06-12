#create an annuity formula to calculate appreciation over a term of months


#initial investment
investment = 10000
#number of years to calculate appreciation
term = 5
#annual appreciation rate
apperciation_rate = 0.03

def appreciation(investment,term,apperciation_rate):

    #convert annual rate to monthly rate
    monthly_rate = apperciation_rate/12

    #convert term to months
    months = term * 12

    #calculate appreciation
    total = investment
    
    for i in range(months):
        total = total * (1 + monthly_rate)

    return total

print(appreciation(investment,term,apperciation_rate))