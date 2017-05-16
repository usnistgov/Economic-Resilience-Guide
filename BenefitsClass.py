""" Contains all calculations for EconGuide and the class that holds all of the data."""
#File:          BenefitsClass.py
#Author:        Shannon Grubb
#Email:         shannon.grubb@nist.gov
#Date:          May 2017
#Description:   Interacts with EconGuide.py, focusing on the benefits and their uncertainties

class Benefits():
    """ Contains all of the data for the benefits of a simulation.    """
    direct = []
    indirect = []
    res_rec = []

    d_sum = [0]
    i_sum = [0]
    r_sum = [0]

    u_direct = []
    u_indirect = []
    u_res_rec = []

    total = []

    def summer(self, i):
        """Calculates the sum of response/recovery cost reduction,
           direct cost reduction and indirect cost reduction
           for plan i."""
        # === Response/Recovery Costs Reduction
        for j in range(len(self.res_rec[i])):
            if self.res_rec[i][j][1] == "":
                self.res_rec[i][j][1] = 0
            self.r_sum[i] += float(self.res_rec[i][j][1])
        # === Direct Costs Reduction
        for j in range(len(self.direct[i])):
            if self.direct[i][j][1] == "":
                self.direct[i][j][1] = 0
            self.d_sum[i] += float(self.direct[i][j][1])

        # === Indirect Costs Reduction
        for j in range(len(self.indirect[i])):
            if self.indirect[i][j][1] == "":
                self.indirect[i][j][1] = 0
            self.i_sum[i] += float(self.indirect[i][j][1])
