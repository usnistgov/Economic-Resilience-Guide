""" The fatalities package for the list of fatalities and the fatality class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-07
"""

import math

class Fatalities():
    """ Holds a list of all of the externalities and performs the fatality-related calculations."""
    def __init__(self, disaster_rate, discount_rate, stat_value, horizon):
        self.averted = 0
        self.desc = "N/A"

        self.disaster_rate = float(disaster_rate)
        self.discount_rate = float(discount_rate)
        self.stat_life = float(stat_value)
        self.horizon = float(horizon)
        self.stat_value = float(stat_value)

        self.stat_value_averted = self.on_dis_occ(self.stat_value * self.averted, self.horizon,
                                                  self.disaster_rate, self.discount_rate)
        self.stat_averted = 1/self.disaster_rate * self.horizon * self.averted

        self.num_range = [0, 0]
        self.value_range = [0, 0]


    def update(self, averted, desc):
        """ Makes a new fatality and adds it to the list of fatality types. """
        self.averted = float(averted)
        self.desc = ""
        for i in range(len(desc)):
            if i != 0:
                self.desc += ','
            self.desc += desc[i]

        self.stat_value_averted = self.on_dis_occ(self.stat_value * self.averted, self.horizon,
                                                  self.disaster_rate, self.discount_rate)
        self.stat_averted = 1/self.disaster_rate * self.horizon * self.averted

    def on_dis_occ(self, value, horizon, disaster_rate, discount_rate):
        """ Used for expected value on disaster occurence. """
        horizon = float(horizon)
        value = float(value)
        eqn_lambda = 1/disaster_rate
        k = discount_rate/100
        try:
            mult = eqn_lambda / math.fabs(1 - math.exp(-k))* (1 - math.exp(-k * horizon))
        except ZeroDivisionError:
            mult = eqn_lambda * horizon
        return mult * value
