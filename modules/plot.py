import ROOT
from array import array
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

# conversion to ROOT
def plt_to_TH1(plot, name=""):
    print("@ 1D hist: ", name)
    bincontent, edge, patches = plot

    binsize = edge[1] - edge[0]

    xmin = edge[0]
    xmax = edge[-1]
    nbins = int((xmax - xmin) / binsize)

    hist = ROOT.TH1F(name, name, nbins, xmin, xmax)
    for bin, content in enumerate(bincontent):
        hist.SetBinContent(bin + 1, content)
    #hist.Sumw2()
    return hist


def plt_to_TH2(plot, name=""):
    print("@ 2D hist: ", name)
    bincontent, xedge, yedge, patches = plot
    x = np.asarray(xedge, dtype=np.float64)
    y = np.asarray(yedge, dtype=np.float64)

    hist = ROOT.TH2F(name, name, len(x) - 1, x, len(y) - 1, y)
    for i in range(0, len(x) - 1):
        for j in range(0, len(y) - 1):
            hist.SetBinContent(i + 1, j + 1, bincontent[i, j])
    #hist.Sumw2()
    return hist


def table_to_TH2(table, name):
    print("@ 2D map: ", name)
    table = table.fillna(0)
    x = np.asarray(list(table.columns.values), dtype=np.float64)
    y = np.asarray(list(table.index.values), dtype=np.float64)
    x = np.append(x, x[-1] + 1)
    y = np.append(y, y[-1] + 1)

    hist = ROOT.TH2F(name, name, len(x) - 1, x, len(y) - 1, y)

    isPandas = False
    if len(table.columns.values) + 1 < 256:
        isPandas = True
    i = 0
    for row in table.itertuples():
        for j, value in enumerate(list(table.columns.values)):
            if isPandas:
                hist.SetBinContent(j + 1, i + 1, getattr(row, "_" + str(j + 1)))
            else:
                hist.SetBinContent(j + 1, i + 1, row[j+1])
        i += 1

    return hist


def plt_to_TGraph(plot, name="", binning=None):
    print("@ graph: ", name)
    x = plot.lines[0].get_xdata()
    y = plot.lines[0].get_ydata()
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    if len(binning) > 0:
        x = np.asarray((binning[1:] + binning[:-1]) / 2, dtype=np.float64)
        ex = np.asarray((binning[1:] - binning[:-1]) / 2, dtype=np.float64)
        graph = ROOT.TGraphErrors(len(x), x, y, ex, np.zeros(len(x)))
    else:
        graph = ROOT.TGraph(len(x), x, y)

    graph.SetName(name)
    return graph
