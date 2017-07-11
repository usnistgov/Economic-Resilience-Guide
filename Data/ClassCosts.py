""" The costs package for the list of costs and the cost class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-07
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

    def save(self, title, cost_type, omr_type, amount, omr_times, desc, err_messages, blank=False):
        """ Saves the fields if possible and returns applicable error messages if not."""
        field_dict = {}
        if blank:
            valid = False
        else:
            valid = True
        # ===== Mandatory fields cannot be left blank or left alone
        if title == "" or title == "<enter a title for this cost>":
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        else:
            blank = False

        if cost_type != "direct" and cost_type != "indirect" and cost_type != "omr":
            err_messages += "A 'Cost Type' has not been selected!\n\n"
            valid = False
        else:
            field_dict['cost_type'] = cost_type

        # ===== Cost cannot have a duplicate title
        for plan in self.indiv:
            if title == plan.title:
                err_messages += title + " is already used as an cost title for this plan. "
                err_messages += "Please input a different title.\n\n"
                valid = False
        # No comma in title
        if "," in title:
            err_messages += "Title cannot have a comma. Please change the title.\n\n"
            valid = False
        # Set title in dict
        field_dict['title'] = title

        # ===== Cost must be a positive number
        try:
            float(amount)
            field_dict['amount'] = amount
        except ValueError:
            if amount not in {"", "<enter an amount for this cost>"}:
                blank = False
            err_messages += "Dollar value of the cost must be a number. Please enter an amount.\n\n"
            valid = False
        if "-" in amount:
            err_messages += "Cost must be a positive number."
            err_messages += "Perhaps you should enter that as a benefit.\n"
            err_messages += "Please enter a positive amount.\n\n"
            blank = False
            valid = False

        # ===== Omr Fields must be filled if OMR is selected
        if cost_type == "omr":
            try:
                float(omr_times[0])
            except ValueError:
                err_messages += "Starting year must be number. Please enter an amount.\n\n"
                valid = False
            if "-" in omr_times[0]:
                err_messages += "Starting year must be a positive number. "
                err_messages += "Please enter a positive amount.\n\n"
                blank = False
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
        # Set blank description to N/A or non-blank description to dict
        if desc in {"", "<enter a description for this externality>\n"}:
            field_dict['desc'] = 'N/A'
        else:
            desc = desc.replace('\n', '')
            field_dict['desc'] = [desc]
        if valid:
            self.indiv.append(Cost(**field_dict))
            return [valid, blank, "Cost has been successfully added!"]
        else:
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
        self.desc = ""
        for i in range(len(desc)):
            if i != 0:
                self.desc += ','
            self.desc += desc[i]
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

        self.range = new_range
        self.dist = distribution
