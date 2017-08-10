import math  # Unnecessary if math.floor calc removed
import numpy

## Begin Input
## Feel free to adapt code as necessary to be used in the EconGuide program

tol = 1E-7
    # Honestly, this could probably be larger (1E-4 or 1E-3) and have no noticable effect on results
rec_list = [[0.1, 0.6, 1], [2, 1, -4], [3.1, 2, -2], [1.4, 1.57, -2.4]]
    # for recurring costs (OMR) or NDRBs
    # [rate, start_time, amount]
ot_list = [[0, -10], [5.3, -10], [14.347, -15]]
    # for one time costs or NDRBs [time,amt]
horizon = 20
inv_lambda = 35
ben_list = [0.25, 0.45, 1.25]
val_stat_life = 7.5
fat_averted = 0.2

## End Input

## Construct time series
## The time_series variable would need to be added, the cash_flow variable would be repurposed
## Constructing the time_series variable would be similar to what the code is doing with the cash_flow variable now.
## Instead of adding to a list of set length however, the variable would be getting new values appended for each cost

time_series = []
for item in rec_list:
    rate = item[0]
    start = item[1]
    amt = item[2]
    number_of_elements = math.floor(horizon/rate)  # Unnecessary
    i = 0
    while start + rate*i <= horizon+tol:
        time_series.append([start + rate*i,amt])
        i += 1

for item in ot_list:
    time_series.append(item)

## End construct time_series

## Construct cash_flow
## This could be a new function, as it only operates on the completed time_series list
## (In theory you could remove duplicates at each stage of contructing the time_series, I prefer one loop for simplicity).

time_series.sort(key=lambda x: x[0])
prev = -1
for i in range(len(time_series)): 
    # Loop to remove duplicate times. This loop is not necessary to get the correct value for IRR, 
    # as time_series contains the individual cash flow and its timing for all cases.
    if abs(time_series[i][0]-prev) <= tol: 
        # The real benefit of removing duplicates is to reduce the size of the cash_flow list,
        # which speeds up the bracketing method by reducing the number of calculations.
        time_series[i][0] = -1
        time_series[i-1][1] += time_series[i][1]
    else:
        prev = time_series[i][0]

cash_flow = []
## Loop to create list without duplicate values
for item in time_series:
    if item[0] != -1:
        cash_flow.append(item)

## cash_flow is now an input into the irr_for_all function.
## End contruct cash flow

## Find IRR
## The code from newIRR.py, edited for the new cash_flows format

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
            for item in cash_flows:
                dcf_list[index].append(item[1] * math.exp(-rate_list[index]*item[0]))  ## item to item[1], year to item[0]
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
            #print('The problem is here')
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

## End find IRR

## Check calculation

#irr = irr_for_all(cash_flow, horizon, inv_lambda, ben_list, val_stat_life, fat_averted)
#print(irr)

## End check calculation
