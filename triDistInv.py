import math

def triDistInv(rand,a,b,c):
    if a > b:
        return "a must be less than b"
    elif b > c:
        return "b must be less than c"
    if a > c:
        return "a must be less than c"
    vertex = (b-a)/(c-a)

    if rand <= vertex:
        return a+math.sqrt(rand*(c-a)*(b-a))
    else:
        return c-math.sqrt((1-rand)*(c-a)*(c-b))

def triDistCDF(value,a,b,c):
    if a > b:
        return "a must be less than b"
    elif b > c:
        return "b must be less than c"
    if a > c:
        return "a must be less than c"
    vertex = (b-a)/(c-a)

    if value < a:
        return 0
    elif value <= b:
        return 2*(value-a)**2/((c-a)*(b-a))
    if value <= c:
        return 1-(c-value)**2/((c-a)*(c-b))
    else:
        return 1
