""" Uses matplotlib to create all plots and images."""

import numpy as np
import matplotlib
from matplotlib.figure import Figure

from tempfile import mkdtemp
from joblib import Memory

CACHEDIR = mkdtemp()
mem = Memory(cachedir=CACHEDIR, verbose=0)


matplotlib.use("TkAgg")

@mem.cache
def none_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = [0, 1, 2, 2.99, 3, 3.01, 4, 5, 6]
    y = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    sub.plot(x, y)

    return fig

@mem.cache
def disc_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = [0, 0.99, 1, 1.01, 1.99, 2, 2.01, 3, 3.99, 4, 4.01, 5, 6]
    y = [0, 0,    1, 0,    0,    3, 0,    0, 0,    2, 0,    0, 0]
    sub.plot(x,y)
    return fig

@mem.cache
def gauss_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = np.linspace(-3, 3, 100)
    y = matplotlib.mlab.normpdf(x, 0, 1)
    sub.plot(x, y)
    return fig

@mem.cache
def tri_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = range(5)
    y = [0] * len(x)
    y[2]=1
    sub.plot(x, y)
    return fig

@mem.cache
def rect_dist():
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x = [0, 0.99, 1, 2, 3, 4, 5, 5.01, 6]
    y = [0, 0, 1, 1, 1, 1, 1, 0, 0]
    sub.plot(x, y)
    return fig
