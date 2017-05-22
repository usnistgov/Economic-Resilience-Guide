""" The simulation package for the list of plans and the plans class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-05
"""

import csv

from Data.ClassBenefits import Benefits, Benefit
from Data.ClassCosts import Costs
from Data.ClassExternalities import Externalities
from Data.ClassFatalities import Fatalities
from Data.ClassNonDBens import NonDBens

from NewIRR import irr_for_all

import math

class Simulation():
    """ Holds all of the plans and does all of the larger calculations. """
    def __init__(self):
        self.title = ""
        self.plan_list = []
        self.num_plans = 0
        self.horizon = 0
        self.discount_rate = 0.03
        self.risk_pref = "neutral"
        self.stat_life = 7500000

    def file_read(self, file_name):
        """ Reads in the save file to fill the simulation with all plans. """
        file_data = open(file_name, 'r')
        data = csv.reader(file_data)
        for line in data:
            if line[0] == 'Title':
                self.title = line[1]
                self.horizon = line[4]
            elif line[0] == 'Discount Rate':
                self.discount_rate = line[1]
                self.risk_pref = line[4]
                self.stat_life = line[7]
            elif 'Plan' in line[0]:
                build_list = [list(line)]
                next_plan = Plan(line[0][-1], line[1], list(line[2:5]), list(line[5:8]),
                                 self.discount_rate, self.horizon, self.stat_life)
            elif line[0] == "":
                build_list.append(list(line))
            elif line[0] == 'END PLAN':
                next_plan.new_plan(build_list)
                self.plan_list.append(next_plan)
                build_list = []
            elif line[0] == 'END FILE':
                self.num_plans = len(self.plan_list)

                return True
            else:
                pass

    def get_disaster_rate(self):
        """ Returns the disaster rate for the first plan
        since at the moment all plans will be the same."""
        return [self.plan_list[0].recurrence,
                self.plan_list[0].recurr_uncert,
                self.plan_list[0].recurr_dist]

    def get_disaster_magnitude(self):
        """ Returns the disaster magnitude for the first plan
        since at the moment all plans will be the same."""
        return [self.plan_list[0].magnitude,
                self.plan_list[0].mag_uncert,
                self.plan_list[0].mag_dist]

    def summer(self):
        """ Sums up all of the pieces."""
        for plan in self.plan_list:
            plan.sum_it(self.horizon)

