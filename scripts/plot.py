import ROOT
import argparse
from ROOT import gPad
import pandas as pd

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

def TextAuto(gPad, text, size = 0.05, font=42, align = 13, line = 1):
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

def GetNDC(x):
  gPad.Update()
  return (x - gPad.GetX1())/(gPad.GetX2()-gPad.GetX1())


def DrawEras(gPad, year):
    df_eras = pd.read_csv("eras.dat", usecols = [0,1], names=["eras","first"], header = None, delimiter="\t")
    df_eras = df_eras[(df_eras["eras"].str.contains(year))]
    print(df_eras)

    tm = 1.-gPad.GetTopMargin();
    bm = gPad.GetBottomMargin();
    lines = []
    labels = []
    for index, row in df_eras.iterrows():
        l = ROOT.TLine()
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kGray+2)
        l.SetLineStyle(9)
        print(row['eras'], row['first'])
        l.DrawLineNDC(GetNDC(row['first']),bm,GetNDC(row['first']),tm);
        lines.append(l)
        latex = ROOT.TLatex()   
        latex.SetNDC()
        latex.SetTextAngle(90)
        latex.SetTextAlign(11)
        latex.SetTextColor(ROOT.kGray+2)
        latex.SetTextSize(0.03)
        latex.DrawLatex(GetNDC(row['first'])+0.02, 0.3*tm,row["eras"])
        labels.append(latex)
    return lines, labels


parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', dest='year', help='which year', default="all")
parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="all")
parser.add_argument('--legend', dest='legend', help='legend labels', default="all")

parser.add_argument('--norm', dest='norm', help='norm to 1', default=False, action='store_true')


parser.add_argument('--logz', dest='logz', help='log z' , default=False, action='store_true')
parser.add_argument('--show_eras', dest='show_eras', help='have markers indicating eras' , default=False, action='store_true')


parser.add_argument('--zmin', dest='zmin',type = float, help='zmin', default=None)
parser.add_argument('--zmax', dest='zmax',type = float, help='zmax', default=None)


parser.add_argument('--name', dest='name', help='plot name', default=None)
parser.add_argument('--xlabel', dest='xlabel', help='xlabel', default=None)
parser.add_argument('--ylabel', dest='ylabel', help='ylabel', default=None)
parser.add_argument('--zlabel', dest='zlabel', help='zlabel', default=None)


args = parser.parse_args()

sel_colors = [
    ROOT.kBlue+1,
    ROOT.kGreen,
    ROOT.kRed+1
    ]


#ROOT.gROOT.SetBatch(True)

tag = ""
if args.tag: tag = "_"+args.tag
if args.year == "all":
    year = ["2016", "2017", "2018"]
#else:
#     year = args.year
# for yr in year:
#     inFile = ROOT.TFile.Open("plots/outPlot_2016"+tag+".root")
#     inFile17 = ROOT.TFile.Open("plots/outPlot_2017"+tag+".root")
#     inFile18 = ROOT.TFile.Open("plots/outPlot_2018"+tag+".root")

#     h16 = inFile16.Get(args.name)
#     h17 = inFile17.Get(args.name)
#     h18 = inFile18.Get(args.name)
#     if not isinstance(h16, ROOT.TH1F):
#         print("ERROR comp is allowed for TH1F only")




    #### not yet impl

else:
    inFile = ROOT.TFile.Open("plots/"+args.tag+"/outPlot_"+args.year+".root")
    selections = [item for item in args.sel.split(',')]
    if args.legend:
        leg_labels = [item for item in args.legend.split(',')]
    else:
        leg_labels = selections
    plot = []   
    
    for sel in selections:
        print(args.name+"_"+sel)
        plot.append(inFile.Get(args.name+"_"+sel))

    if isinstance(plot[0], ROOT.TH1F):
        c = ROOT.TCanvas("c","c",600,600)
        c.SetLeftMargin(0.15)
        if args.norm: [p.Scale(1./p.Integral()) for p in plot] 
        ymax = max([p.GetMaximum() for p in plot])
        legend = ROOT.TLegend(0.65,0.7,0.89,0.89)
        for i, sel in enumerate(selections):
            plot[i].SetLineWidth(2) 
            plot[i].SetLineColor(sel_colors[i])
            if i == 0: 
                plot[i].SetMaximum(ymax + ymax/10.)
                plot[i].Draw("hist")                
                plot[i].SetTitle("")
                if args.xlabel: plot[i].GetXaxis().SetTitle(args.xlabel)
                if args.ylabel: plot[i].GetYaxis().SetTitle(args.ylabel)
            else:
                plot[i].Draw("hist same")
            if len(selections)> 1:
                legend.AddEntry(plot[i], leg_labels[i], "l")
        ROOT.gStyle.SetOptStat(0)            
        if len(selections)> 1:
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextFont(43)
            legend.Draw("same")
        Frame(gPad)
        yrlabel = TextAuto(gPad, args.year, align = 31)
        c.Update()

    elif isinstance(plot[0], ROOT.TH2F):

        h = plot[0]
        c = ROOT.TCanvas("c","c",700,600)
        c.SetLeftMargin(0.15)
        c.SetRightMargin(0.15)
        h.Draw("colz")
        h.SetTitle("")
        if args.logz: c.SetLogz(1)
        if args.xlabel: h.GetXaxis().SetTitle(args.xlabel)
        if args.ylabel: h.GetYaxis().SetTitle(args.ylabel)
        if args.zlabel: h.GetZaxis().SetTitle(args.zlabel)
        print(h.GetMinimum, h.GetMaximum)
        print(args.zmin, args.zmax)
        if args.zmin: h.SetMinimum(args.zmin)
        if args.zmax: h.SetMaximum(args.zmax)

        ROOT.gStyle.SetOptStat(0)
        Frame(gPad)
        yrlabel = TextAuto(gPad, args.year, align = 31)
        c.Update()

    elif isinstance(plot[0], ROOT.TGraph):
        
        c = ROOT.TCanvas("c","c",800, 600)
        c.SetLeftMargin(0.15)
        if len(selections) == 1:
            gr = plot[0]
            gr.Draw("ap")
            gr.SetTitle("")
            gr.SetMarkerStyle(8)
            gr.SetMarkerColor(ROOT.kBlue+1)
            if args.xlabel: gr.GetXaxis().SetTitle(args.xlabel)
            if args.ylabel: gr.GetYaxis().SetTitle(args.ylabel)
        else:
            legend = ROOT.TLegend(0.65,0.7,0.89,0.89)
            mg = ROOT.TMultiGraph()
            for i, sel in enumerate(selections):
                plot[i].SetMarkerStyle(8) 
                plot[i].SetLineColor(sel_colors[i])
                plot[i].SetMarkerColor(sel_colors[i])
                mg.Add(plot[i])
                legend.AddEntry(plot[i], leg_labels[i], "p")

            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextFont(43)
            mg.Draw("ap")
            if args.xlabel: mg.GetXaxis().SetTitle(args.xlabel)
            if args.ylabel: mg.GetYaxis().SetTitle(args.ylabel)
            legend.Draw("same")
        Frame(gPad) 
        if args.show_eras: runlines, runlabels = DrawEras(gPad, args.year)
        yrlabel = TextAuto(gPad, args.year, align = 31)
        c.Update()
        input()

    selname = ""
    for i in selections:
        selname = selname+"_"+i

    c.SaveAs("plots/"+args.tag+"/"+args.year+"/"+args.name+selname+".png")
    c.SaveAs("plots/"+args.tag+"/"+args.year+"/"+args.name+selname+".pdf")