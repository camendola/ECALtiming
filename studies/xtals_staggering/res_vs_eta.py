import ROOT
from ROOT import TFile, TCanvas

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



infile = TFile.Open("plots/staggered_2021_03_15/outPlot_2018.root")

ca = TCanvas("ca", "ca", 600,600)
ca.Draw()
var = "timeSeedSC1_corr"
sel = ["B1", "EtaLt0p4", "EtaGt0p4Lt0p8", "EtaGt0p8Lt1p4"]
label = ["|#eta|<1.4", "|#eta|<0.4", "0.4<|#eta|<0.8", "0.8<|#eta|<1.4"]
color = [ROOT.kBlack,ROOT.kRed, ROOT.kGreen, ROOT.kBlue]
norm = True
hist = [infile.Get(var+"_"+s) for s in sel]
if norm: 
    for h in hist:  h.Scale(1./h.Integral())

print (hist)
ymax = max([h.GetMaximum() for h in hist])
leg = ROOT.TLegend (0.3, 0.7, 0.89,0.89)
i = 0
for l, c, h in zip(label, color, hist):
    print (l, c)
    h.SetLineColor(c)
    #if not s == "B1":
    #    h.SetLineStyle(2)
    h.SetLineWidth(2)
    h.SetLineColor(c)
    ca.cd()
    if not i == 0:
        h.Draw("same hist")
    else:
        h.SetTitle("")
        ROOT.gStyle.SetOptStat(0)
        h.SetMaximum(ymax+ymax/2)
        h.Draw("hist")
        h.GetXaxis().SetTitle("e arrival time [ns]")
        h.GetYaxis().SetTitle("a.u." if norm else "Events")
    l = l + " - mean = {:.2f} ns, RMS = {:.2f} ns".format(h.GetMean(), h.GetRMS())
    leg.AddEntry(h, l, "l")
    i += 1

leg.Draw("same")
ca.Update()
ca.Modified()

Frame(ROOT.gPad)

input()
    
    

    
    

