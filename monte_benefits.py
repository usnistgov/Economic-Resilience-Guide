
import random as r

from uniDistInv import uniDistInv
from triDistInv import triDistInv

from Data.ClassBenefits import Benefits

import numpy as np
import matplotlib
from matplotlib.figure import Figure

def monte_carlo(ben_original, plan, num_iters):
    ben_list = []

    for i in range(num_iters):
        ben_list.append(one_iter(ben_original, plan))


    direct_totals = []
    indirect_totals = []
    res_rec_totals = []
    for ben in ben_list:
        ben.summer(plan)
        direct_totals.append(ben.d_sum)
        indirect_totals.append(ben.i_sum)
        res_rec_totals.append(ben.r_sum)
    # TODO: Figure out how to report out

    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    n, bins, patches = sub.hist(direct_totals, 50)
    sub.show()


def one_iter(ben_original, plan, seed=100):
    dist_dict = {'Tri':triDistInv, 'Rect':uniDistInv}
    ## === direct
    # ==== For each direct benefit, pull distribution
    newBen = Benefits()
    d_dist = []
    d_size = []
    for benefit in range(len(ben_original.direct[plan])):
        print(ben_original.u_direct[plan])
        d_dist.append(ben_original.u_direct[plan][benefit][1])
        d_size.append(ben_original.u_direct[plan][benefit][0])
    # Build a new benefit with some variation within the dist
    r.random.seed(100)
    rand = r.random()

    for i in range(len(d_dist)):
        newBen.direct[0].append(dist_dict[d_dist[i]](rand, ben_original.direct[plan][i]-d_size[i], ben_original.direct[plan][i]+d_size[i]))

    ## === indirect
    for i in range(len(ben_original[plan].indirect)):
        newBen.indirect[0].append(ben_original.indirect[plan][i])

    ## === res_rec
    for i in range(len(ben_original[plan].res_rec)):
        newBen.res_rec[0].append(ben_original.res_rec[plan][i])

    return newBen
