""" The externalities package for the list of externalities and the externality class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import numpy as np

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv
from Data.distributions import calc_one_time, calc_recur

class Externalities():
    """ Holds a list of all of the externalities
        and performs the externality-related calculations."""
    def __init__(self, discount_rate, horizon, parties):
        # === The list of each individual externality
        self.indiv = []

        # === The sums used for the final analysis
        self.one_sum_p = 0
        self.one_sum_n = 0
        self.r_sum_p = 0
        self.r_sum_n = 0
        self.total_p = self.one_sum_p + self.r_sum_p
        self.total_n = self.one_sum_n + self.r_sum_n

        # === The third parties affected for assignment
        self.parties = parties

        # === Discount rate, horizon for calc_one_time and calc_recur
        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

        # === Uncertainties ranges
        self.one_p_range = [0, 0]
        self.one_n_range = [0, 0]
        self.r_p_range = [0, 0]
        self.r_n_range = [0, 0]


    def new_ext(self, line):
        """ From the file read-in, makes a new externality
            and adds it to the list of externality types. """
        # === If we are adding uncertainty
        if line[0] == 'Uncertainty':
            self.indiv[-1].dist = line[1]
            self.indiv[-1].range = list(line[2:8])
        # === For the thrid-party, positive/negative line
        elif line[0] == "positive":
            self.indiv[-1].plus_minus = '+'
            self.indiv[-1].set_party(line[1])
        elif line[0] == "negative":
            self.indiv[-1].plus_minus = '-'
            self.indiv[-1].set_party(line[1])
        else:
            opts = {}
            opts['title'] = line[0]
            opts['ext_type'] = line[1]
            opts['times'] = [line[2], line[3], line[4]]
            opts['amount'] = line[5]
            opts['desc'] = line[6:]
            opts['parties'] = self.parties
            this_ext = Externality(**opts)
            self.indiv.append(this_ext)

    def make_sum(self):
        """ Calculates the cost sums from externalities."""
        self.one_sum_p = 0
        self.r_sum_p = 0
        self.one_sum_n = 0
        self.r_sum_n = 0

        for ext in self.indiv:
            if ext.plus_minus == "+":
                if ext.ext_type == "one-time":
                    self.one_sum_p += calc_one_time(self.discount_rate, ext.amount, ext.times[0])
                elif ext.ext_type == "recurring":
                    self.r_sum_p += calc_recur(self.discount_rate, self.horizon,
                                               ext.amount, ext.times[0], ext.times[1])
            elif ext.plus_minus == "-":
                if ext.ext_type == "one-time":
                    self.one_sum_n += calc_one_time(self.discount_rate, ext.amount, ext.times[0])
                elif ext.ext_type == "recurring":
                    self.r_sum_n += calc_recur(self.discount_rate, self.horizon,
                                               ext.amount, ext.times[0], ext.times[1])

        self.total_p = self.one_sum_p + self.r_sum_p
        self.total_n = self.one_sum_n + self.r_sum_n

    def save(self, title, desc, amount, new_type, times, err_messages, plus_minus, party,
             blank=False):
        """ Saves the fields if possible and returns applicable error messages if not."""
        field_dict = {}

        # ===== Checking the title field
        if title in {"", "<enter a title for this externality>"}:
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
                    err_messages += title + " is already used as an externality title for this "
                    err_messages += "plan. Please input a different title.\n\n"
                    valid = False

        # ===== Checking the amount field
        try:
            amount = amount.replace(',', '')#.replace(' ', '')
            if float(amount) < 0:
                err_messages += "Dollar value of the externality must be positive. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
            blank = False
            field_dict['amount'] = float(amount)
        except ValueError:
            valid = False
            if amount not in {"", "<enter an amount for this externality>"}:
                blank = False
            err_messages += "Dollar value of the externality must be a number. "
            err_messages += "Please enter an amount.\n\n"

        # ===== Checking the description field
        if desc in {"", "<enter a description for this externality>\n"}:
            field_dict['desc'] = ['N/A']
        else:
            desc = desc.replace('\n', '')
            blank = False
        field_dict['desc'] = [desc]

        # ===== Checking the externality type
        if new_type not in {"one-time", "recurring"}:
            err_messages += "Type cannot be left empty. \n\n"
            valid = False
        else:
            field_dict['ext_type'] = new_type
            blank = False

        # ===== Checking year fields
        if times[2] != 0:
            if times[0] >= times[2]:
                err_messages += "End year cannot be before starting year."
        if new_type == "one-time":
            times[1] = 0
        # All years must be numbers
        for year in times:
            try:
                year = float(year)
            except ValueError:
                err_messages += "All years must be numbers. "
                err_messages += "Please enter an amount.\n\n"
                valid = False
                break
        # Recursion cannot be at a zero/negative rate
        try:
            if (float(times[1]) <= 0) & (new_type == "recurring"):
                err_messages += "Cannot recur every " + str(times[1]) +" years. "
                err_messages += "Please enter a positive amount.\n\n"
                valid = False
        except ValueError:
            field_dict['times'] = times

        # ===== Checking if a positive or negative externality
        if (plus_minus == '+') | (plus_minus == '-'):
            field_dict['plus_minus'] = plus_minus
            blank = False
        else:
            err_messages += "Must choose if this is a positive or negative externality. \n\n"
            valid = False

        # ===== Checking Party-Affected
        if party == "":
            err_messages += "Must choose a party affected.\n\n"
            valid = False
        else:
            field_dict['new_party'] = party
            blank = False

        # ===== Adding the cost if valid and returning error messages if not.
        if not blank and valid:
            self.indiv.append(Externality(**field_dict))
            err_messages = "Externality has been successfully added!"
        return [valid, blank, err_messages]

    def one_iter(self, old_ext_list):
        """ Creates one instance of Externalities with all exts within uncertainty ranges."""
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        delta_ext = Externalities(self.discount_rate, self.horizon, self.parties)
        for ext in old_ext_list:
            ext_dict = {'title': ext.title,
                        'ext_type': ext.ext_type,
                        'times': ext.times,
                        'plus_minus': ext.plus_minus,
                        'new_party': ext.third_party,
                        'parties': ext.parties,
                        'desc': ext.desc}
            ext_dict['amount'] = dist_dict[ext.dist](np.random.uniform(), ext.amount, ext.range)
            delta_ext.indiv.append(Externality(**ext_dict))

        return delta_ext

class Externality():
    """ Holds all of the information about externalities. """
    def __init__(self, title="none", amount=0, ext_type='none', times=None, plus_minus='none',
                 new_party='none', parties=['none'], desc="N/A"):
        self.title = title
        self.amount = float(amount)
        self.ext_type = ext_type
        self.times = []
        if times is None:
            times = [0, 0, 0]
        for item in times:
            self.times.append(float(item))
        self.plus_minus = plus_minus
        self.set_desc(desc)
        self.parties = parties
        self.third_party = self.set_party(new_party)
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

    def set_party(self, new_party):
        """ Sets the third party and appends to the list of parties if
            this party is not already in the list."""
        if (new_party == 'none') | (new_party == ''):
            self.third_party = 'none'
        elif new_party in self.parties:
            self.third_party = new_party
        else:
            self.parties.append(new_party)
            self.third_party = new_party
        return self.third_party

    def set_desc(self, new_desc):
        """ Sets the description. """
        self.desc = ""
        for item in new_desc:
            if self.desc != "" and not self.desc.endswith(","):
                self.desc += ','
            self.desc += item
        if self.desc == 'N/A,':
            self.desc = 'N/A'
