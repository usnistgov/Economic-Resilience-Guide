
import random as r

from uniDistInv import uniDistInv
from triDistInv import triDistInv

from Data.ClassBenefits import Benefits, Benefit

import numpy as np
import matplotlib
from matplotlib.figure import Figure
from matplotlib import pyplot

def monte_carlo(ben_original, num_iters):
    ben_list = []

    for i in range(num_iters):
        ben_list.append(one_iter(ben_original))


    direct_totals = []
    indirect_totals = []
    res_rec_totals = []
    for ben in ben_list:
        ben.make_sum()
        direct_totals.append(ben.d_sum)
        indirect_totals.append(ben.i_sum)
        res_rec_totals.append(ben.r_sum)
    direct_totals.sort()
    indirect_totals.sort()
    res_rec_totals.sort()

    return([direct_totals[0], direct_totals[num_iters]],
           [indirect_totals[0], indirect_totals[num_iters]],
           [res_rec_totals[0], res_rec_totals[num_iters]])

    # TODO: Figure out how to report out

    fig = pyplot.figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    n, bins, patches = sub.hist(direct_totals, 50000)
    fig.show()


def one_iter(ben_original, new_seed=100):
    dist_dict = {'tri':triDistInv, 'rect':uniDistInv}
    delta_ben = Benefits(ben_original.dis_rate, ben_original.disc_rate, ben_original.horizon)
    r.seed(new_seed)
    for ben in ben_original.indiv:
        ben_dict = {'title': ben.title,
                    'ben_type': ben.ben_type,
                    'desc': ben.desc}
        rand = r.random()
        ben_dict['amount'] = dist_dict[ben.dist](rand, ben.amount-ben.range, ben.amount+ben.range)
        delta_ben.indiv.append(Benefit(**ben_dict))

    return delta_ben
