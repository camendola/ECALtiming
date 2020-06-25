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


import modules.classes as obj

import pandas as pd

import gc
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

print("*** Processing year "+str(args.year))

### ECALELF original content:
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
            'xSeedSC','ySeedSC','etaEle','vtxZ',
            'R9Ele', 
            'timeSeedSC','timeSecondToSeedSC','amplitudeSeedSC', 'amplitudeSecondToSeedSC',
            'energySeedSC', 'energySecondToSeedSC', 'noiseSeedSC',
            'invMass','ele1E', 'ele2E']
branches_extra = ['noiseSeedSC1_GT', 'noiseSeedSC2_GT', 'runNumber', 'noiseSecondToSeedSC1_GT','iTTSeedSC1', 'scSeedSC1','iTTSecondToSeedSC1', 'scSecondToSeedSC1',]

#df_chain = load_data.load_chain(files, "selected", branches, suffix = "extra", other_tree_name = "extended", other_branch = branches_extra)
df_chain = load_data.load_chain(files, "selected", branches)
#df_extra = load_data.load_chain(files, "extended", branches_extra, suffix = "extra") # taking only X, Y, Z of first hit
#df_chain = pd.concat([df_original.set_index('runNumber'), df_extra.set_index('runNumber')], axis=1, join = 'inner').reset_index()
#df_chain = df_original
print(df_chain.keys())
print("entries = %d" % df_chain.shape[0])

#flat columns
branches_split = ["timeSeedSC","timeSecondToSeedSC","chargeEle","etaSCEle", "phiSCEle","xSeedSC", "ySeedSC", "amplitudeSeedSC","energySeedSC", "energySecondToSeedSC", "amplitudeSecondToSeedSC","R9Ele","etaEle","noiseSeedSC"]
for br in branches_split:
    if br+"[1]" in df_chain:
        df_chain[[br+'1', br+'2']] = df_chain[[br+'[0]',br+'[1]']]
        df_chaih = df_chain.drop(columns=[br+'[0]',br+'[1]',br+'[2]'])

df_chain['deltaT_ee'] = df_chain['timeSeedSC1']-df_chain['timeSeedSC2']

df_chain['deltaEta_ee'] = df_chain['etaSCEle1']-df_chain['etaSCEle1']
df_chain['deltaPhi_ee'] = compute.delta_phi(df_chain['phiSCEle1'], df_chain['phiSCEle2'])
df_chain['deltaT_e1'] = df_chain['timeSeedSC1']-df_chain['timeSecondToSeedSC1']

df_chain['deltaA_e1'] = df_chain['amplitudeSeedSC1']-df_chain['amplitudeSecondToSeedSC1']
df_chain['deltaA_e2'] = df_chain['amplitudeSeedSC2']-df_chain['amplitudeSecondToSeedSC2']


df_chain['effA_ee'] = compute.effective_amplitude(df_chain['amplitudeSeedSC1'],
                                                        df_chain['noiseSeedSC1'],
                                                        df_chain['amplitudeSeedSC2'],
                                                        df_chain['noiseSeedSC2'])

df_chain['effA_e1'] = compute.effective_amplitude(df_chain['amplitudeSeedSC1'],
                                                        df_chain['noiseSeedSC1'],
                                                        df_chain['amplitudeSecondToSeedSC1'],
                                                        df_chain['noiseSeedSC1'])
#
#df_chain['effA_e2'] = compute.effective_amplitude(df_chain['amplitudeSeedSC2'],
#                                                        df_chain['noiseSeedSC2'],
#                                                        df_chain['amplitudeSecondToSeedSC2'],
#                                                        df_chain['noiseSeedSC2'])

df_chain['timeSeedSC1_corr'] = compute.corr_time(df_chain['vtxZ'], df_chain['etaEle1'], df_chain['timeSeedSC1'])
df_chain['timeSeedSC2_corr'] = compute.corr_time(df_chain['vtxZ'], df_chain['etaEle2'], df_chain['timeSeedSC2'])
df_chain['timeSecondToSeedSC1_corr'] = compute.corr_time(df_chain['vtxZ'], df_chain['etaEle1'], df_chain['timeSecondToSeedSC1'])
df_chain['timeSecondToSeedSC2_corr'] = compute.corr_time(df_chain['vtxZ'], df_chain['etaEle2'], df_chain['timeSecondToSeedSC2'])

df_chain['deltaT_ee_corr'] = df_chain['timeSeedSC1_corr']-df_chain['timeSeedSC2_corr']
df_chain['deltaT_e1_corr'] = df_chain['timeSeedSC1_corr']-df_chain['timeSecondToSeedSC1_corr']


#df = get_ids.appendIdxs(df, "1")
#df = get_ids.appendIdxs(df, "2")

#df_chain['transparencySeedSC1'] = compute.relative_response(df_chain['laserSeedSC[0]'],df_chain['alphaSeedSC[0]'])
#df_chain['transparencySeedSC2'] = compute.relative_response(df_chain['laserSeedSC[1]'],df_chain['alphaSeedSC[1]'])


tag = ""
if args.tag:
    tag = args.tag
    os.makedirs("plots/"+str(tag), exist_ok = True)

outFile = ROOT.TFile.Open("plots/"+str(tag)+"/outPlot_"+str(year)+".root","RECREATE")
config = config_reader.cfg_reader(args.cfg)

hvarList    = config.readListOption("general::hvariables")
hvar2DList  = config.readListOption("general::hvariables2D")
grList      = config.readListOption("general::grvariables")
mapList     = config.readListOption("general::mvariables")

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
        toPlot.append(mvarz)

for var in toPlot:
    if not var in df_chain:
        print("### ERROR: missing variable: "+ var)
        sys.exit()

### 1D histograms
if hvarList:
    for hvar in hvarList:
        h = obj.histo1D(hvar,config)
        for s in h.selections: 
            s_name = h.var+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)
            plot_root = plt_to_TH1(h.plot(df_this), s_name)
            plot_root.Write()
            plt.close()
            if "outliers" in h.options: 
                plot_root = plt_to_TH1(h.outlier_aware_hist(df_this), s_name+'_outliers')
                if plot_root: plot_root.Write()
            del df_this
            gc.collect()

### 2D histograms
if hvar2DList:
    for hvars in hvar2DList:
        h = obj.histo2D(hvars, config)
        for s in h.selections:
            s_name = h.name+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)
            plot_root = plt_to_TH2(h.plot(df_this), s_name)
            plot_root.Write()
            plt.close()
            del df_this
            gc.collect()

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
                            if hasattr(compute, aggr_var[0]):
                                aggr_graph = graph.agg(getattr(compute, aggr_var[0]))
                            elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var[0]):
                                aggr_graph = getattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var[0])(graph)
                            #aggr_graph = graph.agg(aggr_var)
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

print("*** Output saved in plots/"+str(tag)+"/outPlot_"+str(year)+".root")



