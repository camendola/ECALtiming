import ROOT
from array import array
import numpy

import matplotlib as mpl
import matplotlib.pyplot as plt

# matplotlib
def outlier_aware_hist(data, nbins , hrange = []):
    lower , upper = hrange
    if not lower or (lower < (data.min())):
        lower = data.min()
        lower_outliers = False
    else:
        lower_outliers = True

    if not upper or upper > data.max():
        upper = data.max()
        upper_outliers = False
    else:
        upper_outliers = True

    n, bins, patches = plt.hist(data, bins = nbins,range=(lower, upper))

    if lower_outliers:
        n_lower_outliers = (data < lower).sum()
        patches[0].set_height(patches[0].get_height() + n_lower_outliers)
        patches[0].set_label('Lower outliers: ({:.2f}, {:.2f})'.format(data.min(), lower))

    if upper_outliers:
        n_upper_outliers = (data > upper).sum()
        patches[-1].set_height(patches[-1].get_height() + n_upper_outliers)
        patches[-1].set_label('Upper outliers: ({:.2f}, {:.2f})'.format(upper, data.max()))

    return [n,bins,patches]


# conversion to ROOT
def pltToTH1(plot, name=""):
    print ("@ 1D hist: ", name) 
    bincontent, edge, patches = plot
    
    binsize = edge[1]-edge[0]
    
    xmin = edge[0]
    xmax = edge[-1]
    nbins = int((xmax-xmin)/binsize)

    
    hist = ROOT.TH1F(name, name, nbins, xmin,xmax) 
    for bin,content in enumerate(bincontent):
        hist.SetBinContent(bin, content)
    return hist


def pltToTH2(plot, name=""):
    print ("@ 2D hist: ", name) 
    bincontent, xedge, yedge, patches = plot


    xbinsize = xedge[1]-xedge[0]
    
    xmin = xedge[0]
    xmax = xedge[-1]
    nxbins = int((xmax-xmin)/xbinsize)

    ybinsize = yedge[1]-yedge[0]
    
    ymin = yedge[0]
    ymax = yedge[-1]
    nybins = int((ymax-ymin)/ybinsize)

    hist = ROOT.TH2F(name, name, nxbins, xmin,xmax, nybins, ymin, ymax) 
    for i in range(1, nxbins):
        for j in range(1, nybins):
            hist.SetBinContent(i,j, bincontent[i,j])
    return hist



def pltToTGraph(plot, name=""):
    x = plot.lines[0].get_xdata()
    y = plot.lines[0].get_ydata()
    x = numpy.asarray(x,dtype=numpy.float64) 
    y = numpy.asarray(y,dtype=numpy.float64) 
    
    graph = ROOT.TGraph(len(x), x , y)
    graph.SetName(name)
    return graph

