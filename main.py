import numpy as np
import modules.load_data as load_data
import modules.config_reader as config_reader
import modules.selections as select
import modules.get_ids as get_ids
import modules.compute_variables as compute
from modules.plot import *
import uproot_methods
import argparse

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


import pandas as pd

import ROOT
import datetime
import os, sys

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', type = int, dest='year', help='which year', default=2016)
parser.add_argument('--tag', dest='tag', help='tag for plot', default=None)
parser.add_argument('--cfg', dest='cfg', help='cfg file', default=None)
parser.add_argument('--debug', dest='debug', help='debug', default=False, action ='store_true')

args = parser.parse_args()

year = args.year 
fileList = "filelists/ECALELF_Run2UL/Data_UL2016.log"
fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2016_extra.log"
if year ==2017: 
    fileList = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017_extra.log"
if year ==2018: 
    fileList = "filelists/ECALELF_Run2UL/Data_UL2018.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2018_extra.log"


files = [line. rstrip('\n') for line in open(fileList)]
files_extra = [line. rstrip('\n') for line in open(fileList_extra)]


debug = args.debug

if debug:
    files = files[-1:] #files[:1]
    files_extra = files_extra[:1]

### ECALELF content:
#['runNumber', 'lumiBlock', 'eventNumber', 'eventTime', 'nBX', 'isTrain', 'mcGenWeight', 'HLTfire', 
#'rho', 'nPV', 'nPU', 'vtxX', 'vtxY', 'vtxZ', 
#'eleID', 'chargeEle', 'recoFlagsEle', 'etaEle', 'phiEle', 'fremEle', 'R9Ele', 
#'gsfTrackLengthFromVtxP', 'gsfTrackLengthFromTangents', 'etaSCEle', 'phiSCEle', 'nHitsSCEle', 
#'avgLCSC', 'rawEnergySCEle', 'mustEnergySCEle', 'energy_ECAL_ele', 'energy_ECAL_pho', 
#'energyUncertainty_ECAL_ele', 'energyUncertainty_ECAL_pho', 
#'energy_5x5SC', 'pModeGsfEle', 'pAtVtxGsfEle', 'pNormalizedChi2Ele', 'trackMomentumErrorEle', 
#'xSeedSC', 'ySeedSC', 'eeRingNoSeedSC', 'gainSeedSC', 
#'energySeedSC', 'energySecondToSeedSC', 'amplitudeSeedSC', 'amplitudeSecondToSeedSC', 
#'timeSeedSC', 'timeSecondToSeedSC', 'icSeedSC', 'laserSeedSC', 'alphaSeedSC', 
#'pedestalSeedSC', 'noiseSeedSC', 'esEnergySCEle', 'esEnergyPlane2SCEle', 'esEnergyPlane1SCEle', 
#'rawESEnergyPlane2SCEle', 'rawESEnergyPlane1SCEle', 'etaMCEle', 'phiMCEle', 'energyMCEle', 
#'invMass_MC', 'ZEvent', 'invMass', 'invMass_ECAL_ele', 'invMass_ECAL_pho', 'invMass_5x5SC', 
#'invMass_rawSC', 'invMass_rawSC_esSC', 'invMass_highEta', 'ele1E', 'ele2E', 'ele1ecalE', 'ele2ecalE', 'angleEle12']



branches = ['runNumber','etaSCEle','phiSCEle',
            'xSeedSC','ySeedSC',
            'nPV','nBX', 'vtxX', 'vtxZ','vtxY',
            'fbremEle', 'R9Ele', 'ZEvent','eleID', 
            'timeSeedSC','timeSecondToSeedSC','amplitudeSeedSC', 'amplitudeSecondToSeedSC',
            'rawEnergySCEle',
            'noiseSeedSC', 
            'laserSeedSC','alphaSeedSC', 'chargeEle', 'invMass', 'gainSeedSC']

branches_extra = ['XRecHitSCEle1','XRecHitSCEle2',
                  'YRecHitSCEle1','YRecHitSCEle2',
                  'ZRecHitSCEle1','ZRecHitSCEle2']



df_original= load_data.load_chain(files, "selected", branches)
#df_extra= load_data.load_chain(files_extra, "extraCalibTree", branches_extra, firsthit = True) # taking only X, Y, Z of first hit
#df_chain = pd.concat([df_original, df_extra], axis=1) 
df_chain = df_original
print("entries = %d" % df_chain.shape[0])

#flat columns
branches_split = ["chargeEle","etaSCEle", "phiSCEle","xSeedSC", "ySeedSC", "amplitudeSeedSC","energySeedSC", "energySecondToSeedSC", "amplitudeSecondToSeedSC","R9Ele"]
for br in branches_split:
    if br+"[1]" in df_chain:
        df_chain[[br+'1', br+'2']] = df_chain[[br+'[0]',br+'[1]']]


df_chain['deltaT_ee'] = df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]']

