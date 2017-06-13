""" The costs package for the list of costs and the cost class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

import math
import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv

class Costs():
    """ Holds a list of all of the costs and performs the cost-related calculations."""

    def __init__(self, discount_rate, horizon):

        self.indiv = []
        self.d_sum = 0
        self.i_sum = 0
        self.omr_1_sum = 0
        self.omr_r_sum = 0

        self.total = 0

        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

        self.direct_range = [0, 0]
        self.indirect_range = [0, 0]
        self.omr_one_range = [0, 0]
        self.omr_r_range = [0, 0]

    def new_cost(self, line):
        """ Makes a new cost and adds it to the list of cost types. """
        if line[0] == 'Uncertainty':
            self.indiv[-1].dist = line[1]
            self.indiv[-1].range = list(line[2:8])
        else:
            opts = {}
            opts['title'] = line[0]
            opts['cost_type'] = line[1]
            opts['omr_type'] = line[2]
            opts['omr_times'] = [line[3], line[4], line[5]]
            opts['amount'] = float(line[6])
            opts['desc'] = line[7:]
            this_cost = Cost(**opts)
            self.indiv.append(this_cost)

    def make_sum(self):
        """ Calculates the additional Direct Costs, Indirect Costs, and
            OMR costs both initial and recurring. """
        self.d_sum = 0
        self.i_sum = 0
        self.omr_1_sum = 0
        self.omr_r_sum = 0
        for cost in self.indiv:
            if cost.cost_type == "direct":
                self.d_sum += cost.amount
            elif cost.cost_type == "indirect":
                self.i_sum += cost.amount
            elif cost.cost_type == "omr":
                if cost.omr_type == "one-time":
                    self.omr_1_sum += self.calc_one_time(cost.amount, cost.times[0])
                elif cost.omr_type == "recurring":
                    self.omr_r_sum += self.calc_recur(cost.amount, cost.times[0], cost.times[1])
        self.total = self.d_sum + self.i_sum + self.omr_1_sum + self.omr_r_sum

    def calc_one_time(self, value, time):
        """Equation used for One-time OMR costs"""
        time = float(time)
        value = float(value)
        return (math.exp(-(float(self.discount_rate) / 100) * time)) * value

    def calc_recur(self, value, start, rate):
        """Equation used for Recurring OMR costs"""
        value = float(value)
        year = float(start)
        rate = float(rate)
        total = 0

        while year <= float(self.horizon):
            total += value * math.exp(-(float(self.discount_rate) / 100) * (year))
            year += rate
        return total

    def one_iter(self, old_cost_list):
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist, 'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        delta_cost = Costs(self.discount_rate, self.horizon)
        for cost in old_cost_list:
            cost_dict = {'title': cost.title,
                        'cost_type': cost.cost_type,
                        'omr_type': cost.omr_type,
                        'omr_times': cost.times,
                        'desc': cost.desc}
            cost_dict['amount'] = dist_dict[cost.dist](np.random.uniform(), cost.amount, cost.range)
            delta_cost.indiv.append(Cost(**cost_dict))

        return delta_cost

class Cost():
    """ Holds all of the information about costs. """
    types = ["direct", "indirect", "omr"]
    omr_types = ["none", "one-time", "recurring"]
    def __init__(self, title="none", cost_type="none", omr_type="none", amount=0,
                 omr_times="none", desc="N/A"):
        assert cost_type in self.types
        assert omr_type in self.omr_types
        self.title = title
        self.cost_type = cost_type
        self.omr_type = omr_type
        self.amount = float(amount)
        self.times = omr_times
        self.desc = ""
        for bit in desc:
            self.desc += bit
        for num in self.times:
            num = float(num)

        self.range = ['<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>']
        self.dist = "none"

    def add_uncertainty(self, new_range, distribution):
        """ Adds uncertainty to a specific costefit."""

        self.range = new_range
        self.dist = distribution
