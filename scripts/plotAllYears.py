import ROOT
import argparse
import numpy as np
parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="all")
parser.add_argument('--legend', dest='legend', help='legend labels', default="all")

parser.add_argument('--norm', dest='norm', help='norm to 1', default=False, action='store_true')

parser.add_argument('--name', dest='name', help='plot name', default=None)
parser.add_argument('--xlabel', dest='xlabel', help='xlabel', default=None)
parser.add_argument('--ylabel', dest='ylabel', help='ylabel', default=None)
parser.add_argument('--zlabel', dest='zlabel', help='zlabel', default=None)


args = parser.parse_args()



year_sel = {
    "2016": [ROOT.kBlue+1,  ROOT.kAzure+2,    ROOT.kCyan, ROOT.kCyan -2],
    "2017": [ROOT.kRed + 2, ROOT.kOrange +10, ROOT.kOrange +2, ROOT.kOrange -1],
    "2018": [ROOT.kGreen+4, ROOT.kGreen+2 ,   ROOT.kSpring, ROOT.kSpring -2]
}   

ROOT.gROOT.SetBatch(True)

tag = ""
if args.tag: tag = "_"+args.tag

years = ["2016", "2017", "2018"]

selections = [item for item in args.sel.split(',')]
if args.legend:
    leg_labels = [item for item in args.legend.split(',')]
else:
    leg_labels = selections 

inFile = {} 
mg = ROOT.TMultiGraph()   
c = ROOT.TCanvas("c","c",1200, 600)
leg = ROOT.TLegend(0.11, 0.7, 0.5, 0.89)
leg.SetNColumns(3)       
plots = []
for yr in years:
    inFile[yr] = ROOT.TFile.Open("plots/"+args.tag+"/outPlot_"+yr+".root")
    #print(inFile[yr].ls())

    for i,sel in enumerate(selections):
        print(args.name+"_"+sel)
        thisPlot = inFile[yr].Get(args.name+"_"+sel)
        title = thisPlot.GetName()
        thisPlot.SetName(title+"_"+yr) 
        thisPlot.SetMarkerColor(year_sel[yr][i])
        thisPlot.SetMarkerStyle(8)
        mg.Add(thisPlot)
        plots.append(thisPlot)
        leg.AddEntry(thisPlot, leg_labels[i]+" "+yr, "p")
 

ymax = max([p.GetHistogram().GetMaximum() for p in plots])
ymin = min([p.GetHistogram().GetMinimum() for p in plots])

xmax = max([np.ndarray(len(p.GetX()), 'd', p.GetX())[-1] for p in plots])
xmin = min([np.ndarray(len(p.GetX()), 'd', p.GetX())[0] for p in plots])

c.DrawFrame(xmin,ymin-abs(ymin)/5,xmax,ymax*2)
c.SetFrameLineWidth(3)
mg.Draw("ap")
mg.SetTitle("")
if args.xlabel: mg.GetXaxis().SetTitle(args.xlabel)
if args.ylabel: mg.GetYaxis().SetTitle(args.ylabel)

leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.SetTextFont(43)

#mg.GetXaxis().SetLimits(xmin-xmin/100, xmax+xmax/100);
#mg.GetYaxis().SetLimits(ymin-abs(ymin)/5, ymax+abs(ymax)/3);
leg.Draw("same")
c.Update()


selname = ""
for i in selections:
    selname = selname+"_"+i

c.SaveAs("plots/"+args.tag+"/allYears/"+args.name+selname+".png")
c.SaveAs("plots/"+args.tag+"/allYears/"+args.name+selname+".pdf")