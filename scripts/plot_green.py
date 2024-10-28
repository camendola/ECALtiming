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

def DrawHw(gPad, year):
    df_hw = pd.read_csv("data/hw_changes.dat", names=["time","run"], header = None, delimiter="\t")
    df_hw = df_hw[(df_hw["time"].str.contains(year))]
    print(df_hw)
    lm = gPad.GetLeftMargin();
    tm = 1.-gPad.GetTopMargin();
    bm = gPad.GetBottomMargin();
    lines = []
    for index, row in df_hw.iterrows():
        l = ROOT.TLine()
        l.SetLineWidth(2)
        l.SetLineColor(ROOT.kRed+1)
        l.SetLineStyle(8)
        print(row['run'])
        start = GetNDC(row['run'])
        if (GetNDC(row['run']) < lm): start = lm
        l.DrawLineNDC(start,bm,start,tm);
        lines.append(l)
        #latex.DrawLatex(GetNDC(row['first'])+0.02, 0.3*tm,row["eras"])
    return lines

def DrawEras(gPad, year):
    df_eras = pd.read_csv("data/eras.dat", usecols = [0,1], names=["eras","first"], header = None, delimiter="\t")
    df_eras = df_eras[(df_eras["eras"].str.contains(year))]
    print(df_eras)
    lm = gPad.GetLeftMargin();
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
        start = GetNDC(row['first'])
        if (GetNDC(row['first']) < lm): start = lm
        l.DrawLineNDC(start,bm,start,tm);
        lines.append(l)
        latex = ROOT.TLatex()   
        latex.SetNDC()
        latex.SetTextAngle(90)
        latex.SetTextAlign(11)
        latex.SetTextColor(ROOT.kGray+2)
        latex.SetTextSize(0.03)
        #latex.DrawLatex(GetNDC(row['first'])+0.02, 0.3*tm,row["eras"])
        latex.DrawLatex(start+0.02, 0.8*tm,row["eras"])
        labels.append(latex)
    return lines, labels


parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', dest='year', help='which year', default="2018")
parser.add_argument('--era', dest='era', help='which era', default="")
parser.add_argument('--tag', dest='tag', help='tag root file', default=None)
parser.add_argument('--sel', dest='sel', help='selection(s)', default="all")
parser.add_argument('--legend', dest='legend', help='legend labels', default="all")

parser.add_argument('--norm', dest='norm', help='norm to 1', default=False, action='store_true')


parser.add_argument('--logz', dest='logz', help='log z' , default=False, action='store_true')
parser.add_argument('--showeras', dest='showeras', help='have markers indicating eras' , default=False, action='store_true')
parser.add_argument('--showhw',   dest='showhw', help='have markers indicating hw changes' , default=False, action='store_true')
parser.add_argument('--show', dest='show', help='show plots' , default=False, action='store_true')


parser.add_argument('--zmin', dest='zmin',type = float, help='zmin', default=None)
parser.add_argument('--zmax', dest='zmax',type = float, help='zmax', default=None)


parser.add_argument('--name', dest='name', help='plot name(s)', default=None)
parser.add_argument('--xlabel', dest='xlabel', help='xlabel', default=None)
parser.add_argument('--ylabel', dest='ylabel', help='ylabel', default=None)
parser.add_argument('--zlabel', dest='zlabel', help='zlabel', default=None)


args = parser.parse_args()

sel_colors = [
    ROOT.kBlack,
    ROOT.kBlue,
    ROOT.kSpring, 
    ]

#sel_colors = [
#    ROOT.kBlue+1,
#    ROOT.kGreen,
#    ROOT.kRed+1
#    ]


if not args.show: ROOT.gROOT.SetBatch(True)

tag = ""
if args.tag: tag = "_"+args.tag

inFile = ROOT.TFile.Open("plots/"+args.tag+"/outPlot_"+args.year+args.era+".root")
inFile_green = ROOT.TFile.Open("plots/2021_3_16_laser_g_ref316995/outPlot_"+args.year+args.era+".root")
selections = [item for item in args.sel.split(',')]
varnames = [item for item in args.name.split(',')]
if args.legend:
    leg_labels = [item for item in args.legend.split(',')]
else:
    leg_labels = selections
plot = []   


for sel in selections:
    for name in varnames:
        print(name+"_"+sel)
        plot.append(inFile.Get(name+"_"+sel))
        if "recal" in name or "laser" in name: (plot.append(inFile_green.Get(name+"_"+sel)))
