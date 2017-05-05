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
