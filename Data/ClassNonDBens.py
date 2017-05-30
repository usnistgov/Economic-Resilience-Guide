""" The non-disaster related benefits package for the list of non-disaster related benefits
        and the non-disaster related benefits class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

import math

class NonDBens():
    """ Holds a list of all of the benefits and performs the benefit-related calculations."""
    def __init__(self, discount_rate, horizon):
        self.indiv = []

        self.one_sum = 0
        self.r_sum = 0

        self.total = 0

        self.horizon = float(horizon)
        self.discount_rate = float(discount_rate)

    def new_ben(self, line):
        """ Makes a new benefit and adds it to the list of benefit types. """
        opts = {}
        opts['title'] = line[0]
        opts['ben_type'] = line[1]
        opts['times'] = [line[2], line[3], line[4]]
        opts['amount'] = line[5]
        opts['desc'] = line[6]
        this_ben = Benefit(**opts)
        self.indiv.append(this_ben)

    def make_sum(self):
        """ Calculates the value of all Non-Disaster related benefits."""
        self.one_sum = 0
        self.r_sum = 0
        for ben in self.indiv:
            if ben.ben_type == "one-time":
                self.one_sum += self.calc_one_time(ben.amount, ben.times[0])
            elif ben.ben_type == "recurring":
                self.r_sum += self.calc_recur(ben.amount, ben.times[0], ben.times[1])
            else:
                print(ben.ben_type)
        self.total = self.one_sum + self.r_sum

    def calc_one_time(self, value, time):
        """Equation used for One-time OMR costs"""
        value = float(value)
        time = float(time)
        return (math.exp(-(float(self.discount_rate) / 100) * time)) * value

    def calc_recur(self, value, start, rate):
        """Equation used for Recurring OMR costs"""
        total = 0
        year = float(start)
        value = float(value)
        rate = float(rate)

        while year <= float(self.horizon):
            total += value * math.exp(-(float(self.discount_rate) / 100) * year)
            year += rate
        return total

class Benefit():
    """ Holds all of the information about benefits. """
    types = ["one-time", "recurring"]
    def __init__(self, title="none", times=[0, 0, 0], ben_type="none", amount=0, desc="N/A"):
        assert ben_type in self.types
        self.title = title
        self.ben_type = ben_type
        self.times = times
        self.amount = amount
        self.desc = desc
