""" Contains all calculations for EconGuide and the class that holds all of the data."""
#File:          CostClass.py
#Author:        Shannon Grubb
#Email:         shannon.grubb@nist.gov
#Date:          May 2017
#Description:   Interacts with EconGuide.py, focusing on the costs and their uncertainties

class Costs():
    """ Contains all of the data for the costs of a simulation.    """
    direct = []
    indirect = []
    omr = []
    omr_type = []

    d_sum = [0]
    i_sum = [0]
    omr_1_sum = [0]
    omr_r_sum = [0]


    total = [0]

    def fill_direct(self, line, plan_index_list, fields_per):
        """ Reads in the direct costs from a file."""
        for index in plan_index_list:
            self.direct.append([])
            start_value = index
            count = 0
            for j in range(start_value, start_value + fields_per):
                if line[j] != "":
                    if (j-1) % fields_per == 0:
                        self.direct[-1].append([line[j]])
                        self.direct[-1][count].append(line[j+1])
                        self.direct[-1][count].append(line[j+2])
                        j = j + fields_per
                        count += 1

    def fill_indirect(self, line, plan_index_list, fields_per):
        """ Reads in the indirect costs from a file."""
        for index in plan_index_list:
            self.indirect.append([])
            start_value = index
            try:
                end_value = plan_index_list[plan_index_list.index(index)+1]
            except IndexError:
                end_value = len(line)
            count = 0
            for j in range(start_value, end_value):
                if line[j] != "":
                    if (j - 1) % fields_per == 0:
                        self.indirect[-1].append([line[j]])
                        self.indirect[-1][count].append(line[j+1])
                        self.indirect[-1][count].append(line[j+2])
                        j = j + fields_per
                        count += 1

    def summer(self, i, cash_flows, calc_one_time, calc_recur):
        """Calculates the sum of response/recovery cost reduction,
           direct cost reduction and indirect cost reduction
           for plan i."""
        # === Direct Costs
        for j in range(len(self.direct[i])):
            if self.direct[i][j][1] == "":
                self.direct[i][j][1] = 0
            self.d_sum[i] += float(self.direct[i][j][1])
            cash_flows[i][0] -= float(self.direct[i][j][1])

        # === Indirect Costs
        for j in range(len(self.indirect[i])):
            if self.indirect[i][j][1] == "":
                self.indirect[i][j][1] = 0
            self.i_sum[i] += float(self.indirect[i][j][1])
            cash_flows[i][0] -= float(self.indirect[i][j][1])

        # === One Time OMR / Recurring OMR
        for j in range(len(self.omr[i])):
            if self.omr[i][j][1] == "":
                self.omr[i][j][1] = 0

            if self.omr_type[i][j][0] == "OneTime":
                cash_flows[i][int(self.omr_type[i][j][1])] -= float(self.omr[i][j][1])
                add = calc_one_time(float(self.omr[i][j][1]), float(self.omr_type[i][j][1]))
                self.omr_1_sum[i] += add

            if self.omr_type[i][j][0] == "Recurring":
                add = calc_recur(float(self.omr[i][j][1]), float(self.omr_type[i][j][1]),
                                 float(self.omr_type[i][j][2]))
                self.omr_r_sum[i] += add
                for k in range(1, len(cash_flows[i])):
                    if k % int(self.omr_type[i][j][2]) == 0:
                        cash_flows[i][k] += -float(self.omr[i][j][1])
