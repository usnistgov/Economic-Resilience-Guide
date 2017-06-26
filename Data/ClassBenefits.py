""" The benefits package for the list of benefits and the benefit class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

import math
import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv

class Benefits():
    """ Holds a list of all of the benefits and performs the benefit-related calculations."""
    def __init__(self, disaster_rate, discount_rate, horizon):
        self.indiv = []

        self.d_sum = 0
        self.d_sum_no_discount = 0
        self.i_sum = 0
        self.i_sum_no_discount = 0
        self.r_sum = 0
        self.r_sum_no_discount = 0

        self.total = 0

        self.dis_rate = float(disaster_rate)
        self.disc_rate = float(discount_rate)
        self.horizon = float(horizon)

        self.direct_range = [0, 0]
        self.indirect_range = [0, 0]
        self.res_rec_range = [0, 0]

    def new_ben(self, line):
        """ Makes a new benefit and adds it to the list of benefit types. """
        if line[0] == 'Uncertainty':
            self.indiv[-1].dist = line[1]
            self.indiv[-1].range = list(line[2:8])
        else:
            opts = {}
            opts['title'] = line[0]
            opts['ben_type'] = line[1]
            opts['amount'] = float(line[2])
            opts['desc'] = line[3:]
            this_ben = Benefit(**opts)
            self.indiv.append(this_ben)

    def make_sum(self):
        """ Calculates reduction in response and recovery costs, direct losses,
            and indirect losses. """
        self.d_sum = 0
        self.i_sum = 0
        self.r_sum = 0
        for ben in self.indiv:
            if ben.ben_type == "direct":
                self.d_sum += ben.amount
            elif ben.ben_type == "indirect":
                self.i_sum += ben.amount
            elif ben.ben_type == "res-rec":
                self.r_sum += ben.amount
        self.d_sum_no_discount = self.d_sum
        self.i_sum_no_discount = self.i_sum
        self.r_sum_no_discount = self.r_sum
        self.d_sum = self.on_dis_occ(self.d_sum, self.horizon, self.dis_rate, self.disc_rate)
        self.i_sum = self.on_dis_occ(self.i_sum, self.horizon, self.dis_rate, self.disc_rate)
        self.r_sum = self.on_dis_occ(self.r_sum, self.horizon, self.dis_rate, self.disc_rate)
        self.total = self.d_sum + self.i_sum + self.r_sum


    def on_dis_occ(self, value, horizon, disaster_rate, discount_rate):
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

    def one_iter(self, old_ben_list):
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist, 'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        delta_ben = Benefits(self.dis_rate, self.disc_rate, self.horizon)
        for ben in old_ben_list:
            ben_dict = {'title': ben.title,
                        'ben_type': ben.ben_type,
                        'desc': ben.desc}
            ben_dict['amount'] = dist_dict[ben.dist](np.random.uniform(), ben.amount, ben.range)
            delta_ben.indiv.append(Benefit(**ben_dict))

        return delta_ben

class Benefit():
    """ Holds all of the information about benefits. """
    types = ["direct", "indirect", "res-rec"]
    def __init__(self, title="none", ben_type="none", amount=0, desc="N/A"):
        try:
            assert ben_type in self.types
        except AssertionError:
            print(title, ben_type)
            raise AssertionError
        self.title = title
        self.ben_type = ben_type
        self.amount = float(amount)
        self.desc = ""
        for bit in desc:
            self.desc += bit

        self.range = ['<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>']
        self.dist = "none"

    def add_uncertainty(self, new_range, distribution):
        """ Adds uncertainty to a specific benefit."""

        self.range = new_range
        self.dist = distribution
