""" Contains all calculations for EconGuide and the class that holds all of the data."""
#File:          Calculations.py
#Author:        Shannon Craig
#Email:         shannon.craig@nist.gov
#Date:          October 2016
#Description:   Interacts with EconGuide.py, focusing on the meat of the resilience calculations

import csv
    # Enables use of csv methods. look online for more info
import math
#import tkinter as tk
from tkinter import filedialog
#from tkinter import ttk
#from NewIRR import irr as calc_irr
from NewIRR import irr_for_all
#import numpy
    # Allows for the calculation of Internal Rate of Return (IRR).
    # This must be downloaded from the internet
import docx
# Allows analysis to be exported to a .docx file.
# This must be downloaded from the internet
from Constants import TAB

class Data():
    """ Contains all of the data for the simulations and does a bulk of the calculations.    """
    # Couldn't find a way to make this look nicer. Basically initializes all global lists
    plan_name = []
    DirectCost = []
    IndirectCost = []
    Externalities = []
    Omr = []
    OmrType = []
    DirectBen = []
    IndirectBen = []
    ResRec = []
    NonDBen = []
    Fatalities = []
    FIELDS_PER_VALUE = 3

    res_rec_sum = [0]
    direct_ben_sum = [0]
    indirect_ben_sum = [0]
    fatalities_sum = [0]
    direct_cost_sum = [0]
    indirect_cost_sum = [0]
    one_time_omr_sum = [0]
    recur_omr_sum = [0]
    one_time_non_d_ben_sum = [0]
    recur_non_d_ben_sum = [0]
    tot_costs = [0]
    tot_bens = [0]
    net = [0]
    non_d_ben_totals = [0]

    nonDBenNames = []
    up_front = []

    def __init__(self, file_name=''):
        """ Gives the option of building a file from scratch or reading it in as a .csv."""
        if file_name == '':
            pass
        else:
            initial_file = open(file_name, 'r')

            plan_index_list = []

            # Gathers all information from the .csv file
            # and places them into corresponding variables
            file_data = csv.reader(initial_file)

            for line in file_data:
                # ===== Records index values for each plan (for file reading)
                if line[0] == "-":
                    for item in line:
                        if item != "" and item != "-":
                            new_index = line.index(item)
                            plan_index_list.append(new_index)

            # Restarts the file cursor so that we can iterate over the file again
            initial_file.seek(0)

            count = 0
            for line in file_data:
                if line[0] == "Analysis Title":
                    self.analysis_title = line[1]
                elif line[0] == "Number of Plans":
                    self.num_plans = int(line[1])
                elif line[0] == "Objective Function":
                    self.objective = line[1]
                elif line[0] == "Planning Horizon":
                    self.horizon = int(line[1])
                elif line[0] == "Constraints":
                    self.constraints = line[1]
                elif line[0] == "Statistical Life":
                    self.stat_life = int(line[1])
                elif line[0] == "Discount Rate":
                    self.discount_rate = line[1]
                elif line[0] == "Disaster Rate":
                    self.disaster_rate = float(line[1])
                elif line[0] == "Disaster Magnitude":
                    self.dis_magnitude = line[1]
                elif line[0] == "Risk Preference":
                    self.risk_preference = line[1]
                # ===== Internal 'for loops' accounts for possible multiple scenarios/plans
                elif line[0] == "Name of Plans":
                    for i in range(1, len(line)):
                        if line[i] != "":
                            self.plan_name.append(line[i])

                elif line[0] == "Direct Costs":
                    for index in plan_index_list:
                        self.DirectCost.append([])
                        # 2nd dimension: Plan # (1st dimension is 'cost type')
                        start_value = index
                        for j in range(start_value, start_value + self.FIELDS_PER_VALUE):
                            if line[j] != "":
                                if (j-1) % self.FIELDS_PER_VALUE == 0:
                                    self.DirectCost[-1].append([line[j]])
                                    # 3rd dimension: Cost of corresponding plan | Title of the cost
                                    self.DirectCost[-1][count].append(line[j+1])
                                    self.DirectCost[-1][count].append(line[j+2])
                                    j = j + 3
                                    # $ value of the cost
                                    # Description of the cost
                                    count += 1
                        count = 0

                elif line[0] == "Indirect Costs":
                    for index in plan_index_list:
                        self.IndirectCost.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.IndirectCost[-1].append([line[j]])
                                    self.IndirectCost[-1][count].append(line[j+1])
                                    self.IndirectCost[-1][count].append(line[j+2])
                                    j = j + 3
                                    count += 1
                        count = 0

                elif line[0] == "OMR":
                    for index in plan_index_list:
                        self.Omr.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.Omr[-1].append([line[j]])
                                    self.Omr[-1][count].append(line[j+1])
                                    self.Omr[-1][count].append(line[j+2])
                                    j = j + 2
                                    count += 1
                        count = 0

                elif line[0] == "OMRType":
                    for index in plan_index_list:
                        self.OmrType.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.OmrType[-1].append([line[j]])
                                    self.OmrType[-1][count].append(line[j+1])
                                    self.OmrType[-1][count].append(line[j+2])
                                    j = j + 3
                                    count += 1
                        count = 0

                elif line[0] == "Externalities":
                    for index in plan_index_list:
                        self.Externalities.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.Externalities[-1].append([line[j]])
                                    self.Externalities[-1][count].append(line[j+1])
                                    self.Externalities[-1][count].append(line[j+2])
                                    # 3rd dimension: Cost of corresponding plan
                                    # Cost of the plan
                                    j = j+3
                                    count += 1
                        count = 0

                elif line[0] == "Direct Loss Reduction":
                    for index in plan_index_list:
                        self.DirectBen.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.DirectBen[-1].append([line[j]])
                                    self.DirectBen[-1][count].append(line[j+1])
                                    self.DirectBen[-1][count].append(line[j+2])
                                    j = j+3
                                    count += 1
                        count = 0

                elif line[0] == "Indirect Loss Reduction":
                    for index in plan_index_list:
                        self.IndirectBen.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.IndirectBen[-1].append([line[j]])
                                    self.IndirectBen[-1][count].append(line[j+1])
                                    self.IndirectBen[-1][count].append(line[j+2])
                                    j = j+3
                                    count += 1
                        count = 0

                elif line[0] == "Response/Recovery Costs":
                    for index in plan_index_list:
                        self.ResRec.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.ResRec[-1].append([line[j]])
                                    self.ResRec[-1][count].append(line[j+1])
                                    self.ResRec[-1][count].append(line[j+2])
                                    j = j+3
                                    count += 1
                        count = 0

                elif line[0] == "Non Disaster Related Benefits":
                    for index in plan_index_list:
                        self.NonDBen.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j - 1) % self.FIELDS_PER_VALUE == 0:
                                    self.NonDBen[-1].append([line[j]])
                                    self.NonDBen[-1][count].append(line[j+1])
                                    self.NonDBen[-1][count].append(line[j+2])
                                    j = j+3
                                    count += 1
                        count = 0
                elif line[0] == "NDRBType":
                    for index in plan_index_list:
                        start_value = index
                        i = plan_index_list.index(index)
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            if line[j] != "":
                                if (j-1) % self.FIELDS_PER_VALUE == 0:
                                    self.NonDBen[i][count].append(line[j])
                                    self.NonDBen[i][count].append(line[j+1])
                                    self.NonDBen[i][count].append(line[j+2])
                                    j = j+3
                                    count += 1
                        count = 0

                elif line[0] == "Fatalities Averted":
                    for index in plan_index_list:
                        self.Fatalities.append([])
                        start_value = index
                        try:
                            end_value = plan_index_list[plan_index_list.index(index)+1]
                        except IndexError:
                            end_value = len(line)
                        for j in range(start_value, end_value):
                            self.Fatalities[-1].append(line[j])

            initial_file.close()

            for i in range(self.num_plans + 1):
            # === Makes sure that fields aren't unnecessarily given default values
                if len(self.DirectCost[i]) == 0:
                    self.DirectCost[i].append(["", "", ""])
                if len(self.IndirectCost[i]) == 0:
                    self.IndirectCost[i].append(["", "", ""])
                if len(self.Omr[i]) == 0:
                    self.Omr[i].append(["", "", ""])
                    self.OmrType[i].append(["", "", ""])
                if len(self.DirectBen[i]) == 0:
                    self.DirectBen[i].append(["", "", ""])
                if len(self.IndirectBen[i]) == 0:
                    self.IndirectBen[i].append(["", "", ""])
                if len(self.ResRec[i]) == 0:
                    self.ResRec[i].append(["", "", ""])
                if len(self.Externalities[i]) == 0:
                    self.Externalities[i].append(["", "", ""])
                if len(self.NonDBen[i]) == 0:
                    self.NonDBen[i].append(["", "", "", "", "", ""])

