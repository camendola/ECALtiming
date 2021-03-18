import ROOT
from ROOT import TFile, TCanvas, TF1, TGraphAsymmErrors
import numpy as np


def Frame(gPad, width=2):
    gPad.Update()
    gPad.RedrawAxis()
    l = ROOT.TLine()
    l.SetLineWidth(width)
    lm = gPad.GetLeftMargin()
    rm = 1.0 - gPad.GetRightMargin()
    tm = 1.0 - gPad.GetTopMargin()
    bm = gPad.GetBottomMargin()
    # top
    l.DrawLineNDC(lm, tm, rm, tm)
    # right
    l.DrawLineNDC(rm, bm, rm, tm)
    # bottom
    l.DrawLineNDC(lm, bm, rm, bm)
    # top
    l.DrawLineNDC(lm, bm, lm, tm)


def TextAuto(gPad, text, size=0.05, font=42, align=13, line=1):
    x = 0
    y = 0

    t = gPad.GetTopMargin()
    b = gPad.GetBottomMargin()
    l = gPad.GetLeftMargin()
    r = gPad.GetRightMargin()
    if align == 13:
        x = l + 0.02
        y = 1 - t - 0.02
    if align == 31:
        x = 1 - r
        y = 1 - t + 0.01
    if align == 11:
        x = l
        y = 1 - t + 0.01

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(size)
    latex.SetTextAlign(align)
    latex.SetTextFont(font)
    latex.DrawLatex(x, y, text)
    return latex


def GetNDC(x):
    gPad.Update()
    return (x - gPad.GetX1()) / (gPad.GetX2() - gPad.GetX1())


infile = TFile.Open("plots/staggered_2021_03_15/outPlot_2018.root")

ca = TCanvas("ca", "ca", 800, 600)
ca.Draw()
#h2d = infile.Get("time_vs_iphi_B1")
#h2d = infile.Get("time_vs_ieta_B1")
h2d = infile.Get("time_vs_A_B1")
h2d.SetTitle("")
h2d.GetXaxis().SetTitle("Amplitude")
#h2d.GetXaxis().SetTitle("i#eta")
#h2d.GetXaxis().SetTitle("i#phi")
h2d.GetYaxis().SetTitle("e arrival time [ns]")

#h2d.GetYaxis().SetTitle("#eta")
h2d.Draw("colz")
ca.SetRightMargin(0.17)


center = []
low = []
high = []

mean = []
sigma = []
fit = False
if fit:
	ROOT.gROOT.SetBatch(True)
	for i in range(1, h2d.GetNbinsX() + 1):
	    center.append(h2d.GetXaxis().GetBinCenter(i))
	    c1 = TCanvas("c1", "c1")
	    low.append(h2d.GetXaxis().GetBinCenter(i) - h2d.GetXaxis().GetBinLowEdge(i))
	    high.append(
	        h2d.GetXaxis().GetBinLowEdge(i)
	        + h2d.GetXaxis().GetBinWidth(i)
	        - h2d.GetXaxis().GetBinCenter(i)
	    )
	    if low == 0: continue
	    hY = h2d.ProjectionY("prof" + str(i), i, i)
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
	graph.SetMarkerStyle(8)
	graph.SetMarkerColor(ROOT.kRed)
	graph.SetLineColor(ROOT.kRed)
	ca.cd()
	graph.Draw("same")

ROOT.gStyle.SetOptStat(0)
Frame(ROOT.gPad)
ca.Update()
ca.Modified()

input()
