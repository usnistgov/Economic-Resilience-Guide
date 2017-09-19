""" The simulation package for the list of plans and the plans class.
    Author: Shannon Grubb
            shannon.grubb@nist.gov
"""

import csv

import math
import numpy as np

from tkinter import filedialog, messagebox

from Data.ClassBenefits import Benefits
from Data.ClassCosts import Costs, Cost
from Data.ClassExternalities import Externalities
from Data.ClassFatalities import Fatalities
from Data.ClassNonDBens import NonDBens
from Data.ClassNonDBens import Benefit as NonDBenefit

from Data.distributions import uniDistInv, triDistInv, gauss_dist_inv, none_dist, discrete_dist_inv


from NewIRR import irr_for_all

class Simulation():
    """ Holds all of the plans and does all of the larger calculations. """
    # These are the default third-parties
    parties = ['Developer', 'Title holder(s)', 'Lender(s)', 'Tenants', 'Users', 'Community']

    def __init__(self):
        # The pieces that are the same for every plan.
        self.title = ""
        self.plan_list = []
        self.num_plans = 0
        self.horizon = 0
        self.discount_rate = 0.03
        self.risk_pref = "none"
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
                next_plan.new_plan(build_list, self.stat_life)
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
        new_file.write(',,Risk Pref,' + self.risk_pref)
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
            ext_totals = []
            net_totals = []
            plan.net_ext_totals = []
            irr_totals = []
            irr_ext_totals = []
            bcr_totals = []
            bcr_ext_totals = []
            roi_totals = []
            roi_ext_totals = []
            nond_roi_totals = []
            nond_roi_ext_totals = []

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
                    ext_totals.append(new_sim.exts.total_p - new_sim.exts.total_n)
                    net_totals.append(new_sim.net)
                    plan.net_ext_totals.append(new_sim.net_w_ext)
                    if new_sim.irr() == "---":
                        irr_totals.append(-1)
                    elif new_sim.irr() == "No Valid IRR":
                        irr_totals.append(-2)
                    else:
                        irr_totals.append(new_sim.irr())
                    if new_sim.irr(w_ext=True) == "---":
                        irr_ext_totals.append(-1)
                    elif new_sim.irr(w_ext=True) == "No Valid IRR":
                        irr_ext_totals.append(-2)
                    else:
                        irr_ext_totals.append(new_sim.irr(w_ext=True))
                    sim_list = [[bcr_totals, new_sim.bcr()],
                                [bcr_ext_totals, new_sim.bcr(w_ext=True)],
                                [roi_totals, new_sim.roi()],
                                [roi_ext_totals, new_sim.roi(w_ext=True)],
                                [nond_roi_totals, new_sim.non_d_roi()],
                                [nond_roi_ext_totals, new_sim.non_d_roi(w_ext=True)]]
                    for item in sim_list:
                        if isinstance(item[1], str):
                            item[0].append(-1)
                        else:
                            item[0].append(item[1])
                    #if isinstance(new_sim.bcr(), str):
                    #    bcr_totals.append(-1)
                    #else:
                    #    bcr_totals.append(new_sim.bcr())
                    #if isinstance(new_sim.roi(), str):
                    #    roi_totals.append(-1)
                    #else:
                    #    roi_totals.append(new_sim.roi())
                    #if isinstance(new_sim.non_d_roi(), str):
                    #    nond_roi_totals.append(-1)
                    #else:
                    #    nond_roi_totals.append(new_sim.non_d_roi())

                # Test costs
                tol = plan.total_costs * tol_percent + 0.001
                if abs(np.mean(cost_totals) - old_cost) < tol:
                    cost_ben_net[0] = True

                # Test bens
                tol = plan.total_bens * tol_percent + 0.001
                if abs(np.mean(ben_totals) - old_ben) < tol:
                    cost_ben_net[1] = True
                # Test net
                tol = abs(plan.net * tol_percent + 0.001)
                if abs(np.mean(net_totals) - old_net) < tol:
                    cost_ben_net[2] = True
                # Test net with externalities
                tol = abs(plan.net_w_ext * tol_percent + 0.001)
                if abs(np.mean(plan.net_ext_totals) - old_ext_net) < tol:
                    cost_ben_net[3] = True

                old_ben = np.mean(ben_totals)
                old_cost = np.mean(cost_totals)
                old_net = np.mean(net_totals)
                old_ext_net = np.mean(plan.net_ext_totals)

                old_iters = num_iters
                num_iters = num_iters + low_iters#2 * num_iters
                if num_iters >= high_iters:
                    messagebox.showwarning("Maximum number of runs", "The maximum number of "
                                           "Monte-Carlo runs has been reached for "
                                           + plan.name + '. The results may not have converged.')

            num_iters = num_iters - low_iters

            first_num = math.floor(num_iters*(1-confidence/100)/2)
            last_num = math.ceil(num_iters - num_iters*(1-confidence/100)/2)

            ben_totals.sort()
            cost_totals.sort()
            net_totals.sort()
            plan.net_ext_totals.sort()
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
            ext_totals.sort()
            irr_totals.sort()
            irr_ext_totals.sort()
            bcr_totals.sort()
            bcr_ext_totals.sort()
            roi_totals.sort()
            roi_ext_totals.sort()
            nond_roi_totals.sort()
            nond_roi_ext_totals.sort()

            plan.ben_range = [ben_totals[first_num], ben_totals[last_num]]
            plan.cost_range = [cost_totals[first_num], cost_totals[last_num]]
            plan.net_range = [net_totals[first_num], net_totals[last_num]]
            plan.net_ext_range = [plan.net_ext_totals[first_num], plan.net_ext_totals[last_num]]
            plan.bens.direct_range = [ben_direct_totals[first_num], ben_direct_totals[last_num]]
            plan.bens.indirect_range = [ben_indirect_totals[first_num],
                                        ben_indirect_totals[last_num]]
            plan.bens.res_rec_range = [res_rec_totals[first_num], res_rec_totals[last_num]]
            plan.fat.num_range = [fat_num_totals[first_num], fat_num_totals[last_num]]
            plan.fat.value_range = [fat_value_totals[first_num], fat_value_totals[last_num]]
            plan.costs.direct_range = [cost_direct_totals[first_num], cost_direct_totals[last_num]]
            plan.costs.indirect_range = [cost_indirect_totals[first_num],
                                         cost_indirect_totals[last_num]]
            plan.costs.omr_one_range = [cost_omr_1_totals[first_num], cost_omr_1_totals[last_num]]
            plan.costs.omr_r_range = [cost_omr_r_totals[first_num], cost_omr_r_totals[last_num]]
            plan.nond_bens.one_range = [nond_1_totals[first_num], nond_1_totals[last_num]]
            plan.nond_bens.r_range = [nond_r_totals[first_num], nond_r_totals[last_num]]
            plan.exts.one_p_range = [ext_p_one_totals[first_num], ext_p_one_totals[last_num]]
            plan.exts.one_n_range = [ext_n_one_totals[first_num], ext_n_one_totals[last_num]]
            plan.exts.r_p_range = [ext_p_r_totals[first_num], ext_p_r_totals[last_num]]
            plan.exts.r_n_range = [ext_n_r_totals[first_num], ext_n_r_totals[last_num]]
            plan.ext_range = [ext_totals[first_num], ext_totals[last_num]]
            plan.irr_range = [irr_totals[first_num], irr_totals[last_num]]
            plan.irr_ext_range = [irr_ext_totals[first_num], irr_ext_totals[last_num]]
            plan.bcr_range = [bcr_totals[first_num], bcr_totals[last_num]]
            plan.bcr_ext_range = [bcr_ext_totals[first_num], bcr_ext_totals[last_num]]
            plan.roi_range = [roi_totals[first_num], roi_totals[last_num]]
            plan.roi_ext_range = [roi_ext_totals[first_num], roi_ext_totals[last_num]]
            plan.nond_roi_range = [nond_roi_totals[first_num], nond_roi_totals[last_num]]
            plan.nond_roi_ext_range = [nond_roi_ext_totals[first_num],
                                       nond_roi_ext_totals[last_num]]

            if plan.irr_range[0] == -1:
                plan.irr_range[0] = '---'
            elif plan.irr_range[0] == -2:
                plan.irr_range[0] = 'No Valid IRR'
            if plan.irr_range[1] == -1:
                plan.irr_range[1] = '---'
            elif plan.irr_range[1] == -2:
                plan.irr_range[1] = 'No Valid IRR'
            if plan.irr_ext_range[0] == -1:
                plan.irr_ext_range[0] = '---'
            elif plan.irr_ext_range[0] == -2:
                plan.irr_ext_range[0] = 'No Valid IRR'
            if plan.irr_ext_range[1] == -1:
                plan.irr_ext_range[1] = '---'
            elif plan.irr_ext_range[1] == -2:
                plan.irr_ext_range[1] = 'No Valid IRR'
            sim_list = [[plan.bcr_range, 'No Valid BCR'], [plan.roi_range, 'No Valid ROI'],
                        [plan.nond_roi_range, 'No Valid ROI'],
                        [plan.bcr_ext_range, 'No Valid BCR'],
                        [plan.roi_ext_range, 'No Valid ROI'],
                        [plan.nond_roi_ext_range, 'No Valid ROI']]
            for item in sim_list:
                if item[0][0] == -1:
                    item[0][0] = item[1]
                if item[0][1] == -1:
                    item[0][1] = item[1]
            #if plan.bcr_range[0] < 0:
            #    plan.bcr_range[0] = 'No Valid BCR'
            #if plan.bcr_range[1] < 0:
            #    plan.bcr_range[1] = 'No Valid BCR'
            #if plan.roi_range[0] < 0:
            #    plan.roi_range[0] = 'No Valid ROI'
            #if plan.roi_range[1] < 0:
            #    plan.roi_range[1] = 'No Valid ROI'
            #if plan.nond_roi_range[0] < 0:
            #    plan.nond_roi_range[0] = 'No Valid ROI'
            #if plan.nond_roi_range[1] < 0:
            #    plan.nond_roi_range[1] = 'No Valid ROI'

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

        # The distributions
        dist_dict = {'tri':triDistInv, 'rect':uniDistInv, 'none':none_dist,
                     'discrete':discrete_dist_inv, 'gauss':gauss_dist_inv}

        # The recurrence with a different frequency
        new_recurr = dist_dict[my_plan.recurr_dist](np.random.uniform(),
                                                    to_pass(my_plan.recurr_dist,
                                                            my_plan.recurr_range)[0],
                                                    to_pass(my_plan.recurr_dist,
                                                            my_plan.recurr_range)[1])
        new_mag = dist_dict[my_plan.mag_dist](np.random.uniform(),
                                              to_pass(my_plan.mag_dist, my_plan.mag_range)[0],
                                              to_pass(my_plan.mag_dist, my_plan.mag_range)[1])
        
        def for_plan(dist, mid, some_range):
            """ Sends the for plan."""
            if dist == "discrete":
                return some_range
            else:
                return [mid, some_range]
        # Creates a new plan (empty)
        delta_plan = Plan(my_plan.num, my_plan.name,
                          [my_plan.recurr_dist, for_plan(my_plan.recurr_dist, new_recurr, my_plan.recurr_range)],
                          [my_plan.mag_dist, for_plan(my_plan.mag_dist, new_mag, my_plan.mag_range)], self.discount_rate,
                          self.horizon, self.stat_life, self.parties)

        # Fills the new plan with the various parts
        delta_plan.bens = delta_plan.bens.one_iter(my_plan.bens.indiv)
        delta_plan.exts = delta_plan.exts.one_iter(my_plan.exts.indiv)
        delta_plan.costs = delta_plan.costs.one_iter(my_plan.costs.indiv)
        delta_plan.fat.update(my_plan.fat.averted, [my_plan.fat.desc], self.stat_life)
        delta_plan.nond_bens = delta_plan.nond_bens.one_iter(my_plan.nond_bens.indiv)

        # Specific pieces
        delta_plan.bens.dis_rate = new_recurr
        delta_plan.fat.disaster_rate = float(new_recurr)
        delta_plan.fat.update(delta_plan.fat.averted, [delta_plan.fat.desc], self.stat_life)

        return delta_plan