class Plan():
    """ Has all of the aspects of the plan. """
    tol = 1E-7
    def __init__(self, plan_id, plan_name, disaster_recurrence, disaster_magnitude,
                 discount_rate, horizon, stat_life):
        # Basic Information
        self.id_assign = int(plan_id)
        self.name = plan_name
        self.recurrence = float(disaster_recurrence[0])
        self.recurr_uncert = float(disaster_recurrence[1])
        self.recurr_dist = disaster_recurrence[2]
        self.magnitude = float(disaster_magnitude[0])
        self.mag_uncert = float(disaster_magnitude[1])
        self.mag_dist = disaster_magnitude[2]
        self.horizon = horizon

        # Specific pieces
        self.costs = Costs(discount_rate, horizon)
        self.exts = Externalities()
        self.bens = Benefits(self.recurrence, discount_rate, horizon)
        self.fat = Fatalities(self.recurrence, discount_rate, stat_life, horizon)
        self.nond_bens = NonDBens(discount_rate, horizon)

        self.total_bens = 0
        self.total_costs = 0
        self.net = 0

        self.annual_cash_flows = [0 for x in range(int(horizon) + 1)]
        self.annual_non_disaster_cash_flows = [0 for x in range(int(horizon) + 1)]

    def new_plan(self, save_list):
        """ Builds a plan from a list of pieces from the save file."""
        for line in save_list:
            if line[1] == "Costs":
                self.costs.new_cost(list(line[2:]))
            elif line[1] == "Benefits":
                self.bens.new_ben(list(line[2:]))
            elif line[1] == "Externalities":
                self.exts.new_ext(list(line[2:]))
            elif line[1] == "Fatalities":
                self.fat.update(line[2], line[3:])
            elif line[1] == "Non-Disaster Benefits":
                self.nond_bens.new_ben(list(line[2:]))

    def sum_it(self, horizon):
        """ Sums up all of the individual pieces. """
        self.total_bens = 0
        self.total_costs = 0
        self.net = 0
        horizon = int(horizon)
        # Note: Fatilites does all summing every time it is updated.
        self.costs.make_sum()
        self.bens.make_sum()
        # TODO: Figure out how externalities play into this adventure,
        #       becuase they are MIA in calculations
        #self.exts.make_sum()
        self.nond_bens.make_sum()

        rec_list = []
        ot_list = []
        for ben in self.nond_bens.indiv:
            if ben.ben_type == "recurring":
                rec_list.append(ben)
            else:
                ot_list.append(ben)
        for cost in self.costs.indiv:
            if cost.omr_type == "recurring":
                rec_list.append(cost)
            else:
                rec_list.append(cost)
        time_series = []
        for item in rec_list:
            start = float(item.times[0])
            rate = float(item.times[1])
            if isinstance(item, Benefit):
                amount = float(item.amount)
            else:
                amount = -float(item.amount)
            i = 0
            while start + rate * i <= horizon + self.tol:
                time_series.append([start + rate * i, amount])
                i += 1
                if rate <= self.tol:
                    break
        for item in ot_list:
            if isinstance(item, Benefit):
                amount = float(item.amount)
            else:
                amount = -float(item.amount)
            time_series.append([float(item.times[0]), amount])

        time_series.sort(key=lambda x: x[0])
        prev = -1
        for i in range(len(time_series)):
            if abs(time_series[i][0]-prev) <= self.tol:
                time_series[i][0] = -1
                time_series[i-1][1] += float(time_series[i][1])
            else:
                prev = time_series[i][0]

        self.annual_cash_flows = []
        for item in time_series:
            if item[0] != -1:
                self.annual_cash_flows.append(item)

        self.total_bens = self.bens.total + self.fat.stat_value_averted + self.nond_bens.total
        self.total_costs = self.costs.total
        self.net = self.total_bens - self.total_costs

    def sir(self):
        """Equation for the Savings-to-Investment Ratio"""
        up_front = self.costs.d_sum + self.costs.i_sum

        if up_front == 0:
            return 0

        return self.net / up_front

    def irr(self):
        """Equation for the Internal Rate of Return"""
        # === Calls the function so that self.up_front is calculated
        #self.sir(plan_num)

        #annual_cost = (self.cost.total - self.up_front) / float(self.horizon)
        #annual_savings = self.ben.total / float(self.horizon)

        #irr_list = [annual_savings - annual_cost] * (int(self.horizon) + 1)
        #irr_list[0] = -(self.up_front)

        cash_flows = self.annual_non_disaster_cash_flows
        ben_list = [self.bens.d_sum, self.bens.i_sum,
                    self.bens.r_sum]

        try:
            the_irr = irr_for_all(cash_flows, self.horizon, self.recurrence, ben_list,
                                  self.fat.stat_life, self.fat.averted)
        except ValueError:
            print('ValueError')
            return 'No Valid IRR'
        except OverflowError:
            print('OverflowError')
            return 'No Valid IRR'
        if the_irr == 0.5:
            return "---"

        return the_irr * 100


    def roi(self):
        """Equation for the Return on Investment"""
        if self.bens.total == 0:
            return 0
        elif self.costs.total == 0:
            return 0
        annual_savings = self.bens.total / float(self.horizon)
        simple_payback = self.costs.total / annual_savings
        return (1 / simple_payback) * 100

    def non_d_roi(self):
        """Equation for the Return on Investment (without any chance of disaster occurring)"""
        non_d_ben_total = self.nond_bens.r_sum + self.nond_bens.one_sum

        if non_d_ben_total == 0:
            return 0
        elif self.costs.total == 0:
            return 0
        annual_savings = non_d_ben_total / float(self.horizon)
        simple_payback = self.costs.total / annual_savings
        return (1 / simple_payback) * 100
