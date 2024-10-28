import ROOT
import argparse
from ROOT import TFile, TCanvas, TF1, TGraphAsymmErrors
import numpy as np
import modules.graphs as make_graphs


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



parser = argparse.ArgumentParser(description="Command line parser of plotting options")

parser.add_argument("--tag", dest="tag", help="tag root file", default=None)
parser.add_argument("--era", dest="era", help="era", default="")
parser.add_argument("--name", dest="name", help="2d histo name", default=None)
parser.add_argument("--add", dest="add", help="additional 2d histo name", default=None)
parser.add_argument(
    "--logz", dest="logz", help="log z", default=False, action="store_true"
)
parser.add_argument(
    "--show", dest="show", help="show plots", default=False, action="store_true"
)

parser.add_argument(
    "--hist", dest="hist", help="draw 2d hist", default=False, action="store_true"
)

parser.add_argument(
    "--fit", dest="fit", help="draw fit of slices", default=False, action="store_true"
)

parser.add_argument(
    "--median",
    dest="med",
    help="draw median of slices",
    default=False,
    action="store_true",
)

parser.add_argument("--zmin", dest="zmin", type=float, help="zmin", default=None)
parser.add_argument("--zmax", dest="zmax", type=float, help="zmax", default=None)


parser.add_argument("--text", dest="text", help="text", default=None)
parser.add_argument("--xlabel", dest="xlabel", help="xlabel", default=None)
parser.add_argument("--ylabel", dest="ylabel", help="ylabel", default=None)


args = parser.parse_args()


if not args.show: ROOT.gROOT.SetBatch(True)

ca = TCanvas("ca", "ca", 800, 600)
ca.Draw()


eras = ["A","B", "C", "D", ""]
labels   = ["2018A", "2018B", "2018C", "2018D", "2018ABCD"]




color = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kBlue, ROOT.kOrange]

eragraph = {}
for i, era in enumerate(eras):
    infile = TFile.Open("plots/"+args.tag+"/outPlot_2018"+era+".root")
    h2d = infile.Get(args.name)
    h2d.SetTitle("")
    if args.add:
        h2d_add = infile.Get(args.add)
        h2d.Add(h2d_add)
        del h2d_add
    if args.fit:
        graph = make_graphs.slices_fit(h2d)
    elif args.med:
        graph = make_graphs.slices_median(h2d)
    ca.cd()
    del h2d
    graph.SetName(labels[i])
    graph.SetMarkerStyle(8)
    graph.SetMarkerColor(color[i])
    graph.SetLineColor(color[i])
    
    eragraph[i] = graph


ymax = max([g.GetHistogram().GetMaximum() for g in eragraph.values()])
ymin = min([g.GetHistogram().GetMinimum() for g in eragraph.values()])


mg      = ROOT.TMultiGraph()


for k, v in eragraph.items():
    print (k, v)
    mg.Add(v)

if not args.show:
    ROOT.gROOT.SetBatch(True)


mg.GetXaxis().SetTitle(args.xlabel)
mg.GetYaxis().SetTitle(args.ylabel)
    
legend = ROOT.TLegend(0.5, 0.7, 0.89, 0.89)
legend.SetBorderSize(0)

for g in mg.GetListOfGraphs():
    print ("   ", g.GetName())
    legend.AddEntry(g, g.GetName(), "pl")
    
ROOT.gStyle.SetOptStat(0)
Frame(ROOT.gPad)



mg.Draw("ap")
mg.SetMaximum(ymax + abs(ymax*3))
mg.SetMinimum(ymin - abs(ymin/2))

    
legend.Draw("same") 
if args.text:
    text = TextAuto(ROOT.gPad, args.text, align=11)

ca.Update()
ca.Modified()
ca.SaveAs(
    "plots/"
    + args.tag
    + "/2018/"
    + args.name
    + "_fit" * args.fit
    + "_median" * args.med
    + ".pdf"
    )

ca.SaveAs(
    "plots/"
    + args.tag
    + "/2018/"
    + args.name
    + "_fit" * args.fit
    + "_median" * args.med
    + ".png"
)
