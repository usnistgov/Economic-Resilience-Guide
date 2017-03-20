""" Uses matplotlib to create all plots and images."""

import numpy as np
import matplotlib
from matplotlib.figure import Figure

matplotlib.use("TkAgg")


def none_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = [0, 1, 2, 2.99, 3, 3.01, 4, 5, 6]
    y = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    sub.plot(x, y)

    return fig

def gauss_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = np.linspace(-3, 3, 100)
    y = matplotlib.mlab.normpdf(x, 0, 1)
    sub.plot(x, y)
    return fig

def tri_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = range(5)
    y = [0] * len(x)
    y[2]=1
    sub.plot(x, y)
    return fig

def rect_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = [0, 0.99, 1, 2, 3, 4, 5, 5.01, 6]
    y = [0, 0, 1, 1, 1, 1, 1, 0, 0]
    sub.plot(x, y)
    return fig
