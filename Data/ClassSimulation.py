""" The simulation package for the list of plans and the plans class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
    2017-07
"""

import csv

import math
import numpy as np

from tkinter import filedialog

from Data.ClassBenefits import Benefits
from Data.ClassCosts import Costs
from Data.ClassExternalities import Externalities
from Data.ClassFatalities import Fatalities
from Data.ClassNonDBens import NonDBens
from Data.ClassNonDBens import Benefit as NonDBenefit

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv


from NewIRR import irr_for_all

class Simulation():
    """ Holds all of the plans and does all of the larger calculations. """
    parties = ['developer', 'title holder(s)', 'lender(s)', 'tenants', 'users', 'community']
    def __init__(self):
        self.title = ""
        self.plan_list = []
        self.num_plans = 0
        self.horizon = 0
        self.discount_rate = 0.03
        self.risk_pref = "neutral"
        self.stat_life = 7500000
        self.seed = 000
        self.confidence = 95 #%
        self.tolerance = 0.1 #%

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
                next_plan = Plan(line[0][-1], line[1], [line[2], list(line[3:9])],
                                 [line[9], list(line[10:17])],
                                 self.discount_rate, self.horizon, self.stat_life, self.parties)
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

    def file_save(self):
        """ Saves the data in the save file."""
        my_formats = [('Comma Separated Value', '*.csv'),]
        file_name = filedialog.asksaveasfilename(filetypes=my_formats, title="Save the file as...")
        if file_name[-4:] != '.csv':
            file_name = file_name + '.csv'
        new_file = open(file_name, 'w')
        new_file.write('Title,' + str(self.title) + ',,Horizon,' + str(int(self.horizon)) + '\n')
        new_file.write('Discount Rate,' + str(self.discount_rate))
        new_file.write(',,Risk Prev,' + self.risk_pref)
        new_file.write(',,Value of Stat Life,' + str(self.stat_life) + '\n')
        new_file.write('BEGIN PLANS\n')
        for plan in self.plan_list:
            plan.save_plan(new_file)
            new_file.write('END PLAN\n')
        new_file.write('END FILE')
        new_file.close()

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

    def monte(self, new_seed, confidence, tol, low_iters=1000, high_iters=102400):
        """ Runs the monte-carlo everything."""
        self.seed = new_seed
        self.confidence = confidence
        self.tolerance = tol
        tol_percent = tol/100
        num_iters = low_iters
        # Because we are doing a while, it is cutting off below the high_iters mark,
        high_iters = high_iters + 0.5
        ### NOTE: It's mad about this call, claiming it will pull an error. It doesn't
        np.random.seed(seed=new_seed)

        for plan in self.plan_list:
            ben_direct_totals = []
            ben_indirect_totals = []
            res_rec_totals = []
            fat_num_totals = []
            fat_value_totals = []
            cost_direct_totals = []
            cost_indirect_totals = []
            cost_omr_1_totals = []
            cost_omr_r_totals = []
            nond_1_totals = []
            nond_r_totals = []
            ext_p_one_totals = []
            ext_p_r_totals = []
            ext_n_one_totals = []
            ext_n_r_totals = []

            ben_totals = []
            cost_totals = []
            net_totals = []
            net_ext_totals = []
            irr_totals = []
            sir_totals = []
            roi_totals = []
            nond_roi_totals = []

            #similar_list = []
            cost_ben_net = [False, False, False, False]
            old_iters = 0
            num_iters = low_iters

            old_ben = plan.total_bens#list(plan.ben_range)
            old_cost = plan.total_costs#list(plan.cost_range)
            old_net = plan.net#list(plan.net_range)
            old_ext_net = plan.net_w_ext#list(plan.net_ext_range)

            while (not all(cost_ben_net)) and num_iters < high_iters:
                for i in range(old_iters, num_iters):
                    #similar_list.append(self.one_iter(plan))
                    #similar_list[i].sum_it(self.horizon)
                    new_sim = self.one_iter(plan)
                    new_sim.sum_it(self.horizon)
                    ben_direct_totals.append(new_sim.bens.d_sum)
                    ben_indirect_totals.append(new_sim.bens.i_sum)
                    fat_num_totals.append(new_sim.fat.stat_averted)
                    fat_value_totals.append(new_sim.fat.stat_value_averted)
                    cost_direct_totals.append(new_sim.costs.d_sum)
                    cost_indirect_totals.append(new_sim.costs.i_sum)
                    cost_omr_1_totals.append(new_sim.costs.omr_1_sum)
                    cost_omr_r_totals.append(new_sim.costs.omr_r_sum)
                    res_rec_totals.append(new_sim.bens.r_sum)
                    nond_1_totals.append(new_sim.nond_bens.one_sum)
                    nond_r_totals.append(new_sim.nond_bens.r_sum)
                    ext_p_one_totals.append(new_sim.exts.one_sum_p)
                    ext_p_r_totals.append(new_sim.exts.r_sum_p)
                    ext_n_one_totals.append(new_sim.exts.one_sum_n)
                    ext_n_r_totals.append(new_sim.exts.r_sum_n)
                    ben_totals.append(new_sim.total_bens)
                    cost_totals.append(new_sim.total_costs)
                    net_totals.append(new_sim.net)
                    net_ext_totals.append(new_sim.net_w_ext)
                    if isinstance(new_sim.irr(), str):
                        irr_totals.append(-1)
                    else:
                        irr_totals.append(new_sim.irr())
                    sir_totals.append(new_sim.sir())
                    roi_totals.append(new_sim.roi())
                    nond_roi_totals.append(new_sim.non_d_roi())

                # Test costs
                tol = plan.total_costs * tol_percent + 0.001
                #if max(abs(plan.cost_range[0] - old_cost[0]), abs(plan.cost_range[1] - old_cost[1])) < tol:
                if abs(np.mean(cost_totals) - old_cost) < tol:
                    cost_ben_net[0] = True

                # Test bens
                #tol = plan.total_bens * tol_percent + 0.001
                #if max(abs(plan.ben_range[0] - old_ben[0]), abs(plan.ben_range[1] - old_ben[1])) < tol:
                if abs(np.mean(ben_totals) - old_ben) < tol:
                    cost_ben_net[1] = True
                # Test net
                #tol = plan.net * tol_percent + 0.001
                #if max(abs(plan.net_range[0] - old_net[0]), abs(plan.net_range[1] - old_net[1])) < tol:
                if abs(np.mean(net_totals) - old_net) < tol:
                    cost_ben_net[2] = True
                # Test net with externalities
                #tol = plan.net_w_ext * tol_percent + 0.001
                #if max(abs(plan.net_ext_range[0] - old_ext_net[0]), abs(plan.net_ext_range[1] - old_ext_net[1])) < tol:
                if abs(np.mean(net_ext_totals) - old_ext_net) < tol:
                    cost_ben_net[3] = True

                old_ben = np.mean(ben_totals)
                old_cost = np.mean(cost_totals)
                old_net = np.mean(net_totals)
                old_ext_net = np.mean(net_ext_totals)

                old_iters = num_iters
                num_iters = num_iters + low_iters#2 * num_iters

            num_iters = num_iters - low_iters

            first_num = math.floor(num_iters*(1-confidence/100)/2)
            last_num = math.ceil(num_iters - num_iters*(1-confidence/100)/2)

            ben_totals.sort()
            cost_totals.sort()
            net_totals.sort()
            net_ext_totals.sort()
            ben_direct_totals.sort()
            ben_indirect_totals.sort()
            fat_num_totals.sort()
            fat_value_totals.sort()
            cost_direct_totals.sort()
            cost_indirect_totals.sort()
            cost_omr_1_totals.sort()
            cost_omr_r_totals.sort()
            res_rec_totals.sort()
            nond_1_totals.sort()
            nond_r_totals.sort()
            ext_p_one_totals.sort()
            ext_p_r_totals.sort()
            ext_n_one_totals.sort()
            ext_n_r_totals.sort()
            irr_totals.sort()
            sir_totals.sort()
            roi_totals.sort()
            nond_roi_totals.sort()

            plan.ben_range = [ben_totals[first_num], ben_totals[last_num]]
            plan.cost_range = [cost_totals[first_num], cost_totals[last_num]]
            plan.net_range = [net_totals[first_num], net_totals[last_num]]
            plan.net_ext_range = [net_ext_totals[first_num], net_ext_totals[last_num]]
            plan.bens.direct_range = [ben_direct_totals[first_num], ben_direct_totals[last_num]]
            plan.bens.indirect_range = [ben_indirect_totals[first_num], ben_indirect_totals[last_num]]
            plan.bens.res_rec_range = [res_rec_totals[first_num], res_rec_totals[last_num]]
            plan.fat.num_range = [fat_num_totals[first_num], fat_num_totals[last_num]]
            plan.fat.value_range = [fat_value_totals[first_num], fat_value_totals[last_num]]
            plan.costs.direct_range = [cost_direct_totals[first_num], cost_direct_totals[last_num]]
            plan.costs.indirect_range = [cost_indirect_totals[first_num], cost_indirect_totals[last_num]]
            plan.costs.omr_one_range = [cost_omr_1_totals[first_num], cost_omr_1_totals[last_num]]
            plan.costs.omr_r_range = [cost_omr_r_totals[first_num], cost_omr_r_totals[last_num]]
            plan.nond_bens.one_range = [nond_1_totals[first_num], nond_1_totals[last_num]]
            plan.nond_bens.r_range = [nond_r_totals[first_num], nond_r_totals[last_num]]
            plan.exts.one_p_range = [ext_p_one_totals[first_num], ext_p_one_totals[last_num]]
            plan.exts.one_n_range = [ext_n_one_totals[first_num], ext_n_one_totals[last_num]]
            plan.exts.r_p_range = [ext_p_r_totals[first_num], ext_p_r_totals[last_num]]
            plan.exts.r_n_range = [ext_n_r_totals[first_num], ext_n_r_totals[last_num]]
            plan.irr_range = [irr_totals[first_num], irr_totals[last_num]]
            plan.sir_range = [sir_totals[first_num], sir_totals[last_num]]
            plan.roi_range = [roi_totals[first_num], roi_totals[last_num]]
            plan.nond_roi_range = [nond_roi_totals[first_num], nond_roi_totals[last_num]]

            if plan.irr_range[0] < 0:
                plan.irr_range[0] = '---'
            if plan.irr_range[1] < 0:
                plan.irr_range[1] = '---'
            plan.mc_iters = num_iters

    def one_iter(self, my_plan):
        """ Creates one plan that is within the uncertainty bounds of my_plan."""
        def to_pass(dist, some_range):
            """Returns the mid and range to pass the distributions given dist and some_range."""
            if dist == "none":
                mid = some_range[0]
                new_range = [0, 0, 0, 0, 0, 0]
            elif dist == "discrete":
                mid = max(some_range[0:2])
                new_range = list(some_range)
            elif dist == "gauss":
                mid = some_range[0]
                new_range = [some_range[1], 0, 0, 0, 0, 0]
            else:
                mid = some_range[0]
                new_range = [some_range[1], some_range[2], 0, 0, 0, 0]
            return [mid, new_range]
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}
        new_recurr = dist_dict[my_plan.recurr_dist](np.random.uniform(),
                                                    to_pass(my_plan.recurr_dist, my_plan.recurr_range)[0],
                                                    to_pass(my_plan.recurr_dist, my_plan.recurr_range)[1])
        new_mag = dist_dict[my_plan.mag_dist](np.random.uniform(),
                                              to_pass(my_plan.mag_dist, my_plan.mag_range)[0],
                                              to_pass(my_plan.mag_dist, my_plan.mag_range)[1])
        delta_plan = Plan(my_plan.id_assign, my_plan.name,
                          [my_plan.recurr_dist, [new_recurr, my_plan.recurr_range]],
                          [my_plan.mag_dist, [new_mag, my_plan.mag_range]], self.discount_rate,
                          self.horizon, self.stat_life, self.parties)
        delta_plan.bens = delta_plan.bens.one_iter(my_plan.bens.indiv)
        delta_plan.exts = delta_plan.exts.one_iter(my_plan.exts.indiv)
        delta_plan.costs = delta_plan.costs.one_iter(my_plan.costs.indiv)
        delta_plan.fat.update(my_plan.fat.averted, my_plan.fat.desc)
        delta_plan.nond_bens = delta_plan.nond_bens.one_iter(my_plan.nond_bens.indiv)
        return delta_plan