# ========= Functions that complete meaningful calculations
    def on_dis_occ(self, value):
        """Equation used for Expected Value on disaster occurrence"""
        eqn_lambda = 1 / float(self.disaster_rate)
        k = float(self.discount_rate)/100
        mult = eqn_lambda / math.fabs(1 - math.exp(-k))
        return mult * (1 - math.exp(-k * float(self.horizon))) * value

    def calc_fatalities(self, value):
        """Equation used for Fatalities Aversion Calculation"""
        # == may need additional calculations
        return self.on_dis_occ(float(self.stat_life) * float(value))

    def calc_one_time(self, value, time):
        """Equation used for One-time OMR costs"""
        value = float(value)
        time = float(time)
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

    def sir(self, plan_num):
        """Equation for the Savings-to-Investment Ratio"""
        for i in range(self.num_plans + 1):
            self.up_front.append(self.direct_cost_sum[i] + self.indirect_cost_sum[i])

        if self.up_front[plan_num] == 0:
            return 0

        return self.net[plan_num] / self.up_front[plan_num]

    def irr(self, plan_num):
        """Equation for the Internal Rate of Return"""
        # === Calls the function so that self.up_front is calculated
        #self.sir(plan_num)

        #annual_cost = (self.tot_costs[plan_num] - self.up_front[plan_num]) / float(self.horizon)
        #annual_savings = self.tot_bens[plan_num] / float(self.horizon)

        #irr_list = [annual_savings - annual_cost] * (int(self.horizon) + 1)
        #irr_list[0] = -(self.up_front[plan_num])

        cash_flows = self.annual_non_disaster_cash_flows[plan_num]
        ben_list = [self.direct_ben_sum[plan_num], self.indirect_ben_sum[plan_num],
                    self.res_rec_sum[plan_num]]

        try:
            the_irr = irr_for_all(cash_flows, self.horizon, self.disaster_rate, ben_list,
                                  self.stat_life, self.Fatalities[plan_num][1])
            #calc_irr(irr_list)
        #except ValueError:
        #    print('ValueError')
        #    return 'No Valid IRR'
        except OverflowError:
            print('OverflowError')
            return 'No Valid IRR'

       # if str(calc_irr(irr_list)) == "nan":
       #     return 'No Valid IRR'
        return the_irr * 100


    def roi(self, plan_num):
        """Equation for the Return on Investment"""
        if self.tot_bens[plan_num] == 0:
            return 0
        elif self.tot_costs[plan_num] == 0:
            return 0
        annual_savings = self.tot_bens[plan_num] / float(self.horizon)
        simple_payback = self.tot_costs[plan_num] / annual_savings
        return (1 / simple_payback) * 100

    def non_d_roi(self, plan_num):
        """Equation for the Return on Investment (without any chance of disaster occurring)"""
        non_d_ben_total = self.recur_non_d_ben_sum[plan_num] + self.one_time_non_d_ben_sum[plan_num]

        if non_d_ben_total == 0:
            return 0
        elif self.tot_costs[plan_num] == 0:
            return 0
        annual_savings = non_d_ben_total / float(self.horizon)
        simple_payback = self.tot_costs[plan_num] / annual_savings
        return (1 / simple_payback) * 100

    def summer(self):
        """ Sums up all of the values."""
        self.res_rec_sum = [0]*(self.num_plans + 1)
        self.direct_ben_sum = [0]*(self.num_plans + 1)
        self.indirect_ben_sum = [0]*(self.num_plans + 1)
        self.fatalities_sum = [0]*(self.num_plans + 1)
        self.direct_cost_sum = [0]*(self.num_plans + 1)
        self.indirect_cost_sum = [0]*(self.num_plans + 1)
        self.one_time_non_d_ben_sum = [0]*(self.num_plans + 1)
        self.recur_non_d_ben_sum = [0]*(self.num_plans + 1)
        self.one_time_omr_sum = [0]*(self.num_plans + 1)
        self.recur_omr_sum = [0]*(self.num_plans + 1)
        self.tot_costs = [0]*(self.num_plans + 1)
        self.tot_bens = [0]*(self.num_plans + 1)
        self.net = [0]*(self.num_plans + 1)
        self.annual_non_disaster_cash_flows = [[0]*(int(self.horizon)+1) for i in range(int(self.num_plans)+1)]

        for i in range(len(self.NonDBen)):
            for j in range(len(self.NonDBen[i])):
                if (self.NonDBen[i][j][0] not in self.nonDBenNames) and self.NonDBen[i][j][0] != "":
                    self.nonDBenNames.append([self.NonDBen[i][j][0]])


        for i in range(self.num_plans + 1):
            # === Response/Recovery Costs Reduction
            for j in range(len(self.ResRec[i])):
                if self.ResRec[i][j][1] == "":
                    self.ResRec[i][j][1] = 0
                self.res_rec_sum[i] += float(self.ResRec[i][j][1])

            # === Direct Costs Reduction
            for j in range(len(self.DirectBen[i])):
                if self.DirectBen[i][j][1] == "":
                    self.DirectBen[i][j][1] = 0
                self.direct_ben_sum[i] += float(self.DirectBen[i][j][1])

            # === Indirect Costs Reduction
            for j in range(len(self.IndirectBen[i])):
                if self.IndirectBen[i][j][1] == "":
                    self.IndirectBen[i][j][1] = 0
                self.indirect_ben_sum[i] += float(self.IndirectBen[i][j][1])

            # === Fatalities Aversion
            self.fatalities_sum[i] = self.calc_fatalities(self.Fatalities[i][1])

            # === Direct Costs
            for j in range(len(self.DirectCost[i])):
                if self.DirectCost[i][j][1] == "":
                    self.DirectCost[i][j][1] = 0
                self.direct_cost_sum[i] += float(self.DirectCost[i][j][1])
                self.annual_non_disaster_cash_flows[i][0] -= float(self.DirectCost[i][j][1])

            # === Indirect Costs
            for j in range(len(self.IndirectCost[i])):
                if self.IndirectCost[i][j][1] == "":
                    self.IndirectCost[i][j][1] = 0
                self.indirect_cost_sum[i] += float(self.IndirectCost[i][j][1])
                self.annual_non_disaster_cash_flows[i][0] += -float(self.IndirectCost[i][j][1])

            # === One Time OMR  /  Recurring OMR
            for j in range(len(self.Omr[i])):
                if self.Omr[i][j][1] == "":
                    self.Omr[i][j][1] = 0

                if self.OmrType[i][j][0] == "OneTime":
                    self.annual_non_disaster_cash_flows[i][int(self.OmrType[i][j][1])] += -float(self.Omr[i][j][1])
                    to_add = self.calc_one_time(float(self.Omr[i][j][1]),
                                                float(self.OmrType[i][j][1]))
                    self.one_time_omr_sum[i] += to_add

                if self.OmrType[i][j][0] == "Recurring":
                    to_add = self.calc_recur(float(self.Omr[i][j][1]), float(self.OmrType[i][j][1]),
                                             float(self.OmrType[i][j][2]))
                    self.recur_omr_sum[i] += to_add
                    for k in range(1, len(self.annual_non_disaster_cash_flows[i])):
                        if k % int(self.OmrType[i][j][2]) == 0:
                            self.annual_non_disaster_cash_flows[i][k] += -float(self.Omr[i][j][1])

        # === NonDBens
            for j in range(len(self.NonDBen[i])):
                if self.NonDBen[i][j][1] == "":
                    pass
                elif self.NonDBen[i][j][3] == "OneTime":
                    to_add = self.calc_one_time(float(self.NonDBen[i][j][1]),
                                                float(self.NonDBen[i][j][4]))
                    self.one_time_non_d_ben_sum[i] += to_add
                    self.annual_non_disaster_cash_flows[i][int(self.NonDBen[i][j][4])] += float(self.NonDBen[i][j][1])
                elif self.NonDBen[i][j][3] == "Recurring":
                    to_add = self.calc_recur(float(self.NonDBen[i][j][1]),
                                             float(self.NonDBen[i][j][4]),
                                             float(self.NonDBen[i][j][5]))
                    self.recur_non_d_ben_sum[i] += to_add
                    for k in range(1, len(self.annual_non_disaster_cash_flows[i])):
                        if k % int(self.NonDBen[i][j][5]) == 0:
                            self.annual_non_disaster_cash_flows[i][k] += float(self.NonDBen[i][j][1])

        # === Totals
        for i in range(self.num_plans + 1):
            self.tot_bens[i] += self.on_dis_occ(self.res_rec_sum[i])
            self.tot_bens[i] += self.on_dis_occ(self.direct_ben_sum[i])
            self.tot_bens[i] += self.on_dis_occ(self.indirect_ben_sum[i])
            self.tot_bens[i] += self.fatalities_sum[i]
            self.tot_bens[i] += self.one_time_non_d_ben_sum[i] + float(self.recur_non_d_ben_sum[i])
            self.tot_costs[i] += float(self.direct_cost_sum[i]) + float(self.indirect_cost_sum[i])
            self.tot_costs[i] += float(self.one_time_omr_sum[i]) + float(self.recur_omr_sum[i])
            self.net[i] = self.tot_bens[i] - self.tot_costs[i]


