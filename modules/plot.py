import ROOT
from array import array
import numpy as np
import pandas as pd

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

    bincontent, edge, patches = plt.hist(data, bins = nbins,range=(lower, upper))
    
    if lower_outliers:
        n_lower_outliers = (data < lower).sum()
       
        bincontent[0] = (bincontent[0] + n_lower_outliers)
        patches[0].set_label('Lower outliers: ({:.2f}, {:.2f})'.format(data.min(), lower))
        print('Lower outliers: ({:.2f}, {:.2f}), n = {:.2f}'.format(data.min(), lower, n_lower_outliers))
    if upper_outliers:
        n_upper_outliers = (data > upper).sum()
        bincontent[-1] = (bincontent[-1] + n_upper_outliers)
        patches[-1].set_label('Upper outliers: ({:.2f}, {:.2f})'.format(upper, data.max()))
        print('Upper outliers: ({:.2f}, {:.2f}),  n = {:.2f}'.format(upper, data.max(), n_upper_outliers))
    
    return [bincontent,edge,patches]


# conversion to ROOT
def plt_to_TH1(plot, name=""):
    print ("@ 1D hist: ", name) 
    bincontent, edge, patches = plot
    
    binsize = edge[1]-edge[0]
    
    xmin = edge[0]
    xmax = edge[-1]
    nbins = int((xmax-xmin)/binsize)

    
    hist = ROOT.TH1F(name, name, nbins, xmin,xmax) 
    for bin,content in enumerate(bincontent):
        hist.SetBinContent(bin+1, content)
    return hist


#def plt_to_TH2(plot, name=""):
#    print ("@ 2D hist: ", name) 
#    bincontent, xedge, yedge, patches = plot
#    xbinsize = xedge[1]-xedge[0]
#    
#    xmin = xedge[0]
#    xmax = xedge[-1]
#    nxbins = int((xmax-xmin)/xbinsize)
#
#    ybinsize = yedge[1]-yedge[0]
#    
#    ymin = yedge[0]
#    ymax = yedge[-1]
#    nybins = int((ymax-ymin)/ybinsize)
#
#    hist = ROOT.TH2F(name, name, nxbins, xmin, xmax, nybins, ymin, ymax) 
#    for i in range(1, nxbins):
#        for j in range(1, nybins):
#            hist.SetBinContent(i,j, bincontent[i,j])
#    return hist

def plt_to_TH2(plot, name=""):
    print ("@ 2D hist: ", name) 
    bincontent, xedge, yedge, patches = plot
    x = np.asarray(xedge, dtype = np.float64)
    y = np.asarray(yedge, dtype = np.float64)

    hist = ROOT.TH2F(name, name, len(x)-1, x, len(y)-1, y) 
    for i in range(0, len(x)-1):
        for j in range(0, len(y)-1):
            hist.SetBinContent(i+1,j+1, bincontent[i,j])
    return hist


def table_to_TH2(table, name):
    print ("@ 2D map: ", name) 
    table = table.fillna(0)
    x = np.asarray(list(table.columns.values), dtype = np.float64)
    y = np.asarray(list(table.index.values), dtype = np.float64)
    if x[0] < 0: x = x[1:]
    if y[0] < 0: y = y[1:]
    x = np.append(x, x[-1]+1)
    y = np.append(y, y[-1]+1)

    hist = ROOT.TH2F(name, name, len(x)-1, x, len(y)-1, y) 

    isPandas = False
    if(len(table.columns.values) + 1 < 256): isPandas = True
    i = 0
    for row in table.itertuples():
        for j , val in enumerate(list(table.columns.values)):
            if isPandas: 
                hist.SetBinContent(i+1,j+1,getattr(row, "_"+str(j+1)))
            else: 
                hist.SetBinContent(i+1,j+1,row[j]) 
        i += 1

    return hist

def plt_to_TGraph(plot, name="", labels = None, binwidth = None):
    print ("@ graph: ", name) 
    x = plot.lines[0].get_xdata()
    y = plot.lines[0].get_ydata()
    if len(labels) > 0 : x = labels
    x = np.asarray(x,dtype=np.float64) 
    y = np.asarray(y,dtype=np.float64) 
    if len(binwidth) > 0:
        ex = np.asarray((binwidth[1:] - binwidth[:-1]) / 2, dtype=np.float64)

        graph = ROOT.TGraphErrors(len(x), x , y, ex,    np.zeros(len(x)))
    else:
        graph = ROOT.TGraph(len(x), x , y)
    
    graph.SetName(name)
    return graph