class Plan():
    """ Has all of the aspects of the plan. """
    tol = 1E-7
    def __init__(self, plan_id, plan_name, disaster_recurrence, disaster_magnitude,
                 discount_rate, horizon, stat_life, parties):
        # Basic Information
        self.id_assign = int(plan_id)
        self.name = plan_name
        self.recurr_dist = disaster_recurrence[0]
        self.recurr_range = disaster_recurrence[1]
        if self.recurr_dist == "none":
            self.recurr_uncert = [0]
            self.recurrence = disaster_recurrence[1][0]
        elif self.recurr_dist == "gauss":
            self.recurr_uncert = disaster_recurrence[1][1]
            self.recurrence = disaster_recurrence[1][0]
        elif self.recurr_dist == "discrete":
            self.recurr_uncert = list(disaster_recurrence)
            self.recurrence = max([disaster_recurrence[1][0], disaster_recurrence[1][2], disaster_recurrence[1][3]])
        else:
            self.recurr_uncert = list(disaster_recurrence[1])
            self.recurrence = disaster_recurrence[1][1]
        self.mag_dist = disaster_magnitude[0]
        self.mag_range = disaster_magnitude[1]
        if self.mag_dist == "none":
            self.mag_uncert = [0]
            self.magnitude = [disaster_magnitude[1][0]]
        elif self.mag_dist == "gauss":
            self.mag_uncert = disaster_magnitude[1][1]
            self.magnitude = [disaster_magnitude[1][0]]
        elif self.mag_dist == "discrete":
            self.mag_uncert = list(disaster_magnitude)
            self.magnitude = max([disaster_magnitude[1][0], disaster_magnitude[1][2], disaster_magnitude[1][3]])
        else:
            self.mag_uncert = list(disaster_magnitude[1])
            self.magnitude = disaster_magnitude[1][1]
        self.horizon = horizon

        # Specific pieces
        self.costs = Costs(discount_rate, horizon)
        self.exts = Externalities(discount_rate, horizon, parties)
        self.bens = Benefits(self.recurrence, discount_rate, horizon)
        self.fat = Fatalities(self.recurrence, discount_rate, stat_life, horizon)
        self.nond_bens = NonDBens(discount_rate, horizon)

        self.total_bens = 0
        self.total_costs = 0
        self.net = 0
        self.net_w_ext = self.net

        self.annual_cash_flows = [0 for x in range(int(horizon) + 1)]
        self.annual_non_disaster_cash_flows = [0 for x in range(int(horizon) + 1)]
        self.ben_range = [0, 0]
        self.cost_range = [0, 0]
        self.net_range = [0, 0]
        self.net_ext_range = [0, 0]


    def update(self, plan_id, plan_name, disaster_recurrence, disaster_magnitude,
               discount_rate, horizon, stat_life):
        # Basic Information
        self.id_assign = int(plan_id)
        self.name = plan_name
        self.recurr_dist = disaster_recurrence[0]
        self.recurr_range = disaster_recurrence[1]
        if self.recurr_dist == "none":
            self.recurr_uncert = [0]
            self.recurrence = disaster_recurrence[1][0]
        elif self.recurr_dist == "gauss":
            self.recurr_uncert = disaster_recurrence[1][1]
            self.recurrence = disaster_recurrence[1][0]
        elif self.recurr_dist == "discrete":
            self.recurr_uncert = list(disaster_recurrence[1])
            self.recurrence = max([disaster_recurrence[1][0], disaster_recurrence[1][2], disaster_recurrence[1][3]])
        else:
            self.recurr_uncert = list(disaster_recurrence[1])
            self.recurrence = disaster_recurrence[1][1]
        self.mag_dist = disaster_magnitude[0]
        self.mag_range = disaster_magnitude[1]
        if self.mag_dist == "none":
            self.mag_uncert = [0]
            self.magnitude = disaster_magnitude[1][0]
        elif self.mag_dist == "gauss":
            self.mag_uncert = disaster_magnitude[1][1]
            self.magnitude = disaster_magnitude[1][0]
        elif self.mag_dist == "discrete":
            self.mag_uncert = list(disaster_magnitude[1])
            self.magnitude = max([disaster_magnitude[1][0], disaster_magnitude[1][2], disaster_magnitude[1][3]])
        else:
            self.mag_uncert = list(disaster_magnitude[1])
            self.magnitude = disaster_magnitude[1][1]
        self.horizon = horizon

        # Specific pieces
        self.costs.discount_rate = discount_rate
        self.costs.horizon = horizon
        self.exts.discount_rate = discount_rate
        self.exts.horizon = horizon
        self.bens.dis_rate = self.recurrence
        self.bens.discount_rate = discount_rate
        self.bens.horizon = horizon
        self.fat.disaster_rate = self.recurrence
        self.fat.discount_rate = discount_rate
        self.fat.horizon = horizon
        self.fat.update(self.fat.averted, self.fat.desc)
        self.nond_bens.discount_rate = discount_rate
        self.nond_bens.horizon = horizon

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

    def save_plan(self, new_file):
        """ Saves a plan into the file."""
        new_file.write('Plan ' + str(self.id_assign) + ',' + self.name + ',')
        new_file.write(self.recurr_dist + ',')
        if self.recurr_dist in {'discrete', 'rect', 'tri'}:
            to_write = []
            for item in self.recurr_uncert:
                to_write.append(item)
            while len(to_write) < 6:
                to_write.append(0)
            for item in to_write:
                new_file.write(str(item) + ',')
        else:
            to_write = [self.recurrence]
            for item in self.recurr_uncert:
                to_write.append(item)
            while len(to_write) < 6:
                to_write.append(0)
            for item in to_write:
                new_file.write(str(item) + ',')
        new_file.write(self.mag_dist + ',')
        if self.mag_dist in {'discrete', 'rect', 'tri'}:
            to_write = []
            for item in self.mag_uncert:
                to_write.append(item)
            while len(to_write) < 6:
                to_write.append(0)
            for item in to_write:
                new_file.write(str(item) + ',')
        else:
            to_write = [self.magnitude]
            for item in self.mag_uncert:
                to_write.append(item)
            while len(to_write) < 6:
                to_write.append(0)
            for item in to_write:
                new_file.write(str(item) + ',')
        new_file.write('\n')
        for cost in self.costs.indiv:
            new_file.write(',Costs,' + cost.title + ',' + cost.cost_type + ',' + cost.omr_type + ',')
            for time in cost.times:
                new_file.write(str(time) + ',')
            new_file.write(str(cost.amount) + ',' + str(cost.desc) + '\n')
            new_file.write(',Costs,Uncertainty,' + cost.dist)
            for value in cost.range:
                if value != '<insert uncertainty>':
                    new_file.write(',' + str(value))
                else:
                    new_file.write(',0')
            new_file.write('\n')
        for ben in self.bens.indiv:
            new_file.write(',Benefits,' + ben.title + ',' + ben.ben_type + ',')
            new_file.write(str(ben.amount) + ',' + str(ben.desc) + '\n')
            new_file.write(',Benefits,Uncertainty,' + ben.dist)
            for value in ben.range:
                if value != '<insert uncertainty>':
                    new_file.write(',' + str(value))
                else:
                    new_file.write(',0')
            new_file.write('\n')
        for ext in self.exts.indiv:
            new_file.write(',Externalities,' + ext.title + ',' + ext.ext_type)
            for entry in ext.times:
                new_file.write(',' + str(entry))
            new_file.write(',' + str(ext.amount) + ',' + str(ext.desc) + '\n')
            new_file.write(',Externalities,')
            if ext.pm == '+':
                new_file.write('positive,')
            else:
                new_file.write('negative,')
            new_file.write(ext.third_party + '\n')
            new_file.write(',Externalities,Uncertainty,' + ext.dist)
            for value in ext.range:
                if value != '<insert uncertainty>':
                    new_file.write(',' + str(value))
                else:
                    new_file.write(',0')
            new_file.write('\n')
        for nond_ben in self.nond_bens.indiv:
            new_file.write(',Non-Disaster Benefits,' + nond_ben.title + ',' + nond_ben.ben_type + ',')
            for item in nond_ben.times:
                new_file.write(str(item) + ',')
            new_file.write(str(nond_ben.amount) + ',' + str(nond_ben.desc) + '\n')
            new_file.write(',Non-Disaster Benefits,Uncertainty,' + nond_ben.dist)
            for value in nond_ben.range:
                if value != '<insert uncertainty>':
                    new_file.write(',' + str(value))
                else:
                    new_file.write(',0')
            new_file.write('\n')
        new_file.write(',Fatalities,' + str(self.fat.averted) + ',' + str(self.fat.desc) + '\n')

    def sum_it(self, horizon):
        """ Sums up all of the individual pieces. """
        self.total_bens = 0
        self.total_costs = 0
        self.net = 0
        horizon = int(horizon)
        # Note: Fatilites does all summing every time it is updated.
        self.costs.make_sum()
        self.bens.make_sum()
        self.exts.make_sum()
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
                ot_list.append(cost)
        time_series = []
        for item in rec_list:
            start = float(item.times[0])
            rate = float(item.times[1])
            if isinstance(item, NonDBenefit):
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
            if isinstance(item, NonDBenefit):
                amount = float(item.amount)
            else:
                amount = -float(item.amount)
            time_series.append([float(item.times[0]), amount])

        time_series.sort(key=lambda x: x[0])
        prev = -1
        for i in range(len(time_series)):
            if abs(time_series[i][0]-prev) <= self.tol:
                time_series[i][1] += float(time_series[i-1][1])
                time_series[i-1][0] = -1
            else:
                prev = time_series[i][0]

        self.annual_cash_flows = []
        for item in time_series:
            if item[0] != -1:
                self.annual_cash_flows.append(item)

        self.total_bens = self.bens.total + self.fat.stat_value_averted + self.nond_bens.total
        self.total_costs = self.costs.total
        self.net = self.total_bens - self.total_costs
        self.net_w_ext = self.total_bens + self.exts.total_p - self.total_costs - self.exts.total_n

    def sir(self):
        """Equation for the Savings-to-Investment Ratio"""
        up_front = self.costs.d_sum + self.costs.i_sum

        if up_front == 0:
            return 0

        return self.net / up_front

    def irr(self):
        """Equation for the Internal Rate of Return"""
        cash_flows = self.annual_cash_flows
        ben_list = [self.bens.d_sum_no_discount, self.bens.i_sum_no_discount,
                    self.bens.r_sum_no_discount]

        try:
            the_irr = irr_for_all(cash_flows, self.horizon, self.recurrence, ben_list,
                                  self.fat.stat_life, self.fat.averted)
        except ValueError:
            #print('ValueError')
            return 'No Valid IRR'
        except OverflowError:
            #print('OverflowError')
            return 'No Valid IRR'
        if the_irr == 0.5:
            return "---"

        return the_irr * 100

    def roi(self):
        """Equation for the Return on Investment"""
        if self.total_bens == 0:
            return 0
        elif self.total_costs == 0:
            return 0
        annual_savings = self.total_bens / float(self.horizon)
        simple_payback = self.total_costs / annual_savings
        return (1 / simple_payback) * 100

    def non_d_roi(self):
        """Equation for the Return on Investment (without any chance of disaster occurring)"""
        non_d_ben_total = self.nond_bens.r_sum + self.nond_bens.one_sum

        if non_d_ben_total == 0:
            return 0
        elif self.total_costs == 0:
            return 0
        annual_savings = non_d_ben_total / float(self.horizon)
        simple_payback = self.total_costs / annual_savings
        return (1 / simple_payback) * 100