# ========= Functions that interact with a text file =========

    def save_info(self):
        """Saves current progress
        First converts all information into a 2D array, then writes into .csv file.
        Accessible to all classes"""

        # === Holds the maximum lengths of any list related to each plan
        max_lengths = []
        for i in range(self.num_plans + 1):
            max_1 = max([len(self.DirectCost[i]), len(self.IndirectCost[i]), len(self.Omr[i])])
            max_2 = max([len(self.Externalities[i]), len(self.DirectBen[i])])
            max_3 = max([len(self.IndirectBen[i]), len(self.ResRec[i]), len(self.NonDBen[i])])
            max_lengths.append(max([max_1, max_2, max_3]))

        to_write_list = [["Analysis Title", self.analysis_title],   #0
                         ["Number of Plans", self.num_plans],       #1
                         ["Objective Function", self.objective],    #2
                         ["Planning Horizon", self.horizon],        #3
                         ["Constraints", self.constraints],         #4
                         ["Statistical Life", self.stat_life],      #5
                         ["Discount Rate", self.discount_rate],     #6
                         ["Disaster Rate", self.disaster_rate],     #7
                         ["Disaster Magnitude", self.dis_magnitude],#8
                         ["Risk Preference", self.risk_preference], #9
                         ["-", "Base"],                             #10
                         ["Name of Plans"],                         #11
                         [""],                                      #12
                         ["Costs"],                                 #13
                         ["Direct Costs"],                          #14
                         ["Indirect Costs"],                        #15
                         ["OMR"],                                   #16
                         ["OMRType"],                               #17
                         ["Externalities"],                         #18
                         ["Benefits"],                              #19
                         ["Direct Loss Reduction"],                 #20
                         ["Indirect Loss Reduction"],               #21
                         ["Response/Recovery Costs"],               #22
                         ["Non Disaster Related Benefits"],         #23
                         ["NDRBType"],                              #24
                         ["Fatalities Averted"]]                    #25

        # ===== The following 3 for loops are for Excel spreadsheet neatness
        for i in range(self.num_plans+1):
            if i != 0:
                to_write_list[10].append("Plan " + str(i))

            for j in range((max_lengths[i] * self.FIELDS_PER_VALUE) - 1):
                to_write_list[10].append("")
