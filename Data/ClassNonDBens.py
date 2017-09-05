""" The non-disaster related benefits package for the list of non-disaster related benefits
        and the non-disaster related benefits class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv
from Data.distributions import calc_one_time, calc_recur

class NonDBens():
    """ Holds a list of all of the benefits and performs the benefit-related calculations."""
    def __init__(self, discount_rate, horizon):
        # === The list of all non-disaster related benefits
        self.indiv = []

        # === The sums used for the final analysis
        self.one_sum = 0
        self.r_sum = 0

        self.total = 0

        # === Horizon and discount rate needed for calc_one_time and calc_recur
        self.horizon = float(horizon)
        self.discount_rate = float(discount_rate)

        # === Uncertainties ranges
        self.one_range = [0, 0]
        self.r_range = [0, 0]

    def new_ben(self, line):
        """ Makes a new benefit and adds it to the list of benefit types. """
        # === If we are adding uncertainty
        if line[0] == 'Uncertainty':
            self.indiv[-1].dist = line[1]
            self.indiv[-1].range = list(line[2:8])
        else:
            opts = {}
            opts['title'] = line[0]
            opts['ben_type'] = line[1]
            opts['times'] = [line[2], line[3], line[4]]
            opts['amount'] = line[5]
            opts['desc'] = line[6:]
            this_ben = Benefit(**opts)
            self.indiv.append(this_ben)

    def make_sum(self):
        """ Calculates the value of all Non-Disaster related benefits."""
        self.one_sum = 0
        self.r_sum = 0
        for ben in self.indiv:
            if ben.ben_type == "one-time":
                self.one_sum += calc_one_time(self.discount_rate, ben.amount, ben.times[0])
            elif ben.ben_type == "recurring":
                self.r_sum += calc_recur(self.discount_rate, self.horizon,
                                         ben.amount, ben.times[0], ben.times[1])
        self.total = self.one_sum + self.r_sum

    def one_iter(self, old_ben_list):
        """ Creates one instance of Benefits with all benefits within uncertainty ranges."""
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        delta_ben = NonDBens(self.discount_rate, self.horizon)
        for ben in old_ben_list:
            ben_dict = {'title': ben.title,
                        'ben_type': ben.ben_type,
                        'times': ben.times,
                        'desc': ben.desc}
            ben_dict['amount'] = dist_dict[ben.dist](np.random.uniform(), ben.amount, ben.range)
            delta_ben.indiv.append(Benefit(**ben_dict))

        return delta_ben

    def save(self, title, times, ben_type, amount, desc, err_messages, blank=False):
        """ Attempts to save a benefit."""
        field_dict = {}

        valid = True

        # ===== Checking the title field
        if title == "" or title == "<enter a title for this benefit>":
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        elif ',' in title:
            err_messages += "There cannot be a comma in the title.\n\n"
            valid = False
            blank = False
        else:
            field_dict['title'] = title
            blank = False

        # ==== Checking the description field
        if desc in {"", "<enter a description for this benefit>\n"}:
            desc = 'N/A'
        else:
            desc = desc.replace('\n', '')
            blank = False
            for plan in self.indiv:
                if title == plan.title:
                    err_messages += title + " is already used as a benefit title for this plan. "
                    err_messages += "Please input a different title.\n\n"
                    valid = False

        # ===== Checking the amount field
        try:
            amount = amount.replace(',', '')#.replace(' ', '')
            if float(amount) < 0:
                err_messages += "Dollar value must be a positive number. "
                err_messages += "Perhaps this is a cost?\n"
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
            blank = False
            field_dict['amount'] = float(amount)
        except ValueError:
            valid = False
            if amount not in {"", "<enter an amount for this benefit>"}:
                blank = False
            err_messages += "Dollar value of the benefit must be a number. "
            err_messages += "Please enter an amount.\n\n"

        # ===== Checking the description field
        if desc in {"", "<enter a description for this benefit>\n"}:
            desc = ["N/A"]
        else:
            desc = desc.replace('\n', '')
            blank = False
        field_dict['desc'] = [desc]

        # ===== Checking the benefit type
        if ben_type not in ["one-time", "recurring"]:
            err_messages += "A 'Benefit Type' has not been selected!\n\n"
            valid = False
        try:
            if float(times[0]) < 0:
                err_messages += "Starting year must be a positive number. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
            blank = False
        except ValueError:
            err_messages += "Starting year must be number. Please enter an amount.\n\n"
            valid = False

        if ben_type == "recurring":
            blank = False
            try:
                if float(times[1]) <= 0:
                    err_messages += "Recurring rate must be a positive number. "
                    err_messages += "Please enter a positive amount.\n\n"
                    valid = False
            except ValueError:
                err_messages += "Recurring rate must be a number. Please enter an amount.\n\n"
                valid = False
        field_dict['ben_type'] = ben_type
        field_dict['times'] = times

        if not blank and valid:
            self.indiv.append(Benefit(**field_dict))
            err_messages += "Benefit has been successfully added!"

        return [valid, blank, err_messages]


class Benefit():
    """ Holds all of the information about benefits. """
    types = ["one-time", "recurring"]
    def __init__(self, title="none", times=[0, 0, 0], ben_type="none", amount=0, desc="N/A"):
        assert ben_type in self.types
        self.title = title
        self.ben_type = ben_type
        self.times = times
        self.amount = float(amount)
        self.set_desc(desc)
        self.range = ['<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>']
        self.dist = "none"

    def add_uncertainty(self, new_range, distribution):
        """ Adds uncertainty to a specific benefit."""

        self.range = []
        for item in new_range:
            self.range.append(item.replace(',', ''))
        self.dist = distribution

    def set_desc(self, new_desc):
        """ Sets the description. """
        self.desc = ""
        for item in new_desc:
            if self.desc != "" and not self.desc.endswith(","):
                self.desc += ','
            self.desc += item
        if self.desc == 'N/A,':
            self.desc = 'N/A'
