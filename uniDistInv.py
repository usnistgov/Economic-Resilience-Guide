def uniDistInv(rand, a, b):
    if a > b:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"

    return rand*(b-a)+a

def uniDistCDF(value, a, b):
    if a > b:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"

    if value < a:
        return 0
    elif value > b:
        return 1
    else:
        return (value-a)/(b-a)
