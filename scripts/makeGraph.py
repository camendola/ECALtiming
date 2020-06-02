import ROOT 
from ROOT import TH1F, TGraphAsymmErrors, gPad, TF1, gStyle,TFile, TMultiGraph, TLegend, TGaxis
import argparse
import numpy as np
import os

def Frame(gPad,width=3):
    gPad.Update()
    gPad.RedrawAxis()
    l = ROOT.TLine()
    l.SetLineWidth(width)
    lm = gPad.GetLeftMargin();
    rm = 1.-gPad.GetRightMargin();
    tm = 1.-gPad.GetTopMargin();
    bm = gPad.GetBottomMargin();
    #top
    l.DrawLineNDC(lm,tm,rm,tm);
    #right
    l.DrawLineNDC(rm,bm,rm,tm);
    #bottom
    l.DrawLineNDC(lm,bm,rm,bm);
    #top
    l.DrawLineNDC(lm,bm,lm,tm);

def TextAuto(gPad, text, size = 0.05, font=42, align = 13):
    x = 0
    y = 0

    t = gPad.GetTopMargin()
    b = gPad.GetBottomMargin()
    l = gPad.GetLeftMargin()
    r = gPad.GetRightMargin()
    if align==13:
        x = l + 0.02
        y = 1 - t - 0.02
    if align==31:
        x = 1 - r 
        y = 1 - t + 0.01
    if align==11:
        x = l 
        y = 1 - t + 0.01
        
    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(size)
    latex.SetTextAlign(align)
    latex.SetTextFont(font)
    latex.DrawLatex(x,y,text)
    return latex

def Text(gPad, x, y, text, size = 0.03, font=42, align = 11):

    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(size)
    latex.SetTextAlign(align)
    latex.SetTextFont(font)
    latex.DrawLatex(x,y,text)
    return latex

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', dest='year', help='which year', default=None)
parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="BB_clean_ee")

parser.add_argument('--logy', dest='logy', help='log y' , default=False, action='store_true')
parser.add_argument('--logx', dest='logx', help='log x' , default=False, action='store_true')
parser.add_argument('--global', dest='glob', help='global', default=False, action = 'store_true')
parser.add_argument('--local', dest='loc', help='global', default=False, action = 'store_true')
parser.add_argument('--effs', dest='effs', help='make effective sigma graph', default=False, action = 'store_true')
parser.add_argument('--v', dest='v', help='display each fit', default=False, action = 'store_true')
parser.add_argument('--show', dest='show', help='show plots', default=False, action = 'store_true')

parser.add_argument('--name', dest='name', help='plot name', default=None)


args = parser.parse_args()

globselection = "BB_Run1Sel_ee_HighR9"
locselection = "B1_Run1Sel_e1_HighR9_e1"

if args.glob: 
    name = "deltaT_vs_effA_ee_"+globselection
else:
    name = "deltaT_vs_effA_e1_seeds_"+locselection

if args.year:
    years = [args.year]
else:
    years = ["2016", "2017", "2018"]

mg = TMultiGraph()


col_year = {
    "2016": [ROOT.kBlue,  ROOT.kBlue+1],
    "2017": [ROOT.kRed , ROOT.kRed +1],
    "2018": [ROOT.kGreen,  ROOT.kGreen+1]
}   

ADC2GEV_E = 0.060
ADC2GEV_B = 0.035

c = ROOT.TCanvas("c","c",700,600)
c.SetLeftMargin(0.17)
c.Draw()
ymax = 0
ymin = 1
legend = TLegend(0.17, 0.72, 0.89, 0.89)
for year in years:
    inFile = TFile.Open("plots/"+args.tag+"/"+year+"/sigma_"+name+".root")
    thisGraph = inFile.Get("Graph")
    thisGraph.SetLineColor(col_year[year][1])
    thisGraph.SetMarkerColor(col_year[year][1])

    thisFunc = thisGraph.GetFunction("func")
    thisFunc.SetLineColor(col_year[year][0])
    Nlabel = "N = {:.3f} #pm {:.3f} ns".format(thisFunc.GetParameter(0), thisFunc.GetParError(0))
    Clabel = "C = {:.3f} #pm {:.3f} ns".format(thisFunc.GetParameter(1), thisFunc.GetParError(1))
    legend.AddEntry(thisGraph, "{}, {}, {}".format(year, Nlabel, Clabel))
    this_ymax = thisGraph.GetHistogram().GetMaximum()
    this_ymin = thisGraph.GetHistogram().GetMinimum()
    ymax = max(ymax, this_ymax)
    ymin = min(ymin, this_ymin)
    #if args.glob: 
    #    thisGraph.RemovePoint(thisGraph.GetN()-1)
    #    thisFunc.SetRange(150, 1700)
    mg.Add(thisGraph)


mg.GetYaxis().SetTitle("#sigma(#Delta t) [ns]")
mg.GetXaxis().SetTitle("A_{eff}")
mg.Draw("ap")

xmin = 120
xmax = 3000
#if args.glob: xmax = 1800 
mg.GetHistogram().SetMinimum(ymin)
mg.GetHistogram().SetMaximum(ymax+ymax/4)

if args.logx: 
    c.SetLogx(1)
    mg.GetXaxis().SetLimits(xmin, xmax)
if args.logy: 
    c.SetLogy(1)
    mg.GetHistogram().SetMinimum(ymin)
    mg.GetHistogram().SetMaximum(ymax*2)
    mg.GetYaxis().SetMoreLogLabels()
    mg.GetYaxis().SetTitleOffset(1.9)
legend.SetBorderSize(0)
legend.SetTextSize(0.03)
legend.Draw("same")
c.SetGrid()
gStyle.SetGridStyle(2)
gStyle.SetGridColor(ROOT.kGray)

latex = Text(gPad, 0.88,0.65, "#scale[1.2]{#bf{CMS}} #font[50]{Preliminary}", align = 33)
latex = Text(gPad, 0.88,0.60,"Run2 Data (13 TeV)", align = 33,size = 0.03)
if args.glob: latex = Text(gPad, 0.88,0.55,"Z#rightarrow ee events, EB", align = 33,size = 0.03)
if args.loc: latex = Text(gPad, 0.88,0.55,"Same cluster, EB", align = 33,size = 0.03)

latex = Text(gPad, 0.88,0.48,"#sigma = #frac{N}{A_{eff}} #font[62]{#oplus} #sqrt{2}C", align = 33,size = 0.04)


top_axis = TGaxis(xmin ,mg.GetHistogram().GetMaximum(),xmax,mg.GetHistogram().GetMaximum(),ADC2GEV_B*xmin,ADC2GEV_B*xmax,510,"G-");
top_axis.SetTitle("E [GeV]")
top_axis.SetTitleSize(0.035)
top_axis.SetLabelSize(0.035)
top_axis.SetTitleFont(42)
top_axis.SetLabelFont(42)
top_axis.Draw()
Frame(gPad)
c.Update()

c.Modified()
input()
c.SaveAs("plots/"+args.tag+"/allYears/sigma_"+name+".png")
c.SaveAs("plots/"+args.tag+"/allYears/sigma_"+name+".pdf")