print (plot)

if isinstance(plot[0], ROOT.TH1F):
    c = ROOT.TCanvas("c","c",600,600)
    c.SetLeftMargin(0.15)
    if args.norm: [p.Scale(1./p.Integral()) for p in plot] 
    ymax = max([p.GetMaximum() for p in plot])
    legend = ROOT.TLegend(0.55,0.7,0.89,0.89)
    for i, p in enumerate(plot):
        p.SetLineWidth(2) 
        p.SetLineColor(sel_colors[i])
        if i == 0: 
            p.SetMaximum(ymax + ymax/5.)
            p.Draw("hist")                
            p.SetTitle("")
            if args.xlabel: p.GetXaxis().SetTitle(args.xlabel)
            if args.ylabel: p.GetYaxis().SetTitle(args.ylabel)
        else:
            p.Draw("hist same")
        if len(plot)> 1:
            legend.AddEntry(p, leg_labels[i], "l")
    ROOT.gStyle.SetOptStat(0)            
    if len(plot)> 1:
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextFont(43)
        legend.Draw("same")
    Frame(gPad)
    yrlabel = TextAuto(gPad, args.year+args.era, align = 31)
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
    yrlabel = TextAuto(gPad, args.year+args.era, align = 31)
    c.Update()

elif isinstance(plot[0], ROOT.TGraph):
    
    c = ROOT.TCanvas("c","c",800, 600)
    c.SetLeftMargin(0.15)
    if len(plot) == 1:
        gr = plot[0]
        gr.Draw("ap")
        gr.SetTitle("")
        gr.SetMarkerStyle(8)
        gr.SetMarkerColor(ROOT.kBlue)
        gr.SetMaximum(0.8)
        gr.SetMinimum(0.1)
        if args.xlabel: gr.GetXaxis().SetTitle(args.xlabel)
        if args.ylabel: gr.GetYaxis().SetTitle(args.ylabel)
        if args.showeras: runlines, runlabels = DrawEras(gPad, args.year)
        if args.showhw:   runlines = DrawHw(gPad, args.year)
    else:
        ymax = max([p.GetHistogram().GetMaximum() for p in plot])
        print ("---->", ymax)
        
        legend = ROOT.TLegend(0.65,0.7,0.89,0.89)
        mg = ROOT.TMultiGraph()

        for i, p in enumerate(plot):
            #toremove = []
            #for point in range(1,p.GetN()):
            #    if p.GetPointY(point) > 1.2:
            #        toremove.append(point)
            #print (toremove)
            #sub = 0
            #for point in toremove:
            #    #p.Print()
            #    p.RemovePoint(point - sub)
            #    sub = sub + 1
            #
            #for point in range(1,p.GetN()):
            #    if p.GetPointY(point) > 1.2: print(p.GetPointY(point))

            p.SetMarkerStyle(8) 
            p.SetLineColor(sel_colors[i])
            p.SetMarkerColor(sel_colors[i])
            #p.SetMaximum(1.2)
            #p.SetMinimum(0.1)
            mg.Add(p)
            legend.AddEntry(p, leg_labels[i], "p")
            
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        legend.SetTextFont(43)
        #mg.SetMaximum(1.2)
        #mg.SetMinimum(0.1)
        mg.Draw("ap")

        gPad.Modified()
        gPad.Update();
        if args.xlabel: mg.GetXaxis().SetTitle(args.xlabel)
        if args.ylabel: mg.GetYaxis().SetTitle(args.ylabel)
        if args.showeras: runlines, runlabels = DrawEras(gPad, args.year)
        if args.showhw:   runlines = DrawHw(gPad, args.year)
        legend.Draw("same")
    Frame(gPad) 

    yrlabel = TextAuto(gPad, args.year+args.era, align = 31)
    c.Update()


selname = ""
for i in selections:
    selname = selname+"_"+i

plotname = ""
for i in varnames:
    plotname = plotname+"_"+i

if plotname.startswith("_"): plotname = plotname[1:]
if selname.startswith("_"):  selname = selname[1:]

c.SaveAs("plots/"+args.tag+"/"+args.year+args.era+"/"+plotname+"_"+selname+"_green.png")
c.SaveAs("plots/"+args.tag+"/"+args.year+args.era+"/"+plotname+"_"+selname+"_green.pdf")
