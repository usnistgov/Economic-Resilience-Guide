""" The externalities package for the list of externalities and the externality class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""
import math

class Externalities():
    """ Holds a list of all of the externalities
        and performs the externality-related calculations."""
    def __init__(self, discount_rate, horizon, parties):
        self.indiv = []
        self.one_sum_p = 0
        self.one_sum_n = 0
        self.r_sum_p = 0
        self.r_sum_n = 0
        self.total_p = self.one_sum_p + self.r_sum_p
        self.total_n = self.one_sum_n + self.r_sum_n

        self.parties = parties

        self.discount_rate = float(discount_rate)
        self.horizon = float(horizon)

    def new_ext(self, line):
        """ Makes a new externality and adds it to the list of externality types. """
        if line[0] == "positive":
            self.indiv[-1].pm = '+'
            self.indiv[-1].set_party(line[1])
        elif line[0] == "negative":
            self.indiv[-1].pm = '-'
            self.indiv[-1].set_party(line[1])
        else:
            opts = {}
            opts['title'] = line[0]
            opts['ext_type'] = line[1]
            opts['times'] = [line[2], line[3], line[4]]
            opts['amount'] = line[5]
            opts['desc'] = line[6]
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
            if ext.pm == "+":
                if ext.ext_type == "one-time":
                    self.one_sum_p += self.calc_one_time(ext.amount, ext.times[0])
                elif ext.ext_type == "recurring":
                    self.r_sum_p += self.calc_recur(ext.amount, ext.times[0], ext.times[1])
            elif ext.pm == "-":
                if ext.ext_type == "one-time":
                    self.one_sum_n += self.calc_one_time(ext.amount, ext.times[0])
                elif ext.ext_type == "recurring":
                    self.r_sum_n += self.calc_recur(ext.amount, ext.times[0], ext.times[1])

        self.total_p = self.one_sum_p + self.r_sum_p
        self.total_n = self.one_sum_n + self.r_sum_n

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


    def save(self, title, desc, amount, new_type, times, err_messages, pm, blank=False):
        """ Saves the fields if possible and returns applicable error messages if not."""
        field_dict = {}
        if blank:
            valid = False
        else:
            valid = True
        # == TITLE
        # Title cannot be left blank
        if title in {"", "<enter a title for this externality>"}:
            err_messages += "Title field has been left empty!\n\n"
            valid = False
        else:
            blank = False
        # Title cannot match other titles in same plan
        for plan in self.indiv:
            if title == plan.title:
                err_messages += title + " is already used as an externality title for this plan. "
                err_messages += "Please input a different title.\n\n"
                valid = False
        # No hyphen in title
        if "-" in title:
            err_messages += "Title cannot have a hyphen. Please change the title.\n\n"
            valid = False
        # Set title in dict
        field_dict['title'] = title
        # == COST
        # Cost must be a number
        try:
            float(amount)
        except ValueError:
            if amount not in {"", "<enter an amount for this externality>"}:
                blank = False
            err_messages += "Dollar value of the externality must be a number. "
            err_messages += "Please enter an amount.\n\n"
            valid = False
        if "-" in amount:
            err_messages += "Dollar value of the externality must be positive. "
            err_messages += "Please enter a positive amount.\n\n"
            valid = False
        field_dict['amount'] = amount
        # == TYPE
        # Type must be either one-time or recurring
        if new_type not in {"one-time", "recurring"}:
            err_messages += "Type cannot be left empty. \n\n"
            valid = False
        field_dict['ext_type'] = new_type
        # == TIMES
        # Start year must be less than end date
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
                blank = False
                valid = False
        except ValueError:
            pass
        field_dict['times'] = times
        # == POSITIVE/NEGATIVE
        # Must be defined as a positive or negative externality
        if (pm == '+') | (pm == '-'):
            field_dict['pm'] = pm
            blank = False
        else:
            err_messages += "Must choose if this is a positive or negative externalitiy. \n\n"
            valid = False
        # == DESCRIPTION
        # No comma in description
        #if ',' in desc:
        #    err_messages += "Description cannot have a comma. Please change the description.\n\n"
        #    valid = False
        # Set blank description to N/A or non-blank description to dict
        if desc in {"", "<enter a description for this externality>\n"}:
            field_dict['desc'] = 'N/A'
        else:
            field_dict['desc'] = desc
        if valid:
            self.indiv.append(Externality(**field_dict))
            return [valid, blank, "Externality has been successfully added!"]
        else:
            return [valid, blank, err_messages]

class Externality():
    """ Holds all of the information about externalities. """
    def __init__(self, title="none", amount=0, ext_type='none', times=[0, 0, 0], pm='none',
                 new_party='none', parties=['none'], desc="N/A"):
        self.title = title
        self.amount = float(amount)
        self.ext_type = ext_type
        self.times = []
        for item in times:
            self.times.append(float(item))
        self.pm = pm
        self.desc = ""
        for bit in desc:
            self.desc += bit
        self.parties = parties
        self.third_party = self.set_party(new_party)

    def set_party(self, new_party):
        if (new_party == 'none') | (new_party == ''):
            self.third_party = 'none'
        elif new_party in self.parties:
            self.third_party = new_party
        else:
            self.parties.append(new_party)
            self.third_party = new_party
        return self.third_party
