import ROOT


infile = ROOT.TFile.Open("plots/staggered_2021_04_08_checks/outPlot_2018.root")
ele1 = infile.Get("median_timeSeedSC1_corr_vs_ySeedSC1_Amp400_fbrem20_B1")
ele2 = infile.Get("median_timeSeedSC2_corr_vs_ySeedSC2_ele2_Amp400_ele2_fbrem20_B2")
#ele1 = infile.Get("median_timeSeedSC1_corr_vs_xSeedSC1_Amp400_fbrem20_B1")
#ele2 = infile.Get("median_timeSeedSC2_corr_vs_xSeedSC2_ele2_Amp400_ele2_fbrem20_B2")
histo = ROOT.TH1F("h", "h", 20, -0.05, 0.05)
for p in range(0, ele1.GetN()):
    diff = ele1.GetPointY(p) - ele2.GetPointY(p)
    histo.Fill(diff)

c1 = ROOT.TCanvas()
c1.Draw()
ROOT.gStyle.SetOptStat(0)
histo.SetTitle(" ; profile(e_{1}) - profile(e_{2}) [ns]; i#phi slices")
histo.Draw("hist")
c1.Update()
input()
