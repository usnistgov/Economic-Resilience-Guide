""" The externalities package for the list of externalities and the externality class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

class Externalities():
    """ Holds a list of all of the externalities
        and performs the externality-related calculations."""
    def __init__(self):
        self.indiv = []
        self.total = 0

    def new_ext(self, line):
        """ Makes a new externality and adds it to the list of externality types. """
        opts = {}
        opts['title'] = line[0]
        opts['ben_type'] = line[1]
        opts['amount'] = line[2]
        opts['desc'] = line[3:]
        this_ben = Externality(**opts)
        self.indiv.append(this_ben)

    def copy_ext(self, ext):
        """ Adds a new, identical externality to the list."""
        ext_dict = {'title': ext.title,
                    'amount':ext.amount,
                    'desc':ext.desc}
        self.indiv.append(Externality(**ext_dict))


class Externality():
    """ Holds all of the information about externalities. """
    def __init__(self, title="none", amount=0, desc="N/A"):
        self.title = title
        self.amount = amount
        self.desc = desc
