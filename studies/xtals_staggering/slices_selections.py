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

infile = TFile.Open("plots/"+args.tag+"/outPlot_2018.root")
if not args.show: ROOT.gROOT.SetBatch(True)

ca = TCanvas("ca", "ca", 800, 600)
ca.Draw()


selnames = ["etaplus_eminus", "etaplus_eplus", "etaminus_eplus", "etaminus_eminus"]
labels   = ["side: #eta+; charge: e-", "side: #eta+; charge: e+", "side: #eta-; charge: e+", "side: #eta-; charge: e-"]

color = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen, ROOT.kBlue]

selgraph = {}
for i, sel in enumerate(selnames):
    print(args.name.replace("XXX", sel))
    h2d = infile.Get(args.name.replace("XXX", sel))
    h2d.SetTitle("")
    if args.add:
        h2d_add = infile.Get(args.name.replace("XXX", sel))
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
    
    selgraph[sel] = graph


ymax = max([g.GetHistogram().GetMaximum() for g in selgraph.values()])
ymin = min([g.GetHistogram().GetMinimum() for g in selgraph.values()])

mg_all      = ROOT.TMultiGraph()
mg_etaplus  = ROOT.TMultiGraph()
mg_etaminus = ROOT.TMultiGraph()
mg_eplus    = ROOT.TMultiGraph()
mg_eminus   = ROOT.TMultiGraph()


for k, v in selgraph.items():
    print (k, v)
    mg_all.Add(v)
    if "etaplus" in k:
        print("---> in etaplus") 
        mg_etaplus.Add(v)
    if "etaminus" in k:
        print("---> in etaminus") 
        mg_etaminus.Add(v)
    if "eplus" in k:
        print("---> in eplus") 
        mg_eplus.Add(v)
    if "eminus" in k:
        print("---> in eminus") 
        mg_eminus.Add(v)

mgs = [mg_all, mg_etaplus, mg_etaminus, mg_eplus, mg_eminus]
mg_labels = ["all", "etaplus", "etaminus", "eplus", "eminus"]

if not args.show:
    ROOT.gROOT.SetBatch(True)


for mg, mg_label in zip(mgs, mg_labels):

    mg.GetXaxis().SetTitle(args.xlabel)
    mg.GetYaxis().SetTitle(args.ylabel)
    
    legend = ROOT.TLegend(0.5, 0.7, 0.89, 0.89)
    legend.SetBorderSize(0)
    print (mg_label)
    for g in mg.GetListOfGraphs():
        print ("   ", g.GetName())
        legend.AddEntry(g, g.GetName(), "pl")

    ROOT.gStyle.SetOptStat(0)
    Frame(ROOT.gPad)

    mg.Draw("ap")

    mg.SetMaximum(ymax*3)
    mg.SetMinimum(ymin)

    legend.Draw("same") 
    if args.text:
        text = TextAuto(ROOT.gPad, args.text, align=11)

    ca.Update()
    ca.Modified()
    ca.SaveAs(
        "plots/"
        + args.tag
        + "/2018/"
        + args.name.replace("XXX", mg_label)
        + "_fit" * args.fit
        + "_median" * args.med
        + ".pdf"
    )
    ca.SaveAs(
        "plots/"
        + args.tag
        + "/2018/"
        + args.name.replace("XXX", mg_label)
        + "_fit" * args.fit
        + "_median" * args.med
        + ".png"
    )
