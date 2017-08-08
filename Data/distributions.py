""" The distributions.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import math
import numpy

def triDistInv(rand, mid, inputs):
    """ Returns a vlue within the -tri- distribution."""
    aaa = float(inputs[0])
    bbb = float(mid)
    ccc = float(inputs[1])
    if aaa > bbb:
        aaa = float(mid)
        bbb = float(inputs[0])
        ccc = float(inputs[1])
    if aaa > bbb:
        return "a must be less than b"
    elif bbb > ccc:
        return "b must be less than c"
    if aaa > ccc:
        return "a must be less than c"
    vertex = (bbb-aaa)/(ccc-aaa)
    if rand <= vertex:
        return aaa+math.sqrt(rand*(ccc-aaa)*(bbb-aaa))
    else:
        return ccc-math.sqrt((1-rand)*(ccc-aaa)*(ccc-bbb))

def uniDistInv(rand, mid, inputs):
    """ Returns a value within the Rectangular disctribution."""
    aaa = float(inputs[0])
    bbb = float(mid)
    ccc = float(inputs[1])
    if aaa > bbb:
        aaa = float(mid)
        bbb = float(inputs[0])
        ccc = float(inputs[1])
    if aaa > ccc:
        return ("Input Error: a is the lower bound of the distribution and "
                "must be less than b (the upper bound of the distribution)")
    return rand*(ccc-aaa)+aaa

def none_dist(_rand, mid, _inputs):
    """ Gives the Exact distribution"""
    return mid

def discrete_dist_inv(rand, _mid, inputs):
    """ Returns a value within the discrete distribution."""
    if rand < float(inputs[3])/100:
        return inputs[0]
    elif rand < float(inputs[3])/100 + float(inputs[4])/100:
        return inputs[1]
    else:
        return inputs[2]

def gauss_dist_inv(_rand, mid, inputs):
    """ Uses numpy.random.normal to return a value with the Gaussian distribution."""
    ### NOTE: It's mad about this call, claiming it will pull an error. It doesn't
    return numpy.random.normal(float(mid), float(inputs[0]))

def triDistCDF(value, aaa, bbb, ccc):
    """ The CDF for a triangle distribution. """
    if aaa > bbb:
        return "a must be less than b"
    elif bbb > ccc:
        return "b must be less than c"
    if aaa > ccc:
        return "a must be less than c"
    #vertex = (bbb-aaa)/(ccc-aaa)

    if value < aaa:
        return 0
    elif value <= bbb:
        return 2*(value-aaa)**2/((ccc-aaa)*(bbb-aaa))
    if value <= ccc:
        return 1-(ccc-value)**2/((ccc-aaa)*(ccc-bbb))
    else:
        return 1

def uniDistCDF(value, aaa, _bbb, ccc):
    """ The CDF for a uniform distribution."""
    if aaa > ccc:
        return ("Input Error: a is the lower bound of the distribution "
                "and must be less than b (the upper bound of the distribution")

    if value < aaa:
        return 0
    elif value > ccc:
        return 1
    else:
        return (value-aaa)/(ccc-aaa)

##### Functions shared by several item types
def on_dis_occ(value, horizon, disaster_rate, discount_rate):
    """ Used for expected value on disaster occurence. """
    disaster_rate = float(disaster_rate)
    discount_rate = float(discount_rate)
    horizon = float(horizon)
    value = float(value)
    eqn_lambda = 1/disaster_rate
    k = discount_rate/100
    try:
        mult = eqn_lambda / math.fabs(1 - math.exp(-k))* (1 - math.exp(-k * horizon))
    except ZeroDivisionError:
        mult = eqn_lambda * horizon
    return mult * value

def calc_one_time(discount_rate, value, time):
    """Equation used for one-time OMR costs"""
    time = float(time)
    value = float(value)
    return (math.exp(-(float(discount_rate) / 100) * time)) * value

def calc_recur(discount_rate, horizon, value, start, rate):
    """Equation used for Recurring OMR costs"""
    value = float(value)
    year = float(start)
    rate = float(rate)
    total = 0

    while year <= float(horizon):
        total += value * math.exp(-(float(discount_rate) / 100) * (year))
        year += rate
    return total
