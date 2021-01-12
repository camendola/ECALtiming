import ROOT 
from ROOT import TH1F, TGraphAsymmErrors, gPad, TF1, gStyle,TFile
import argparse
import numpy as np
import os

def Frame(gPad,width=2):
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

parser.add_argument('--year', dest='year', help='which year', default=2016)
parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="BB_clean_ee")
parser.add_argument('--skip', dest='skip', help='skip first bins', type = int, default=0)


parser.add_argument('--logy', dest='logy', help='log y' , default=False, action='store_true')
parser.add_argument('--logx', dest='logx', help='log x' , default=False, action='store_true')
parser.add_argument('--global', dest='glob', help='global', default=False, action = 'store_true')
parser.add_argument('--effs', dest='effs', help='make effective sigma graph', default=False, action = 'store_true')
parser.add_argument('--v', dest='v', help='display each fit', default=False, action = 'store_true')
parser.add_argument('--show', dest='show', help='show plots', default=False, action = 'store_true')



parser.add_argument('--name', dest='name', help='plot name', default=None)
parser.add_argument('--xlabel', dest='xlabel', help='xlabel', default=None)
parser.add_argument('--ylabel', dest='ylabel', help='ylabel', default=None)

args = parser.parse_args()

inFile = ROOT.TFile.Open("plots/"+args.tag+"/outPlot_"+args.year+".root")

name = "deltaT_vs_effA_e1"
N = 3.30413e+01
C = 9.27409e-02
if args.year == "2018":
    N =  5.36645e+01
    C =  1.89872e-01

if args.glob: 
	name = "deltaT_vs_effA_ee"

histo = inFile.Get(name+"_"+args.sel)

sigma = []
sigma_error = []
mean = []
print(histo.GetNbinsX())
center = []
low = []
high = []
c1 = ROOT.TCanvas("c","c",700,600)
c1.Draw()


for i in range(1, histo.GetNbinsX()+1):
    if i < args.skip: continue
    center.append(histo.GetXaxis().GetBinCenter(i))
    low.append(histo.GetXaxis().GetBinCenter(i)- histo.GetXaxis().GetBinLowEdge(i))
    high.append(histo.GetXaxis().GetBinLowEdge(i)+ histo.GetXaxis().GetBinWidth(i) -histo.GetXaxis().GetBinCenter(i))
    hY = histo.ProjectionY("prof"+str(i),i,i)
    v = []
    #hY.Draw("hist")
    #hY.Fit("gaus")
    #gaus= hY.GetListOfFunctions().FindObject("gaus")

    x0 = hY.GetMean()
    width = 2*hY.GetRMS()
    #if (args.year == "2018") and i == histo.GetNbinsX():
    #    x0 = mean[-1]
    #    width = 3*sigma[-1]
    #if (args.glob) and i == histo.GetNbinsX(): 
    #    hY.Rebin(2)
    #    x0 = mean[-1]
    #    width = 3*sigma[-1]
    f_gaus = TF1("f_gaus","gaus",x0 - width,x0 + width)
    

    hY.Fit(f_gaus, "R")
    if args.v:
        f_gaus.Draw("same")
        c1.Update()
        c1.Modified()
        input()
    #sigma.append(hY.GetRMS())
    #sigma.append(gaus.GetParameter(2))
    mean.append(f_gaus.GetParameter(1))
    sigma.append(f_gaus.GetParameter(2))
    sigma_error.append(f_gaus.GetParError(2)/2)
print(sigma)


x = np.asarray(center, dtype = np.float64)
x_low = np.asarray(low, dtype = np.float64)
x_high = np.asarray(high, dtype = np.float64)
y = np.asarray(sigma, dtype = np.float64)
y_error = np.asarray(sigma_error, dtype = np.float64)


print(x, x_low, x_high)
graph = TGraphAsymmErrors(x.size, x,y,x_low,x_high, y_error, y_error)
graph.SetMarkerStyle(8)
c = ROOT.TCanvas("c","c",700,600)
c.SetLeftMargin(0.17)
c.Draw()
graph.GetYaxis().SetTitle("#sigma(#Delta t) [ns]")
graph.GetXaxis().SetTitle("A_{eff}")
graph.Draw("ap")
if args.logx: 
    c.SetLogx(1)
    graph.GetXaxis().SetLimits(x[0]-2*x_low[0], x[-1]+2*x_low[-1])
if args.logy: 
    c.SetLogy(1)
    graph.GetHistogram().SetMinimum(y.min()/2)
    graph.GetHistogram().SetMaximum(y.max()*3)