#        to_write_list[10].append("/")      # === Marks end of list of plans (for file reading)

        for i in range(self.num_plans+1):
            to_write_list[11].append(self.plan_name[i])
            for j in range((max_lengths[i]*self.FIELDS_PER_VALUE) - 1):
                to_write_list[11].append("")

        for i in range(self.num_plans+1):
            for j in range(max_lengths[i]):
                to_write_list[12].extend(["Title", "Dollar Amount", "Description"])

        # ===== Direct Cost
        for i in range(self.num_plans+1):
            for j in range(len(self.DirectCost[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[14].append(self.DirectCost[i][j][k])

            for j in range(max_lengths[i] - len(self.DirectCost[i])):
                to_write_list[14].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Indirect Cost
        for i in range(self.num_plans + 1):
            for j in range(len(self.IndirectCost[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[15].append(self.IndirectCost[i][j][k])

            for j in range(max_lengths[i] - len(self.IndirectCost[i])):
                to_write_list[15].extend([""]*self.FIELDS_PER_VALUE)

        # ===== OMR
        for i in range(self.num_plans + 1):
            for j in range(len(self.Omr[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[16].append(self.Omr[i][j][k])

            for j in range(max_lengths[i] - len(self.Omr[i])):
                to_write_list[16].extend([""]*self.FIELDS_PER_VALUE)

        # ===== OMRType
        for i in range(self.num_plans + 1):
            for j in range(len(self.OmrType[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[17].append(self.OmrType[i][j][k])

            for j in range(max_lengths[i] - len(self.OmrType[i])):
                to_write_list[17].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Externalities
        for i in range(self.num_plans + 1):
            for j in range(len(self.Externalities[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[18].append(self.Externalities[i][j][k])

            for j in range(max_lengths[i] - len(self.Externalities[i])):
                to_write_list[18].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Direct Loss Reductions
        for i in range(self.num_plans + 1):
            for j in range(len(self.DirectBen[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[20].append(self.DirectBen[i][j][k])

            for j in range(max_lengths[i] - len(self.DirectBen[i])):
                to_write_list[20].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Indirect Loss Reductions
        for i in range(self.num_plans + 1):
            for j in range(len(self.IndirectBen[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[21].append(self.IndirectBen[i][j][k])

            for j in range(max_lengths[i] - len(self.IndirectBen[i])):
                to_write_list[21].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Response/Recovery Cost Reductions
        for i in range(self.num_plans + 1):
            for j in range(len(self.ResRec[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[22].append(self.ResRec[i][j][k])

            for j in range(max_lengths[i] - len(self.ResRec[i])):
                to_write_list[22].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Non Disaster Related Benefits
        for i in range(self.num_plans + 1):
            for j in range(len(self.NonDBen[i])):
                for k in range(self.FIELDS_PER_VALUE):
                    to_write_list[23].append(self.NonDBen[i][j][k])

            for j in range(max_lengths[i] - len(self.NonDBen[i])):
                to_write_list[23].extend([""]*self.FIELDS_PER_VALUE)

        # ===== Non Disaster Related Benefits Recursion
        for i in range(self.num_plans + 1):
            for j in range(len(self.NonDBen[i])):
                if len(self.NonDBen[i][j]) < 6:
                    self.NonDBen[i][j].extend([""] * (4 - len(self.NonDBen[j])))
                for k in range(3, len(self.NonDBen[i][j])):
                    to_write_list[24].append(self.NonDBen[i][j][k])

            for j in range(max_lengths[i] - len(self.NonDBen[i])):
                to_write_list[24].extend([""] * self.FIELDS_PER_VALUE)

        # ===== Fatalities Averted
        for i in range(self.num_plans + 1):
            for j in range(self.FIELDS_PER_VALUE):
                to_write_list[25].append(self.Fatalities[i][j])

            for j in range(max_lengths[i] - 1):
                to_write_list[25].extend([""] * self.FIELDS_PER_VALUE)

        # ============ Prompts the user to select a location to save to (csv format)
        my_formats = [
            ('Comma Separated Value', '*.csv'),
        ]
        file_name = filedialog.asksaveasfilename(filetypes=my_formats, title="Save the file as...")
        if '.csv' not in file_name:
            file_name = file_name + '.csv'
        file = open(file_name, 'w')


        # ============ Take to_write_list and save into the user inputted location (as a .csv file)
        for row in range(10):
            for value in range(2):
                file.write(str(to_write_list[row][value]))
                file.write(',')
            file.write('\n')
        count = 0

        for i in range(self.num_plans + 1):
            for j in range(max_lengths[i]):
                count += self.FIELDS_PER_VALUE
        count += 2
        for value in range(len(to_write_list[10])):
            file.write(to_write_list[10][value])
            file.write(',')
        file.write('\n')

        count -= 1
        for row in range(11, 13):
            for value in range(count):
                file.write(str(to_write_list[row][value]))
                file.write(',')
            file.write('\n')
        file.write(str(to_write_list[13][0]))
        file.write('\n')

        for row in range(14, 19):
            for value in range(count):
                file.write(str(to_write_list[row][value]))
                file.write(',')
            file.write('\n')
        file.write(str(to_write_list[19][0]))
        file.write('\n')

        for row in range(20, 26):
            for value in range(count):
                file.write(str(to_write_list[row][value]))
                file.write(',')
            file.write('\n')

    def to_docx(self):
        """
        Allows user to save current analysis as a .docx file (for a complete report in paper-form)
        """
        my_formats = [
            ('Microsoft Word Document', '*.docx'),
        ]
        file_name = filedialog.asksaveasfilename(filetypes=my_formats, title="Save the file as...")
        if '.docx' not in file_name:
            file_name = file_name + '.docx'

        doc = docx.Document()               # === Opens a new .docx document

        doc.add_heading('Economic Evaluation Complete Report\n' + self.analysis_title, 0)

        doc.add_heading('Analysis Base Information\n', 1)
        doc.add_paragraph(TAB+'Number of Alternatives: '+str(self.num_plans))
        doc.add_paragraph(TAB+'Planning Horizon: '+str(self.horizon)+' years')
        doc.add_paragraph(TAB+'Discount Rate: '+str(self.discount_rate)+'%')
        doc.add_paragraph()
        doc.add_paragraph(TAB+'Disaster Rate: Every '+str(self.disaster_rate)+' years')
        doc.add_paragraph(TAB+'Disaster Magnitude: '+str(self.dis_magnitude)+'% of build cost')
        doc.add_paragraph(TAB+'Risk Preference: '+str(self.risk_preference))
        doc.add_paragraph()
        doc.add_paragraph(TAB+'Statistical Life Value: '+'${:,.0f}'.format(float(self.stat_life)))

        for i in range(self.num_plans + 1):
            if i == 0:
                doc.add_heading('Base Plan', 1)
            else:
                doc.add_heading(self.plan_name[i] + " (Alternative " + str(i) + ")", 1)

            doc.add_heading('Disaster-Related Benefits\n', 2)
            # === Makes sure the field isn't blank
            if self.ResRec[i][0][0] != "":
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Response and Recovery Cost Reductions\n')
                # === Allows the text to be bolded
                run.bold = True
                for j in range(len(self.ResRec[i])):
                    doc.add_paragraph(TAB + str(j+1) + ") " + self.ResRec[i][j][0])
                    dollar_amount = str('${:,.0f}'.format(float(self.ResRec[i][j][1])))
                    doc.add_paragraph(TAB + 'Dollar Amount: ' + dollar_amount)
                    present_value = self.on_dis_occ(float(self.ResRec[i][j][1]))
                    form_present_value = '${:,.0f}'.format(present_value)
                    doc.add_paragraph(TAB + 'Effective Present Value: ' + form_present_value)
                    doc.add_paragraph(TAB + 'Description: ' + str(self.ResRec[i][j][2]) + "\n")

            if self.DirectBen[i][0][0] != "":
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Direct Losses Prevented\n')
                run.bold = True
                for j in range(len(self.DirectBen[i])):
                    doc.add_paragraph(TAB + str(j+1) + ") " + self.DirectBen[i][j][0])
                    dollar_amount = str('${:,.0f}'.format(float(self.DirectBen[i][j][1])))
                    doc.add_paragraph(TAB + 'Dollar Amount: ' + dollar_amount)
                    present_value = self.on_dis_occ(float(self.DirectBen[i][j][1]))
                    form_present_value = '${:,.0f}'.format(present_value)
                    doc.add_paragraph(TAB + 'Effective Present Value: ' + form_present_value)
                    doc.add_paragraph(TAB + 'Description: ' + str(self.DirectBen[i][j][2]) + "\n")

            if self.IndirectBen[i][0][0] != "":
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Indirect Losses Prevented\n')
                run.bold = True
                for j in range(len(self.IndirectBen[i])):
                    doc.add_paragraph(TAB + str(j + 1) + ") " + self.IndirectBen[i][j][0])
                    doc.add_paragraph(TAB + 'Dollar Amount: '
                                      + str('${:,.0f}'.format(float(self.IndirectBen[i][j][1]))))
                    new_text = self.on_dis_occ(float(self.IndirectBen[i][j][1]))
                    doc.add_paragraph(TAB + 'Effective Present Value: '
                                      + '${:,.0f}'.format(new_text))
                    doc.add_paragraph(TAB + 'Description: ' + str(self.IndirectBen[i][j][2]) + "\n")

            if float(self.Fatalities[i][1]) != 0:
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Fatalities Averted\n')
                run.bold = True
                doc.add_paragraph(TAB + 'Number of Fatalities Averted: '
                                  + str(self.Fatalities[i][1]))
                doc.add_paragraph(TAB + 'Dollar Worth: '
                                  + str('${:,.0f}'.format(self.fatalities_sum[i])))
                doc.add_paragraph(TAB + 'Description: ' + str(self.Fatalities[i][2]) + "\n")

            if self.NonDBen[i][0][0] != "":
                doc.add_heading('Non-disaster-Related Benefits (Resilience Dividend)\n', 2)
                for j in range(len(self.NonDBen[i])):
                    if self.NonDBen[i][j][3] == "OneTime":
                        doc.add_paragraph(TAB + str(j+1) + ") " + self. NonDBen[i][j][0])
                        doc.add_paragraph(TAB + 'Dollar Amount: '
                                          + str('${:,.0f}'.format(float(self.NonDBen[i][j][1]))))
                        doc.add_paragraph(TAB + 'Year Applied: '
                                          + str(self.NonDBen[i][j][4]
                                                + ' years after plan start date'))
                        new_text = self.calc_one_time(float(self.NonDBen[i][j][1]),
                                                      float(self.NonDBen[i][j][4]))
                        doc.add_paragraph(TAB + 'Effective Present Value: '
                                          + '${:,.0f}'.format(new_text))
                        doc.add_paragraph(TAB + 'Description: ' + str(self.NonDBen[i][j][2]) + "\n")
                    if self.NonDBen[i][j][3] == "Recurring":
                        doc.add_paragraph(TAB + str(j + 1) + ") " + self.NonDBen[i][j][0])
                        doc.add_paragraph(TAB + 'Dollar Amount: '
                                          + str('${:,.0f}'.format(float(self.NonDBen[i][j][1]))))
                        doc.add_paragraph(TAB + 'Years Applied: '
                                          + str(self.NonDBen[i][j][4])
                                          + ' years after plan start date and every '
                                          + str(self.NonDBen[i][j][5]) + ' year(s) afterwards')
                        new_text = self.calc_recur(float(self.NonDBen[i][j][1]),
                                                   float(self.NonDBen[i][j][4]),
                                                   float(self.NonDBen[i][j][5]))
                        doc.add_paragraph(TAB + 'Effective Present Value: '
                                          + '${:,.0f}'.format(new_text))
                        doc.add_paragraph(TAB + 'Description: ' + str(self.NonDBen[i][j][2]) + "\n")

            doc.add_heading('Costs\n', 2)
            if self.DirectCost[i][0][0] != "":
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Up-Front Direct Costs\n')
                run.bold = True
                for j in range(len(self.DirectCost[i])):
                    doc.add_paragraph(TAB + str(j + 1) + ") " + self.DirectCost[i][j][0])
                    doc.add_paragraph(TAB + 'Dollar Amount: '
                                      + str('${:,.0f}'.format(float(self.DirectCost[i][j][1]))))
                    doc.add_paragraph(TAB + 'Effective Present Value: '
                                      + '${:,.0f}'.format(float(self.DirectCost[i][j][1])))
                    doc.add_paragraph(TAB + 'Description: ' + str(self.DirectCost[i][j][2]) + "\n")

            if self.IndirectCost[i][0][0] != "":
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Up-Front Indirect Costs\n')
                run.bold = True
                for j in range(len(self.IndirectCost[i])):
                    doc.add_paragraph(TAB + str(j + 1) + ") " + self.IndirectCost[i][j][0])
                    doc.add_paragraph(TAB + 'Dollar Amount: '
                                      + str('${:,.0f}'.format(float(self.IndirectCost[i][j][1]))))
                    doc.add_paragraph(TAB + 'Effective Present Value: '
                                      + '${:,.0f}'.format(float(self.IndirectCost[i][j][1])))
                    doc.add_paragraph(TAB + 'Description: '
                                      + str(self.IndirectCost[i][j][2]) + "\n")

            has_one_time = False
            for j in range(len(self.OmrType[i])):
                # === Checks if there are ANY One-time OMRs to report
                if self.OmrType[i][j][0] == "OneTime":
                    has_one_time = True
            if has_one_time:
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'One-time Operation, Management, or Repairs Costs\n')
                run.bold = True
                for j in range(len(self.Omr[i])):
                    if self.OmrType[i][j][0] == "OneTime":
                        doc.add_paragraph(TAB + str(j + 1) + ") " + self.Omr[i][j][0])
                        doc.add_paragraph(TAB + 'Dollar Amount: '
                                          + str('${:,.0f}'.format(float(self.Omr[i][j][1]))))
                        doc.add_paragraph(TAB + 'Year Applied: '
                                          + str(self.OmrType[i][j][1]
                                                + ' years after plan start date'))
                        new_text = self.calc_one_time(float(self.Omr[i][j][1]),
                                                      float(self.OmrType[i][j][1]))
                        doc.add_paragraph(TAB + 'Effective Present Value: '
                                          + '${:,.0f}'.format(new_text))
                        doc.add_paragraph(TAB + 'Description: ' + str(self.Omr[i][j][2]) + "\n")

            has_recurring = False
            for j in range(len(self.OmrType[i])):
                # === Checks if there are ANY Recurring OMRs to report
                if self.OmrType[i][j][0] == "Recurring":
                    has_recurring = True
            if has_recurring:
                paragraph = doc.add_paragraph()
                run = paragraph.add_run(TAB + 'Recurring Operation, Management, or Repairs Costs\n')
                run.bold = True
                for j in range(len(self.Omr[i])):
                    if self.OmrType[i][j][0] == "Recurring":
                        doc.add_paragraph(TAB + str(j + 1) + ") " + self.Omr[i][j][0])
                        doc.add_paragraph(TAB + 'Dollar Amount: '
                                          + str('${:,.0f}'.format(float(self.Omr[i][j][1]))))
                        doc.add_paragraph(TAB + 'Years Applied: '
                                          + str(self.OmrType[i][j][1])
                                          + ' years after plan start date'
                                          ' and every ' + str(self.OmrType[i][j][2])
                                          + ' year(s) afterwards')
                        new_text = self.calc_recur(float(self.Omr[i][j][1]),
                                                   float(self.OmrType[i][j][1]),
                                                   float(self.OmrType[i][j][2]))
                        doc.add_paragraph(TAB + 'Effective Present Value: '
                                          + '${:,.0f}'.format(new_text))
                        doc.add_paragraph(TAB + 'Description: ' + str(self.Omr[i][j][2]) + "\n")

            doc.add_heading('Totals\n', 2)

            paragraph = doc.add_paragraph()
            if self.net[i] >= 0:
                run = paragraph.add_run(TAB + 'Total Benefits: '
                                        + '${:,.0f}'.format(self.tot_bens[i])
                                        + '\n' + TAB + 'Total Costs: '
                                        + '${:,.0f}'.format(self.tot_costs[i])
                                        + '\n' + TAB + 'Net: '
                                        + '${:,.0f}'.format(self.net[i]))
            else:
                run = paragraph.add_run(TAB + 'Total Benefits: '
                                        + '${:,.0f}'.format(self.tot_bens[i])
                                        + '\n' + TAB + 'Total Costs: '
                                        + '${:,.0f}'.format(self.tot_costs[i])
                                        + '\n' + TAB + 'Net: ('
                                        + '${:,.0f}'.format(self.net[i])+')')
            run.bold = True
            doc.add_paragraph()
            doc.add_paragraph(TAB + 'Savings-to-Investment Ratio (SIR): '
                              + '{:,.2f}'.format(self.sir(i)))
            try:
                text = '{:,.1f}'.format(self.irr(i))+'%'
            except ValueError:
                text = self.irr(i)
            doc.add_paragraph(TAB+'Internal Rate of Return (IRR): '+ text)
            doc.add_paragraph(TAB+'Return on Investment (ROI): '+'{:,.1f}'.format(self.roi(i))+'%')
            doc.add_paragraph(TAB+'Non-Disaster ROI: '+'{:,.1f}'.format(self.non_d_roi(i))+'%')

            doc.save(file_name)


    def to_csv(self):
        """Allows the user to save summary of analysis as a .csv file
        (not to be confused with the to_save .csv file)"""
        to_write_list = [["Outputs of Economic Evaluation: [" + str(self.analysis_title) + "]"], #0
                         [" ", "Base Case"],                                                     #1
                         [" "],                                                                  #2
                         ["Benefits"],                                                           #3
                         ["Disaster Economic Benefits"],                                         #4
                         ["Response and Recovery Costs"],                                        #5
                         ["Direct Losses Prevented"],                                            #6
                         ["Indirect Losses Prevented"],                                          #7
                         ["Disaster Non-Market Benefits"],                                       #8
                         ["Lives Saved"],                                                        #9
                         ["Non-disaster Related Benefits"]]                                      #10

        to_write_list.extend([["Costs"],                                              #11
                              ["Initial"],                                            #12
                              ["Direct Cost"],                                        #13
                              ["Indirect Cost"],                                      #14
                              ["OMR"],                                                #15
                              ["Recurring Costs"],                                    #16
                              ["OMR"],                                                #17
                              ["Total: Present Expected Value"],                      #18
                              ["Benefits"],                                           #19
                              ["Costs"],                                              #20
                              ["Net"],                                                #21
                              [" "],                                                  #22
                              ["Savings-to-Investment Ratio (SIR)"],                  #23
                              ["Internal Rate of Return (IRR)"],                      #24
                              ["Return on Investment (ROI)"],                         #25
                              ["Non-Disaster ROI"]])                                  #26

        for i in range(1, self.num_plans + 1):
            to_write_list[1].append("Alternative " + str(i))
        for i in range(self.num_plans + 1):
            to_write_list[0].append(" ")
            to_write_list[2].append(self.plan_name[i])
            to_write_list[3].append(" ")
            to_write_list[4].append(" ")
            to_write_list[5].append('${:.0f}'.format(self.on_dis_occ(self.res_rec_sum[i])))
            to_write_list[6].append('${:.0f}'.format(self.on_dis_occ(self.direct_ben_sum[i])))
            to_write_list[7].append('${:.0f}'.format(self.on_dis_occ(self.indirect_ben_sum[i])))
            to_write_list[8].append(" ")
            to_write_list[9].append('${:.0f}'.format(self.calc_fatalities(self.Fatalities[i][1])))
            # == Calculation NDRB sum
            total = 0
            for j in range(len(self.NonDBen[i])):
                if self.NonDBen[i][j][3] == 'OneTime':
                    total += self.calc_one_time(self.NonDBen[i][j][1], self.NonDBen[i][j][4])
                elif self.NonDBen[i][j][3] == 'Recurring':
                    total += self.calc_recur(self.NonDBen[i][j][1],
                                             self.NonDBen[i][j][4], self.NonDBen[i][j][5])
            to_write_list[10].append('${:.0f}'.format(total))

        for i in range(self.num_plans + 1):
            to_write_list[11].append(" ")
            to_write_list[12].append(" ")
            to_write_list[13].append('${:.0f}'.format(self.direct_cost_sum[i]))
            to_write_list[14].append('${:.0f}'.format(self.indirect_cost_sum[i]))
            to_write_list[15].append('${:.0f}'.format(self.one_time_omr_sum[i]))
            to_write_list[16].append(" ")
            to_write_list[17].append('${:.0f}'.format(self.recur_omr_sum[i]))
            to_write_list[18].append(" ")
            to_write_list[19].append('${:.0f}'.format(self.tot_bens[i]))
            to_write_list[20].append('${:.0f}'.format(self.tot_costs[i]))
            if self.net[i] >= 0:
                to_write_list[21].append('${:.0f}'.format(self.net[i]))
            else:
                to_write_list[21].append('(${:.0f}'.format(self.net[i]) + ')')
            to_write_list[22].append(" ")
            to_write_list[23].append('{:.2f}'.format(self.sir(i)))
            to_write_list[24].append('{:.1f}'.format(self.irr(i)) + '%')
            to_write_list[25].append('{:.1f}'.format(self.roi(i)) + '%')
            to_write_list[26].append('{:.1f}'.format(self.non_d_roi(i)) + '%')


        # ============ Prompts the user to select a location to save to (csv format)
        my_formats = [('Comma Separated Value', '*.csv'),]
        file_name = filedialog.asksaveasfilename(filetypes=my_formats, title="Save the file as...")
        if '.csv' not in file_name:
            file_name = file_name + '.csv'
        file = open(file_name, 'w')

        # ============ Take to_write_list and save into the user inputted location (as a .csv file)
        for row in range(26):
            for value in range(self.num_plans + 2):
                file.write(str(to_write_list[row][value]))
                file.write(',')
            file.write('\n')
