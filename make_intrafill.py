import ROOT
from ROOT import gPad


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



year = '2018'
filename = "plots_sigma/2020_6_9_zoom"+year+"/outPlot_"+year+".root"
inFile = ROOT.TFile.Open(filename)

year_col = {
    "2016": ROOT.kBlue,
    "2017": ROOT.kRed,
    "2018": ROOT.kGreen,
}

plots = ["e1_seeds_vs_eventTime_B1_Run1Sel_e1_HighR9_e1_AeffLow_e1_Fill"+year,
	"e1_seeds_vs_eventTime_B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1_Fill"+year,
	"ee_vs_eventTime_BB_Run1Sel_ee_HighR9_AeffLow_ee_Fill"+year,
	"ee_vs_eventTime_BB_Run1Sel_ee_HighR9_AeffHigh_ee_Fill"+year]

ylab = ["Mean #Delta t", "#sigma_{eff} #Delta t"]
for p in plots:
	for i, var in enumerate(["mean_effA","effs_deltaT"]):
		c = ROOT.TCanvas("c","c",600, 600)
		print(var+"_"+p)
		graph = inFile.Get(var+"_"+p)
		graph.SetMarkerStyle(8)
		graph.SetMarkerColor(year_col[year])
		graph.SetTitle("")
		graph.GetYaxis().SetTitle(ylab[i])
		graph.GetXaxis().SetTitle("eventTime")
		graph.Draw("ap")
		c.SetFrameLineWidth(3)
		yrlabel = TextAuto(gPad, year, align = 31)
		c.SaveAs(var+"_"+p+".pdf")