graph.SetTitle("")
Frame(gPad)
yrlabel = TextAuto(gPad, args.year, align = 31)
last = histo.GetNbinsX() - 1 

func = TF1("func","sqrt(([0]/(x))^2 + 2*([1]^2))", x[0]-x_low[0], x[last]+x_high[last])
func.SetParameter(0, N)
func.SetParameter(1, C)

graph.Fit("func","R")
Nlabel = Text(gPad, 0.6, 0.7, "N = {:.3f} #pm {:.3f} ns".format(func.GetParameter(0), func.GetParError(0)))
Clabel = Text(gPad, 0.6, 0.65,"C = {:.3f} #pm {:.3f} ns".format(func.GetParameter(1), func.GetParError(1)))

c.Update()
c.Modified()

if args.show: input()


hfit = TH1F("hfit","hfit", 4, 0, 4)
hfit.SetBinContent(1, func.GetParameter(0))
hfit.SetBinContent(2, func.GetParameter(1))
hfit.SetBinContent(3, func.GetParError(0))
hfit.SetBinContent(4, func.GetParError(1))
hfit.GetXaxis().SetBinLabel(1, "N")
hfit.GetXaxis().SetBinLabel(2, "C")
hfit.GetXaxis().SetBinLabel(3, "N_error")
hfit.GetXaxis().SetBinLabel(4, "C_error")

if (args.effs):
    ename = "effs_deltaT_e1_vs_effA_e1"
    if args.glob: 
        ename = "effs_deltaT_ee_vs_effA_ee"

    eff_s_graph = inFile.Get(ename+"_"+args.sel)

    eff_s_graph.SetMarkerStyle(8)
    c2 = ROOT.TCanvas("c2","c2",700,600)
    c2.SetLeftMargin(0.17)
    c2.Draw()
    eff_s_graph.GetYaxis().SetTitle("#sigma_{eff}(#Delta t) [ns]")
    eff_s_graph.GetXaxis().SetTitle("A_{eff}")
    eff_s_graph.Draw("ap")
    if args.logx: 
        c2.SetLogx(1)
        eff_s_graph.GetXaxis().SetLimits(x[0]-2*x_low[0], x[-1]+2*x_low[-1])
    if args.logy: 
        c2.SetLogy(1)
        eff_s_graph.GetHistogram().SetMinimum(y.min()/2)
        eff_s_graph.GetHistogram().SetMaximum(y.max()*3)
    eff_s_graph.GetXaxis().SetLimits(100, 2500)
    eff_s_graph.SetTitle("")
    Frame(gPad)
    yrlabel = TextAuto(gPad, args.year, align = 31)
    func_effs = TF1("func_effs","sqrt(([0]/(x))^2 + 2*([1]^2))", x[0]-x_low[0], x[-1]+x_high[-1])

    N = 48
    C = 0.22
    #if args.year == "2018":
    #    N =  5.36645e+01
    #    C =  1.89872e-01
    func_effs.SetParameter(0, N)
    func_effs.SetParameter(1, C)
    
    eff_s_graph.Fit("func_effs","R")
    Nlabel = Text(gPad, 0.6, 0.7, "N = {:.3f} #pm {:.3f} ns".format(func_effs.GetParameter(0), func_effs.GetParError(0)))
    Clabel = Text(gPad, 0.6, 0.65,"C = {:.3f} #pm {:.3f} ns".format(func_effs.GetParameter(1), func_effs.GetParError(1)))

    c2.Update()
    c2.Modified()
    if args.show: input()




os.makedirs("plots/"+args.tag+"/"+args.year, exist_ok =True)
outFile = TFile.Open("plots/"+args.tag+"/"+args.year+"/sigma_"+name+"_"+args.sel+".root", "recreate")
outFile.cd()
graph.Write()
hfit.Write()
if(args.effs): eff_s_graph.Write()

c.SaveAs("plots/"+args.tag+"/"+args.year+"/sigma_"+name+"_"+args.sel+".png")
c.SaveAs("plots/"+args.tag+"/"+args.year+"/sigma_"+name+"_"+args.sel+".pdf")
if(args.effs):
    c2.SaveAs("plots/"+args.tag+"/"+args.year+"/effs_sigma_"+name+"_"+args.sel+".png")
    c2.SaveAs("plots/"+args.tag+"/"+args.year+"/effs_sigma_"+name+"_"+args.sel+".pdf")
