def uniDistInv(rand, a, _b, c):
    if a > c:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"

    return rand*(c-a)+a

def uniDistCDF(value, a, _b, c):
    if a > c:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"

    if value < a:
        return 0
    elif value > c:
        return 1
    else:
        return (value-a)/(c-a)
