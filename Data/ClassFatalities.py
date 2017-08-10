""" The fatalities package for the list of fatalities and the fatality class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

from Data.distributions import on_dis_occ

class Fatalities():
    """ Holds a list of all of the externalities and performs the fatality-related calculations."""
    def __init__(self, disaster_rate, discount_rate, stat_value, horizon):
        # Basic information
        self.averted = 0
        self.desc = "N/A"
        self.stat_life = float(stat_value)

        # Disaster rate, discount rate, horizon, etc
        self.disaster_rate = float(disaster_rate)
        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

        # Stat values
        self.stat_value_averted = on_dis_occ(self.stat_life * self.averted, self.horizon,
                                             self.disaster_rate, self.discount_rate)
        self.stat_averted = 1/self.disaster_rate * self.horizon * self.averted

        # Uncertainty ranges
        self.num_range = [0, 0]
        self.value_range = [0, 0]


    def update(self, averted, desc, amount):
        """ Makes a new fatality and adds it to the list of fatality types. """
        amount = amount.replace(',', '')
        self.stat_life = float(amount)
        self.averted = float(averted)
        self.desc = ""
        if isinstance(desc, list):
            for i in range(len(desc)):
                if i != 0:
                    self.desc += ','
                self.desc += desc[i]
        else:
            self.desc = desc

        self.stat_value_averted = on_dis_occ(self.stat_life * self.averted, self.horizon,
                                             self.disaster_rate, self.discount_rate)
        self.stat_averted = 1/self.disaster_rate * self.horizon * self.averted
