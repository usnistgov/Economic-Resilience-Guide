""" Uses matplotlib to create all plots and images."""

from tempfile import mkdtemp
from joblib import Memory

import numpy as np
import matplotlib
from matplotlib.figure import Figure

CACHEDIR = mkdtemp()
MEM = Memory(cachedir=CACHEDIR, verbose=0)


matplotlib.use("TkAgg")

@MEM.cache
def none_dist():
    """ Plots a delta function w/o any labels. """
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x_pts = [0, 1, 2, 2.99, 3, 3.01, 4, 5, 6]
    y_pts = [0, 0, 0, 0, 1, 0, 0, 0, 0]
    sub.plot(x_pts, y_pts)

    return fig

@MEM.cache
def disc_dist():
    """ Plots the discrete distribution w/o any labels."""
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x_pts = [0, 0.99, 1, 1.01, 1.99, 2, 2.01, 3, 3.99, 4, 4.01, 5, 6]
    y_pts = [0, 0, 1, 0, 0, 3, 0, 0, 0, 2, 0, 0, 0]
    sub.plot(x_pts, y_pts)
    return fig

@MEM.cache
def gauss_dist():
    """ Plots the Gaussian distribution w/o any labels."""
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x_pts = np.linspace(-3, 3, 100)
    y_pts = matplotlib.mlab.normpdf(x_pts, 0, 1)
    sub.plot(x_pts, y_pts)
    return fig

@MEM.cache
def tri_dist():
    """ Plots the triangular distribution w/o any labels."""
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x_pts = range(5)
    y_pts = [0] * len(x_pts)
    y_pts[2] = 1
    sub.plot(x_pts, y_pts)
    return fig

@MEM.cache
def rect_dist():
    """ Plots the rectangular distribution w/o any labels."""
    fig = Figure(figsize=(0.5, 0.5), dpi=100)
    sub = fig.add_subplot(111)
    x_pts = [0, 0.99, 1, 2, 3, 4, 5, 5.01, 6]
    y_pts = [0, 0, 1, 1, 1, 1, 1, 0, 0]
    sub.plot(x_pts, y_pts)
    return fig
