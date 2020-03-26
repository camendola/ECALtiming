import ROOT
import argparse

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', dest='year', help='which year', default="comp")
parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="all")

parser.add_argument('--norm', dest='norm', help='norm to 1', default=False, action='store_true')

parser.add_argument('--name', dest='name', help='plot name', default=None)
parser.add_argument('--xlabel', dest='xlabel', help='xlabel', default=None)
parser.add_argument('--ylabel', dest='ylabel', help='xlabel', default=None)


args = parser.parse_args()

sel_colors = {
    "all": ROOT.kBlue+1,
    "EE": ROOT.kBlack,
    "BB": ROOT.kGreen+1,
    "EB": ROOT.kRed+1
    }

sel_year = {
    "2016": ROOT.kBlue+1,
    "2017": ROOT.kGreen+2,
    "2018": ROOT.kMagenta+2
    }   

ROOT.gROOT.SetBatch(True)

tag = ""
if args.tag: tag = "_"+args.tag
if args.year == "comp":
    inFile16 = ROOT.TFile.Open("plots/outPlot_2016"+tag+".root")
    inFile17 = ROOT.TFile.Open("plots/outPlot_2017"+tag+".root")
    inFile18 = ROOT.TFile.Open("plots/outPlot_2018"+tag+".root")

    h16 = inFile16.Get(args.name)
    h17 = inFile17.Get(args.name)
    h18 = inFile18.Get(args.name)
    if not isinstance(h16, ROOT.TH1F):
        print("ERROR comp is allowed for TH1F only")

    colors = [kBlue, kRed, kGreen]
    name = ["2016", "2017", "2018"]

    #### not yet impl

else:
    inFile = ROOT.TFile.Open("plots/outPlot_"+args.year+tag+".root")
    selections = [item for item in args.sel.split(',')]
    plot = []   
    
    for sel in selections:
        print(args.name+"_"+sel)
        plot.append(inFile.Get(args.name+"_"+sel))

    if isinstance(plot[0], ROOT.TH1F):
        c = ROOT.TCanvas("c","c",600,600)
        c.SetLeftMargin(0.15)
        if args.norm: [p.Scale(1./p.Integral()) for p in plot] 
        ymax = max([p.GetMaximum() for p in plot])
        legend = ROOT.TLegend(0.7,0.7,0.89,0.89)
        for i, sel in enumerate(selections):
            plot[i].SetLineWidth(2)
            plot[i].SetLineColor(sel_colors[sel])
            if i == 0: 
                plot[i].SetMaximum(ymax + ymax/10.)
                plot[i].Draw("hist")                
                plot[i].SetTitle("")
                if args.xlabel: plot[i].GetXaxis().SetTitle(args.xlabel)
                if args.ylabel: plot[i].GetYaxis().SetTitle(args.ylabel)
            else:
                plot[i].Draw("hist same")
            if len(selections)> 1:
                legend.AddEntry(plot[i], sel, "l")
        ROOT.gStyle.SetOptStat(0)            
        if len(selections)> 1:
            legend.Draw("same")
        c.Update()

    elif isinstance(plot[0], ROOT.TH2F):

        h = plot[0]
        c = ROOT.TCanvas("c","c",700,600)
        c.SetLeftMargin(0.15)
        c.SetRightMargin(0.15)
        h.Draw("colz")
        h.SetTitle("")

        if args.xlabel: h.GetXaxis().SetTitle(args.xlabel)
        if args.ylabel: h.GetYaxis().SetTitle(args.ylabel)
        ROOT.gStyle.SetOptStat(0)
        c.Update()

    elif isinstance(plot[0], ROOT.TGraph):
        gr = plot[0]
        c = ROOT.TCanvas("c","c",800, 600)
        c.SetLeftMargin(0.15)
        gr.Draw("ap")
        gr.SetTitle("")
        gr.SetMarkerStyle(8)
        gr.SetMarkerColor(ROOT.kBlue+1)
        if args.xlabel: gr.GetXaxis().SetTitle(args.xlabel)
        if args.ylabel: gr.GetYaxis().SetTitle(args.ylabel)

        c.Update()

    selname = ""
    for i in selections:
        selname = selname+"_"+i

    c.SaveAs("plots/2020_03_25_"+args.year+"_test/"+args.name+selname+".png")
    c.SaveAs("plots/2020_03_25_"+args.year+"_test/"+args.name+selname+".pdf")