df_chain['deltaEta_ee'] = df_chain['etaSCEle1']-df_chain['etaSCEle1']
df_chain['deltaPhi_ee'] = compute.delta_phi(df_chain['phiSCEle1'], df_chain['phiSCEle2'])
df_chain['deltaT_e1_seeds'] = df_chain['timeSeedSC[0]']-df_chain['timeSecondToSeedSC[0]']
#df_chain['deltaT_e1_seeds'] = df_chain['deltaT_e1_seeds'].div(np.sqrt(2))

df_chain['deltaT_e2_seeds'] = df_chain['timeSeedSC[1]']-df_chain['timeSecondToSeedSC[1]']

df_chain['deltaA_e1_seeds'] = df_chain['amplitudeSeedSC[0]']-df_chain['amplitudeSecondToSeedSC[0]']
df_chain['deltaA_e2_seeds'] = df_chain['amplitudeSeedSC[1]']-df_chain['amplitudeSecondToSeedSC[1]']


df_chain['effA_ee'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[0]'],
                                                        1.5,
                                                        df_chain['amplitudeSeedSC[1]'],
                                                        1.5)

df_chain['effA_e1_seeds'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[0]'],
                                                        1.5,
                                                        df_chain['amplitudeSecondToSeedSC[0]'],
                                                        1.5)

df_chain['effA_e2_seeds'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[1]'],
                                                        1.5,
                                                        df_chain['amplitudeSecondToSeedSC[1]'],
                                                        1.5)
#df_chain['responseSeedSC1'] = compute.relative_response(df_chain['laserSeedSC[0]'],df_chain['alphaSeedSC[0]'])
#df_chain['responseSeedSC2'] = compute.relative_response(df_chain['laserSeedSC[1]'],df_chain['alphaSeedSC[1]'])

df_chain = get_ids.appendIdxs(df_chain, "1")
df_chain = get_ids.appendIdxs(df_chain, "2")


tag = ""
if args.tag:
    tag = args.tag
    os.makedirs("plots/"+str(tag), exist_ok = True)

outFile = ROOT.TFile.Open("plots/"+str(tag)+"/outPlot_"+str(year)+".root","RECREATE")

config = config_reader.cfg_reader(args.cfg)

hvarList  = config.readListOption("general::hvariables")
hvar2DList  = config.readListOption("general::hvariables2D")
grList  = config.readListOption("general::grvariables")
mapList  = config.readListOption("general::mvariables")

toPlot = []
if hvarList:
    for hvar in hvarList:
        toPlot.append(hvar)
if hvar2DList:
    for hvars in hvar2DList:
        hvarx, hvary, name = hvars.split(':')
        toPlot.append(hvarx)
        toPlot.append(hvary)
if grList:
    for grvar in grList:
        gvarx, gvary = grvar.split(':')
        toPlot.append(gvarx)
        toPlot.append(gvary)
if mapList:
    for mvars in mapList:
        mvarx, mvary, mvarz = mvars.split(':')
        toPlot.append(mvarx)
        toPlot.append(mvary)    

for var in toPlot:
    if not var in df_chain:
        print("### ERROR: missing variable: "+ var)
        sys.exit()

if config.hasOption("general::hvariables"):
    for hvar in hvarList:
        binning = []
        if not hvar in config.config['binning']: 
            print("### WARNING: no binning provided for ", hvar, ", using dummy")
        else:
            binning = [float(s) for s in config.config['binning'][hvar].split(",")]
            binning[0] = int(binning[0])
        if hvar in config.config["hselections"]: 
            hselections = config.readOption("hselections::"+hvar).split(",")
        else:
            hselections = ["all"]
        for hselection in hselections:
            hselection = hselection.strip()
            df_this = select.apply_selection(df_chain,hselection)
            if len(binning) > 0:
                plot = plt.hist(df_this[hvar], binning[0], range = binning[-2:])
            else: 
                plot = plt.hist(df_this[hvar])
            plot_root = plt_to_TH1(plot, hvar+'_'+hselection.replace('-',"_"))
            plot_root.Write()
            plt.close()
            if hvar in config.config['hoptions']:
                if "outliers" in config.config['hoptions'][hvar]:
                    if len(binning) > 0:
                        plot_outliers = outlier_aware_hist(df_chain[hvar], binning[0], binning[-2:])
                        plot_root = plt_to_TH1(plot_outliers, hvar+'_'+hselection.replace('-',"_")+'_outliers')
                        plot_root.Write()   
                    else: 
                        print("### WARNING: no binning provided for ", hvar, ", skipping underflow/overflow histogram")
            del df_this