class Plan():
    """ Has all of the aspects of the plan. """
    tol = 1E-7
    def __init__(self, plan_id, plan_name, disaster_recurrence, disaster_magnitude,
                 discount_rate, horizon, stat_life, parties):
        # Basic Information
        self.num = int(plan_id)
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
            self.recurrence = max([disaster_recurrence[1][0], disaster_recurrence[1][1],
                                   disaster_recurrence[1][2]])
        else:
            self.recurr_uncert = disaster_recurrence[1]
            self.recurrence = disaster_recurrence[1][1]
            if isinstance(self.recurrence, list):
                self.recurrence = disaster_recurrence[1][0]
        self.mag_dist = disaster_magnitude[0]
        self.mag_range = disaster_magnitude[1]
        if self.mag_dist == "none":
            self.mag_uncert = [0]
            self.magnitude = disaster_magnitude[1][0]
        elif self.mag_dist == "gauss":
            self.mag_uncert = disaster_magnitude[1][1]
            self.magnitude = [disaster_magnitude[1][0]]
        elif self.mag_dist == "discrete":
            self.mag_uncert = list(disaster_magnitude)
            self.magnitude = max([disaster_magnitude[1][0], disaster_magnitude[1][1],
                                  disaster_magnitude[1][2]])
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
        """ Updates all of the aspects of the simulation. """
        # Basic Information
        self.num = int(plan_id)
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
            self.recurrence = max([disaster_recurrence[1][0], disaster_recurrence[1][2],
                                   disaster_recurrence[1][3]])
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
            self.magnitude = max([disaster_magnitude[1][0], disaster_magnitude[1][2],
                                  disaster_magnitude[1][3]])
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
        self.fat.disaster_rate = float(self.recurrence)
        self.fat.discount_rate = discount_rate
        self.fat.horizon = horizon
        self.fat.update(self.fat.averted, [self.fat.desc], stat_life)
        self.nond_bens.discount_rate = discount_rate
        self.nond_bens.horizon = horizon

    def new_plan(self, save_list, stat_life):
        """ Builds a plan from a list of pieces from the save file."""
        for line in save_list:
            if line[1] == "Costs":
                self.costs.new_cost(list(line[2:]))
            elif line[1] == "Benefits":
                self.bens.new_ben(list(line[2:]))
            elif line[1] == "Externalities":
                self.exts.new_ext(list(line[2:]))
            elif line[1] == "Fatalities":
                self.fat.update(line[2], line[3:], stat_life)
            elif line[1] == "Non-Disaster Benefits":
                self.nond_bens.new_ben(list(line[2:]))

    def save_plan(self, new_file):
        """ Saves a plan into the file."""
        # The first few lines
        new_file.write('Plan ' + str(self.num) + ',' + self.name + ',')
        new_file.write(self.recurr_dist + ',')
        if self.recurr_dist in {'discrete', 'rect', 'tri'}:
            if isinstance(self.recurr_uncert[0], list):
                recurr_uncert = self.recurr_uncert[0]
            else:
                recurr_uncert = self.recurr_uncert
            to_write = []
            for item in recurr_uncert:
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
        # Costs
        for cost in self.costs.indiv:
            new_file.write(',Costs,'+cost.title+','+cost.cost_type+','+cost.omr_type+',')
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
        # Benefits
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
        # Externalities
        for ext in self.exts.indiv:
            new_file.write(',Externalities,' + ext.title + ',' + ext.ext_type)
            for entry in ext.times:
                new_file.write(',' + str(entry))
            new_file.write(',' + str(ext.amount) + ',' + str(ext.desc) + '\n')
            new_file.write(',Externalities,')
            if ext.plus_minus == '+':
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
        # Non-Disaster Related Benefits
        for nond_ben in self.nond_bens.indiv:
            new_file.write(',Non-Disaster Benefits,'+nond_ben.title+','+nond_ben.ben_type+',')
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
        # Fatalities
        new_file.write(',Fatalities,' + str(self.fat.averted) + ',' + str(self.fat.desc) + '\n')

    def make_cash_flows(self, horizon):
        """ Makes cash flows for IRR
            Author: David Webb """
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
        for ext in self.exts.indiv:
            if ext.ext_type == "recurring":
                rec_list.append(ext)
            else:
                ot_list.append(ext)
        time_series = []
        time_series_w_ext = []
        for item in rec_list:
            is_ext = False
            start = float(item.times[0])
            rate = float(item.times[1])
            if isinstance(item, NonDBenefit):
                amount = float(item.amount)
            elif isinstance(item, Cost):
                amount = -float(item.amount)
            else:
                is_ext = True
                if item.plus_minus == "+":
                    amount = float(item.amount)
                else:
                    amount = -float(item.amount)
            i = 0
            while start + rate * i <= horizon + self.tol:
                time_series_w_ext.append([start + rate * i, amount])
                if not is_ext:
                    time_series.append([start + rate * i, amount])
                i += 1
                if rate <= self.tol:
                    break
        for item in ot_list:
            is_ext = False
            if isinstance(item, NonDBenefit):
                amount = float(item.amount)
            elif isinstance(item, Cost):
                amount = -float(item.amount)
            else:
                is_ext = True
                if item.plus_minus == "+":
                    amount = float(item.amount)
                else:
                    amount = -float(item.amount)
            time_series_w_ext.append([float(item.times[0]), amount])
            if not is_ext:
                time_series.append([float(item.times[0]), amount])

        time_series.sort(key=lambda x: x[0])
        time_series_w_ext.sort(key=lambda x: x[0])
        prev = -1
        for i in range(len(time_series)):
            if abs(time_series[i][0]-prev) <= self.tol:
                time_series[i][1] += float(time_series[i-1][1])
                time_series[i-1][0] = -1
            else:
                prev = time_series[i][0]
        for i in range(len(time_series_w_ext)):
            if abs(time_series_w_ext[i][0]-prev) <= self.tol:
                time_series_w_ext[i][1] += float(time_series_w_ext[i-1][1])
                time_series_w_ext[i-1][0] = -1
            else:
                prev = time_series_w_ext[i][0]

        self.annual_cash_flows = []
        for item in time_series:
            if item[0] != -1:
                self.annual_cash_flows.append(item)

        self.annual_cash_flows_w_ext = []
        for item in time_series_w_ext:
            if item[0] != -1:
                self.annual_cash_flows_w_ext.append(item)


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

        self.make_cash_flows(horizon)

        self.total_bens = self.bens.total + self.fat.stat_value_averted + self.nond_bens.total
        self.total_costs = self.costs.total
        self.net = self.total_bens - self.total_costs
        self.net_w_ext = self.total_bens + self.exts.total_p - self.total_costs - self.exts.total_n

    def bcr(self, w_ext=False):
        """Equation for the Benefit-to-Cost Ratio"""
        top_wo_ext = (self.bens.d_sum + self.bens.i_sum + self.bens.r_sum
                      + self.fat.stat_value_averted + self.nond_bens.total)
        bottom = self.costs.total

        if bottom == 0:
            return 'No Valid BCR'

        if w_ext:
            return (top_wo_ext + self.exts.total_p - self.exts.total_n) / bottom
        else:
            return top_wo_ext / bottom

    def irr(self, w_ext=False):
        """Equation for the Internal Rate of Return"""
        if w_ext:
            cash_flows = self.annual_cash_flows_w_ext
        else:
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

    def roi(self, w_ext=False):
        """Equation for the Return on Investment"""
        try:
            if w_ext:
                annual_savings = (self.total_bens + self.exts.total_p - self.total_costs - self.exts.total_n) / float(self.horizon)
                simple_payback = annual_savings / (self.total_costs + self.exts.total_n)
            else:
                annual_savings = (self.total_bens - self.total_costs) / float(self.horizon)
                simple_payback = annual_savings / self.total_costs
            return simple_payback * 100
        except ZeroDivisionError:
            return 'No Valid ROI'

    def non_d_roi(self, w_ext=False):
        """Equation for the Return on Investment (without any chance of disaster occurring)"""
        non_d_ben_total = self.nond_bens.r_sum + self.nond_bens.one_sum
        if w_ext:
            non_d_ben_total += self.exts.total_p

        annual_savings = non_d_ben_total / float(self.horizon)
        try:
            if w_ext:
                simple_payback = annual_savings / (self.total_costs + self.exts.total_n)
            else:
                simple_payback = annual_savings / self.total_costs
            return simple_payback * 100
        except ZeroDivisionError:
            return 'No Valid ROI'
