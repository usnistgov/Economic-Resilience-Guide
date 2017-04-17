"""
    Does the irr calculation without the aid of numpy for ease of packaging
"""
import math
import numpy

MAX_LOG_RATE = 1e3
BASE_TOL = 1e-12
BASE_RATE_TOL = 1e-4

def irr_for_all(cash_flows, horizon, inv_lambda, ben_list, value_stat_life, fat_avert):
    """ Uses David's method to calculate the IRR.
    ben_list is expected to have:
       Direct Loss Reduction, Indirect Loss Reduction, R&R Cost Reduction  """
    rate_list = [0, 0.5, 1]

    # Drops the values of cash_flows, ben_list, value_stat_life
    #  by a factor of 10^6 to avoid OverflowError
    #for cost in cash_flows:
    #    cost = cost/(1e6)
    #for cost in ben_list:
    #    cost = cost/(1e6)
    #value_stat_life = value_stat_life/(1e6)

    for _ in range(200):
        rate_list[1] = (rate_list[2] + rate_list[0])/2
        if abs(rate_list[2]-rate_list[0]) < BASE_RATE_TOL:
            return rate_list[1]
        #print('rate', rate_list)

        dcf_list = []
        ddrb_list = []
        npv_list = []
        for index in range(len(rate_list)):
            dcf_list.append([])
            year = 0  ## Added to keep track of year
            for item in cash_flows:
                dcf_list[index].append(item * math.exp(-rate_list[index]*year))  ## Changed cash_flows.index(item) to year
                year += 1  ## Iterate on year
            ddrb_list.append(discount(rate_list[index], horizon, inv_lambda, ben_list,
                                      float(value_stat_life), float(fat_avert)))
            npv_list.append(sum(dcf_list[index])+ddrb_list[index])

        old_sign = check_sign(npv_list[0])
        sign_change = False
        #print('npv', npv_list)
        for index in range(1, len(npv_list)):
            new_sign = check_sign(npv_list[index])
            if new_sign == 0:
                return rate_list[index]
            if not new_sign == old_sign:
                sign_change = True
                rate_list[0] = rate_list[index-1]
                rate_list[2] = rate_list[index]
                break
        if not sign_change:
            print('The problem is here')
            raise ValueError

    return rate_list[1]

def check_sign(value):
    """ -1 for negative sign, 0 for within BASE_TOL, 1 for positive """
    if abs(value) <= BASE_TOL:
        return 0
    elif value < 0:
        return -1
    elif value > 0:
        return 1
    else:
        raise ValueError

def zero_discount(horizon, inv_lambda, ben_list, value_stat_life, fat_avert):
    """ Calculates the discounted values in the case of a discount of 0."""
    sum = 0
    inv_lambda = float(inv_lambda)
    horizon = float(horizon)
    for benefit in ben_list:
        sum += (1/inv_lambda) * horizon * benefit
    sum += (1/inv_lambda) * horizon * value_stat_life * fat_avert
    return sum

def discount(dr, horizon, inv_lambda, ben_list, value_stat_life, fat_avert):
    """ Calculates the discounted values."""
    if dr == 0:
        sum = zero_discount(horizon, inv_lambda, ben_list, value_stat_life, fat_avert)
    else:
        sum = 0
        for benefit in ben_list:
            sum += (1/inv_lambda) * (1-math.exp(-dr))**(-1) * (1-math.exp(-dr*horizon)) * benefit
        sum += (1/inv_lambda) * (1-math.exp(-dr))**(-1) * (1-math.exp(-dr*horizon)) * value_stat_life * fat_avert
    return sum


##def irr(stream, tol=BASE_TOL):
##    """
##    Calculates continuously compounding irr
##    """
##    rate_lo, rate_hi = -MAX_LOG_RATE, +MAX_LOG_RATE
##    sgn = my_sign(stream[0]) # f(x) is decreasing
##    for _ in range(200):
##        rate = (rate_lo + rate_hi)/2
##        range_values = range(len(stream))
##        #range_values = numpy.arange(len(stream))
##        # Factor exp(max_value) out because it doesn't affect the sign
##        max_value = my_max(range_values, mult=-rate)
##        #max_value = max(-rate * range_values)
##        f_exp = my_exp(range_values, mult=-rate, add=-max_value)
##        #f_exp = numpy.exp(-rate * range_values - max_value)
##        test = my_dot(f_exp, stream)
##        #test = numpy.dot(f_exp, stream)
##        if abs(test) < tol * math.exp(-max_value):
##            break
##        if test * sgn > 0:
##            rate_hi = rate
##        else:
##            rate_lo = rate
##    rate = (rate_lo + rate_hi) / 2
##    return math.exp(rate) - 1

def my_sign(value):
    """
    The equivalent of numpy's sign function.
    """
    if value < 0:
        return -1
    elif value == 0:
        return 0
    else:
        return 1

def my_max(some_array, mult=1):
    """
    Finds the max of some_array multiplied by mult.
    """
    max_value = mult * some_array[0]
    for value in some_array:
        if mult * value > max_value:
            max_value = mult * value
    return max_value

def my_exp(some_array, mult=1, add=0, mult_list=None):
    """
    Takes the exponent of every value of the array.
    """
    if mult_list == None:
        mult_list = [1]*len(some_array)
    new_exp = []
    for value in range(len(some_array)):
        try:
            #new_exp.append(numpy.exp(mult * mult_list[value] * value + add))
            new_exp.append(some_array[value]*math.exp(mult * mult_list[value] * value + add))
        except OverflowError:
            return new_exp
    return new_exp

def my_dot(array_a, array_b):
    """
    A 2D dot product
    """
    if len(array_a) != len(array_b):
        raise ValueError
    dot = sum([a_item*b_item for (a_item, b_item) in zip(array_a, array_b)])
    return dot