if config.hasOption("general::hvariables2D"):
    for hvars in hvar2DList:
        hvarx, hvary, name = hvars.split(':')
        if not "X@"+name in config.config['binning2D']: 
            print("### WARNING: no x binning provided for ", name, ", skipping")
            continue
        if not "Y@"+name in config.config['binning2D']: 
            print("### WARNING: no y binning provided for ", name, ", skipping")
            continue
        xbinning = [float(s) for s in config.config['binning2D']["X@"+name].split(",")]
        ybinning = [float(s) for s in config.config['binning2D']["Y@"+name].split(",")]
        xbinning[0] = int(xbinning[0])
        ybinning[0] = int(ybinning[0])
        xcustom = False
        ycustom = False
        if "X@"+name in config.config['custom_binning2D']: 
            xcustom = True
            xbinning = [float(s) for s in config.config['custom_binning2D']["X@"+name].split(",")]
        if "Y@"+name in config.config['custom_binning2D']: 
            ycustom = True
            ybinning = [float(s) for s in config.config['custom_binning2D']["Y@"+name].split(",")]
        if name in config.config["hselections2D"]: 
            hselections = config.readOption("hselections2D::"+name).split(",")
        else:
            hselections = ["all"]
        for hselection in hselections:
            hselection = hselection.strip()    
            df_this = select.apply_selection(df_chain, hselection)
            if xcustom:
                if ycustom :
                    plot = plt.hist2d(df_this[hvarx], df_this[hvary], bins = [xbinning,ybinning])
                else:
                    plot = plt.hist2d(df_this[hvarx], df_this[hvary], bins = [xbinning,ybinning[0]], range = [[xbinning[0], xbinning[-1]], ybinning[-2:]])
            else:
                if ycustom:
                    plot = plt.hist2d(df_this[hvarx], df_this[hvary], bins = [xbinning[0],ybinning], range = [xbinning[-2:], [ybinning[0], ybinning[-1]]])
                else:
                    plot = plt.hist2d(df_this[hvarx], df_this[hvary], bins = [xbinning[0],ybinning[0]], range = [xbinning[-2:], ybinning[-2:]])
            del df_this

            plot_root = plt_to_TH2(plot, name+'_'+hselection.replace('-',"_"))
            plot_root.Write()
            plt.close()


if config.hasOption("general::grvariables"):
    for grvar in grList:
        if grvar in config.config["grselections"]: 
            grselections = config.readOption("grselections::"+grvar).split(",")
        else:
            grselections = ["all"]
        xvar , yvar = grvar.split(":")
        for grselection in grselections:
            grselection = grselection.strip()
            df_this = select.apply_selection(df_chain,grselection)
            if grvar in config.config["groptions"]:
                gropts = config.readOption("groptions::"+grvar).split(",")
                custom_binning = False
                binning = []
                mid = []
                if grvar in config.config["grmarkerwidth"]: 
                    custom_binning = True
                    cfg_binning = config.readOption("grmarkerwidth::"+grvar).split(",")
                    if len(cfg_binning) == 3:
                        bins, xmin, xmax = cfg_binning
                        xmin = float(xmin.strip())
                        xmax = float(xmax.strip())
                        bins = float(bins.strip())
                        width = (xmax-xmin)/bins
                        binning = np.arange(xmin, xmax+float(width), float(width))
                    else:
                        binning = np.asarray(cfg_binning, dtype=np.float32)
                for opt in gropts:
                    opt = opt.strip()
                    if "aggr" in opt:
                        aggr_var = opt.split(":")
                        aggr_var = aggr_var[1:]
                        if not custom_binning:
                            graph = df_this.groupby(xvar)[yvar]
                            aggr_graph = graph.agg(aggr_var)
                        else: 
                            mid = (binning[1:] + binning[:-1]) / 2
                            graph = df_this.groupby(pd.cut(df_this[xvar], binning))[yvar]
                        if hasattr(compute, aggr_var[0]):
                            aggr_graph = graph.agg(getattr(compute, aggr_var[0]))
                        elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var[0]):
                            aggr_graph = getattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var[0])(graph)
                        else:
                            print("### WARNING: ", aggr_var[0], " not defined, skipping")
                            continue
                        name = yvar+'_vs_'+xvar
                        for i in aggr_var:
                            aggr_name = i+"_"
                        name = aggr_name + name
                        plot = aggr_graph.plot()
                        plot = plt_to_TGraph(plot,name+"_"+grselection.replace('-',"_"), mid, binning)
                        plt.close()
                        plot.Write()
                    else:
                        plot = df_chain.plot(xvar,yvar)
                        plot = plt_to_TGraph(plot,name)  
                        plt.close()
                        plot.Write()
            del df_this

if config.hasOption("general::mvariables"):
    for mvars in mapList:
        mvarx, mvary, mvarz = mvars.split(':')
        if mvars in config.config["mselections"]: 
            mselections = config.readOption("mselections::"+mvars).split(",")
        else:
            mselections = ["all"]
        for mselection in mselections:
            mselection = mselection.strip()    
            df_this = select.apply_selection(df_chain, mselection)
            if mvars in config.config["moptions"]:
                mopts = config.readOption("moptions::"+mvars).split(",")
                for opt in mopts:
                    opt = opt.strip()
                    if "aggr" in opt:                        
                        aggr_var = opt.split(":")
                        aggr_var = aggr_var[1:]
                        name = mvary+'_vs_'+mvarx
                        name = aggr_var[0] + '_'+ mvarz +"_"+ name
                        table = pd.pivot_table(df_this, index=mvary, columns=mvarx, values=mvarz, aggfunc=getattr(np, aggr_var[0]))
                        table.dropna()
                        table.dropna(axis=1)
                        #print(table)
                        plot_root = table_to_TH2(table, name +'_'+mselection.replace('-',"_"))
                        plot_root.Write()
            del df_this

outFile.Close()



