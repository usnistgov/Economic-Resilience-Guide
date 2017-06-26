import math
import numpy

def triDistInv(rand, mid, inputs):
    """ Returns a vlue within the -tri- distribution."""
    a = float(inputs[0])
    b = float(mid)
    c = float(inputs[1])
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

def uniDistInv(rand, _mid, inputs):
    """ Returns a value within the -rect- disctribution."""
    a = float(inputs[0])
    c = float(inputs[1])
    if a > c:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"
    return rand*(c-a)+a

def none_dist(_rand, mid, _inputs):
    """ Gives the -none-type distribution"""
    return mid

def discrete_dist_inv(rand, _mid, inputs):
    """ Returns a value within the -discrete- distribution."""
    if rand < float(inputs[3])/100:
        return inputs[0]
    elif rand < float(inputs[3])/100 + float(inputs[4])/100:
        return inputs[1]
    else:
        return inputs[2]

def gauss_dist_inv(rand, mid, inputs):
    """ Uses numpy.random.normal to return a value with the -gauss- distribution."""
    ### NOTE: It's mad about this call, claiming it will pull an error. It doesn't
    return numpy.random.normal(float(mid), float(inputs[0]))

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

def uniDistCDF(value, a, _b, c):
    if a > c:
        return "Input Error: a is the lower bound of the distribution and must be less than b (the upper bound of the distribution"

    if value < a:
        return 0
    elif value > c:
        return 1
    else:
        return (value-a)/(c-a)
