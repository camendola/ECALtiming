import ROOT
from ROOT import TFile, TCanvas, TF1, TGraphAsymmErrors
import numpy as np


def slices_fit(histo):
    center = []
    low = []
    high = []
    mean = []
    sigma = []

    ROOT.gROOT.SetBatch(True)
    for i in range(1, histo.GetNbinsX() + 1):
        hY = histo.ProjectionY("prof" + str(i), i, i)
        if hY.Integral() < 0.00001:
            continue
        center.append(histo.GetXaxis().GetBinCenter(i))
        c1 = TCanvas("c1", "c1")
        low.append(histo.GetXaxis().GetBinCenter(i) - histo.GetXaxis().GetBinLowEdge(i))
        high.append(
            histo.GetXaxis().GetBinLowEdge(i)
            + histo.GetXaxis().GetBinWidth(i)
            - histo.GetXaxis().GetBinCenter(i)
        )

        hY = histo.ProjectionY("prof" + str(i), i, i)
        x0 = hY.GetMean()
        width = 2 * hY.GetRMS()
        f_gaus = TF1("f_gaus", "gaus", x0 - width, x0 + width)

        hY.Fit(f_gaus, "RQ")
        f_gaus.Draw("same")

        mean.append(f_gaus.GetParameter(1))
        sigma.append(f_gaus.GetParameter(2) / 2)

    ROOT.gROOT.SetBatch(False)

    x = np.asarray(center, dtype=np.float64)
    x_low = np.asarray(low, dtype=np.float64)
    x_high = np.asarray(high, dtype=np.float64)
    y = np.asarray(mean, dtype=np.float64)
    y_error = np.asarray(sigma, dtype=np.float64)

    graph = TGraphAsymmErrors(x.size, x, y, x_low, x_high, y_error, y_error)

    return graph


def slices_median(histo):
    ROOT.gROOT.SetBatch(True)
    center = []
    median = []

    for i in range(1, histo.GetNbinsX() + 1):
        hY = histo.ProjectionY("prof" + str(i), i, i)
        if hY.Integral() < 0.00001:
            continue
        center.append(histo.GetXaxis().GetBinCenter(i))

        c1 = TCanvas("c1", "c1")
        yq = np.asarray([0], dtype=np.float64)
        xq = np.asarray([0.5], dtype=np.float64)
        hY.GetQuantiles(1, yq, xq)
        median.append(yq[0])

    ROOT.gROOT.SetBatch(False)
    x = np.asarray(center, dtype=np.float64)
    y = np.asarray(median, dtype=np.float64)
    print(x, y)
    print(center, median)
    graph = TGraphAsymmErrors(x.size, x, y)

    return graph
