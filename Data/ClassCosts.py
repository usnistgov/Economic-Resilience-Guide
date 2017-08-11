""" The costs package for the list of costs and the cost class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv
from Data.distributions import calc_recur, calc_one_time

class Costs():
    """ Holds a list of all of the costs and performs the cost-related calculations."""
    def __init__(self, discount_rate, horizon):
        # === The list of each individual cost
        self.indiv = []

        # === The sums used for the final analysis
        self.d_sum = 0
        self.i_sum = 0
        self.omr_1_sum = 0
        self.omr_r_sum = 0

        self.total = 0

        # === Disount rate and horizon needed for calc_one_time and calc_recurr
        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

        # Uncertainties results ranges
        self.direct_range = [0, 0]
        self.indirect_range = [0, 0]
        self.omr_one_range = [0, 0]
        self.omr_r_range = [0, 0]

    def new_cost(self, line):
        """ From the file read-in Makes a new cost
            and adds it to the list of cost types. """
        # === If we are adding uncertainty
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
                    self.omr_1_sum += calc_one_time(self.discount_rate, cost.amount, cost.times[0])
                elif cost.omr_type == "recurring":
                    self.omr_r_sum += calc_recur(self.discount_rate, self.horizon,
                                                 cost.amount, cost.times[0], cost.times[1])
        self.total = self.d_sum + self.i_sum + self.omr_1_sum + self.omr_r_sum



    def save(self, title, cost_type, omr_type, amount, omr_times, desc, err_messages, blank=False):
        """ Saves the fields if possible and returns applicable error messages if not.
            If no plan is chosen, blank must be set to True."""
        field_dict = {}

        # ===== Checking the title field
        if title == "" or title == "<enter a title for this cost>":
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
                    err_messages += title + " is already used as an cost title for this plan. "
                    err_messages += "Please input a different title.\n\n"
                    valid = False

        # ==== Checking the amount field
        try:
            amount = amount.replace(',', '')#.replace(' ', '')
            if float(amount) < 0:
                err_messages += "Dollar value must be a positive amount. "
                err_messages += "Perhaps this is a non-disaster related benefit?\n"
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
            blank = False
            field_dict['amount'] = float(amount)
        except ValueError:
            err_messages += "Amount must be a number.\n\n"
            valid = False

        # ===== Checking the description field
        if desc in {"", "<enter a description for this benefit>\n"}:
            desc = ["N/A"]
        else:
            desc = desc.replace('\n', '')
            print('here?')
            blank = False
        field_dict['desc'] = [desc]

        # ===== Checking cost type
        if cost_type not in {"direct", "indirect", "omr"}:
            err_messages += "A 'Cost Type' has not been selected!\n\n"
            valid = False
        else:
            blank = False
            field_dict['cost_type'] = cost_type

        # ===== Checking OMR fields
        if cost_type == "omr":
            try:
                if float(omr_times[0]) < 0:
                    err_messages += "Starting year must be a positive number. "
                    err_messages += "Please enter a positive amount.\n\n"
                    valid = False
            except ValueError:
                err_messages += "Starting year must be number. Please enter an amount.\n\n"
                valid = False

            if omr_type == "recurring":
                try:
                    if float(omr_times[1]) <= 0:
                        err_messages += "Recurring rate must be a positive number. "
                        err_messages += "Please enter a positive amount.\n\n"
                        valid = False
                except ValueError:
                    err_messages += "Recurring rate must be a number. Please enter an amount.\n\n"
                    valid = False
            field_dict['omr_type'] = omr_type
        field_dict['omr_times'] = omr_times

        # ===== Adding the cost if valid and returning error messages if not.
        if not blank and valid:
            self.indiv.append(Cost(**field_dict))
            err_messages = "Cost has been successfully added!"
        return [valid, blank, err_messages]

    def one_iter(self, old_cost_list):
        """ Creates one Cost instance with all costs within set uncertainty range."""
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
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
                 omr_times=[0, 0, 0], desc="N/A"):
        assert cost_type in self.types
        assert omr_type in self.omr_types
        self.title = title
        self.cost_type = cost_type
        self.omr_type = omr_type
        self.amount = float(amount)
        self.times = omr_times
        self.set_desc(desc)
        if self.omr_type != "none":
            for num in self.times:
                try:
                    num = float(num)
                except ValueError:
                    num = 0.
        else:
            self.times = [0, 0, 0]

        self.range = ['<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>',
                      '<insert uncertainty>']
        self.dist = "none"

    def add_uncertainty(self, new_range, distribution):
        """ Adds uncertainty to a specific costefit."""

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
