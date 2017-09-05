""" The benefits package for the list of benefits and the benefit class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv
from Data.distributions import on_dis_occ

class Benefits():
    """ Holds a list of all of the benefits and performs the benefit-related calculations."""
    def __init__(self, disaster_rate, discount_rate, horizon):
        # === The list of each individual benefit
        self.indiv = []

        # === The sums used for the final analysis
        self.d_sum = 0
        self.d_sum_no_discount = 0
        self.i_sum = 0
        self.i_sum_no_discount = 0
        self.r_sum = 0
        self.r_sum_no_discount = 0

        self.total = 0

        # === Disaster rate, discount rate, and horizon needed for on_dis_occ
        self.dis_rate = float(disaster_rate)
        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

        # === Uncertainties ranges
        self.direct_range = [0, 0]
        self.indirect_range = [0, 0]
        self.res_rec_range = [0, 0]

    def new_ben(self, line):
        """ From the file read-in, makes a new benefit
            and adds it to the list of benefit types. """
        # === If we are adding uncertainty
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

        self.d_sum = on_dis_occ(self.d_sum, self.horizon, self.dis_rate, self.discount_rate)
        self.i_sum = on_dis_occ(self.i_sum, self.horizon, self.dis_rate, self.discount_rate)
        self.r_sum = on_dis_occ(self.r_sum, self.horizon, self.dis_rate, self.discount_rate)

        self.total = self.d_sum + self.i_sum + self.r_sum

    def one_iter(self, old_ben_list):
        """ Creates one Benefit class within the range of uncertainties."""
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        delta_ben = Benefits(self.dis_rate, self.discount_rate, self.horizon)
        for ben in old_ben_list:
            ben_dict = {'title': ben.title,
                        'ben_type': ben.ben_type,
                        'desc': ben.desc}
            ben_dict['amount'] = dist_dict[ben.dist](np.random.uniform(), ben.amount, ben.range)
            delta_ben.indiv.append(Benefit(**ben_dict))

        return delta_ben

    def save(self, title, ben_type, amount, desc, err_messages, blank=False):
        """ Saves the fields if possible and returns applicable error messages if not.
            If no plan is chosen, blank must be set to True."""
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
            for plan in self.indiv:
                if title == plan.title:
                    err_messages += title + " is already used as a benefit title for this plan. "
                    err_messages += "Please input a different title.\n\n"
                    valid = False

        # ===== Checking the amount field
        try:
            amount = amount.replace(',', '')#.replace(' ', '')
            if float(amount) < 0:
                err_messages += "Dollar value must be a positive number.\n"
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
            blank = False
            field_dict['amount'] = float(amount)
        except ValueError:
            valid = False
            if amount not in {"", "<enter dollar value for this benefit>"}:
                blank = False
            err_messages += "Dollar value of the benefit must be a number. "
            err_messages += "Please enter an amount.\n\n"

        # ===== Checking the description field
        if desc in {"", "<enter a description for this benefit>\n"}:
            desc = "N/A"
        else:
            desc = desc.replace('\n', '')
            blank = False
        field_dict['desc'] = [desc]

        # ===== Checking the benefit type
        if ben_type not in ["direct", "indirect", "res-rec"]:
            err_messages += "A 'Benefit Type' has not been selected!\n\n"
            valid = False
        else:
            field_dict['ben_type'] = ben_type
            blank = False

        # ===== Adding the benefit if valid and returning error messages if not.
        if not blank and valid:
            self.indiv.append(Benefit(**field_dict))
            err_messages = "Benefit has been successfully added!"
        return [valid, blank, err_messages]


class Benefit():
    """ Holds all of the information about benefits. """
    types = ["direct", "indirect", "res-rec"]
    def __init__(self, title="none", ben_type="none", amount=0, desc="N/A"):

        assert ben_type in self.types

        self.title = title
        self.ben_type = ben_type
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
