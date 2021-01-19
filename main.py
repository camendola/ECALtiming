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

import random, string
import modules.classes as obj

import pandas as pd
import dask
from dask import delayed
import dask.dataframe as dd
import gc
import ROOT
import datetime
import os, sys


import psutil
process = psutil.Process(os.getpid())

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', type = int, dest='year', help='which year', default=2016)
parser.add_argument('--tag', dest='tag', help='tag for plot', default=None)
parser.add_argument('--cfg', dest='cfg', help='cfg file', default=None)
parser.add_argument('--byrun', dest='byrun', help='split graphs by run only', default=False, action ='store_true')
parser.add_argument('--byrunsize', dest='byrunsize', help='split graphs by run and by size', default=False, action ='store_true')
parser.add_argument('--bysize', dest='bysize', help='split graphs by size only', default=False, action ='store_true')
parser.add_argument('-e', '--era', default = None, help="era")
parser.add_argument('--debug', dest='debug', help='debug', default=False, action ='store_true')
parser.add_argument('--laser', dest='laser', help='laser', default = False,  action ='store_true')
parser.add_argument('--color', dest='color', help='color', default = "")


args = parser.parse_args()

year = args.year 
fileList = "filelists/ECALELF_Run2UL_skimmed//Data_UL2016.log"
fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2016_extra.log"
if year ==2017: 
    fileList = "filelists/ECALELF_Run2UL_skimmed//Data_ALCARECO_UL2017.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017_extra.log"
if year ==2018: 
    fileList = "filelists/ECALELF_Run2UL_skimmed/Data_UL2018_106X_dataRun2_UL18.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2018_extra.log"


files = [line. rstrip('\n') for line in open(fileList)]
files_extra = [line. rstrip('\n') for line in open(fileList_extra)]
print (files)
newfiles = []
if args.era:
    for file in files:
        if str(args.year)+args.era in file:
            newfiles.append(file)
    files = newfiles

newfiles = []
if args.laser:
    for file in files:
        newfiles.append(file.replace("skimmed", "laser").replace(".root", args.color+args.color+".root"))
        
    files = newfiles

debug = args.debug

if debug:
    files = files[-1:] 
    files_extra = files_extra[-1:]

print("*** Processing year "+str(args.year))
if args.byrun:     print("*** splitting graphs by run")
if args.byrunsize: print("*** splitting graphs by number of events, respecting the run boundaries")
if args.bysize:    print("*** splitting graphs by number of events")


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






#branches = ['runNumber','etaSCEle','phiSCEle',
#            'etaEle',
#            'R9Ele', 
#            'timeSeedSC','timeSecondToSeedSC','amplitudeSeedSC', 
#            'energySeedSC', 'noiseSeedSC',
#            'invMass','ele1E', 'ele2E', 'eventTime', 'gainSeedSC']

#branches = ['runNumber','etaSCEle1','etaSCEle2', 'phiSCEle1','phiSCEle2', 
#            'xSeedSC1','xSeedSC2','ySeedSC1','ySeedSC2', 'etaEle1','etaEle2','vtxZ',
#            'R9Ele1', 'R9Ele2',
#            'timeSeedSC1','timeSeedSC2', 'timeSecondToSeedSC1','timeSecondToSeedSC2','amplitudeSeedSC1', 'amplitudeSeedSC2','amplitudeSecondToSeedSC1','amplitudeSecondToSeedSC2',
#            'energySeedSC1', 'energySeedSC2','energySecondToSeedSC1','energySecondToSeedSC2', 'noiseSeedSC1','noiseSeedSC2',
#            'invMass','ele1E', 'ele2E', 'eventTime']

#branches = ['runNumber','etaSCEle1','etaSCEle2', 
#            'timeSeedSC1','timeSeedSC2', 'timeSecondToSeedSC1','timeSecondToSeedSC2',
#            'invMass', 'eventTime', "gainSeedSC1", "gainSeedSC2", "R9Ele1", "R9Ele2", "noiseSeedSC1", "noiseSeedSC2", "amplitudeSeedSC1", "amplitudeSeedSC2", "amplitudeSecondToSeedSC1"]

branches_extra = ['noiseSeedSC1_GT', 'noiseSeedSC2_GT', 'eventTime', 'noiseSecondToSeedSC1_GT','iTTSeedSC1', 'scSeedSC1','iTTSecondToSeedSC1', 'scSecondToSeedSC1',]

#df_chain = load_data.load_chain(files, "selected", branches, suffix = "extra", other_tree_name = "extended", other_branch = branches_extra)

#df_chain = load_data.load_hdf_file(files[0], "selected", branches) if args.debug else load_data.load_hdf(files, "selected", branches)
df_chain = load_data.load_chain(files, "selected") 

#print(type(df_chain))
#df_extra = load_data.load_chain(files, "extended", branches_extra, suffix = "extra") # taking only X, Y, Z of first hit
#df_chain = pd.concat([df_original.set_index('runNumber'), df_extra.set_index('runNumber')], axis=1, join = 'inner').reset_index()
#df_chain = df_original
#print(df_chain.keys())
#print("entries = %d" % df_chain.shape[0])

#flat columns
#branches_split = ["timeSeedSC","timeSecondToSeedSC","chargeEle","etaSCEle", "phiSCEle","xSeedSC", "ySeedSC", "amplitudeSeedSC","energySeedSC", "energySecondToSeedSC", "amplitudeSecondToSeedSC","R9Ele","etaEle","noiseSeedSC", "gainSeedSC"]
#branches_split = ["timeSeedSC","chargeEle","etaSCEle", "phiSCEle","amplitudeSeedSC","energySeedSC","R9Ele","etaEle","noiseSeedSC", "gainSeedSC"]
#print (df_chain.columns)
#for br in branches_split:
#    if br+"[1]" in df_chain.columns.values:
#        df_chain[[br+'1', br+'2']] = df_chain[[br+'[0]',br+'[1]']].drop(columns=[br+'[0]',br+'[1]',br+'[2]'])
#        df_chain = df_chain.drop(columns=[br+'[0]',br+'[1]',br+'[2]'])

#df_chain = df_chain.assign(deltaT_ee = df_chain['timeSeedSC1']-df_chain['timeSeedSC2'], deltaT_e1 = df_chain['timeSeedSC1']-df_chain['timeSecondToSeedSC1'], effA_ee = compute.effective_amplitude(df_chain['amplitudeSeedSC1'],df_chain['noiseSeedSC1'], df_chain['amplitudeSeedSC2'], df_chain['noiseSeedSC2']), effA_e1 = compute.effective_amplitude(df_chain['amplitudeSeedSC1'],df_chain['noiseSeedSC1'],df_chain['amplitudeSecondToSeedSC1'],df_chain['noiseSeedSC1']))



print (df_chain.columns)
array_columns = []
for n in range(df_chain.shape[1]):
    if df_chain.dtypes[n] == object:
        if df_chain.infer_objects().dtypes[n] == object:
            array_columns.append(df_chain.columns[n])
    if df_chain.dtypes[n] == bool:
        df_chain[df_chain.columns[n]] = pd.Series(df_chain[df_chain.columns[n]].astype(int), index=df_chain.index)

print(array_columns)
for n in array_columns:
    if df_chain[n].str.len().iloc[0] == 2:
        df_chain[[n+'1', n+'2']] = pd.DataFrame(df_chain[n].tolist(), index=df_chain.index)
    if df_chain[n].str.len().iloc[0] == 3:
        df_chain[[n+'1', n+'2', n+'3']] = pd.DataFrame(df_chain[n].tolist(), index=df_chain.index)
        df_chain = df_chain.drop(columns=n+'3')
        df_chain = df_chain.drop(columns=n)
del array_columns
new_columns = []
for n in range(df_chain.shape[1]):
    print(df_chain.columns[n])
    new_columns.append(df_chain.columns[n].replace("[0]","1").replace("[1]","2"))


df_chain.columns = new_columns
print(df_chain.columns)

df_chain = df_chain.assign(deltaT_ee_recal = df_chain['timeSeedSC1_recal']-df_chain['timeSeedSC2_recal'])

#df = get_ids.appendIdxs(df, "1")
#df = get_ids.appendIdxs(df, "2")


tag = ""
if args.tag:
    tag = args.tag
    os.makedirs("plots/"+str(tag), exist_ok = True)

era = ""
if args.era: era = args.era
outFile = ROOT.TFile.Open("plots/"+str(tag)+"/outPlot_"+str(year)+era+".root","RECREATE")
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
        h = obj.histo1d(hvar,config)
        results = []
        s_names = []
        for s in h.selections: 
            s_name = h.var+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)[h.var]
            plot_root = plt_to_TH1(h.plot(df_this), s_name)
            plot_root.Write()
            plt.close()
            if "outliers" in h.options: 
                plot_root = plt_to_TH1(h.outlier_aware_hist(df_this), s_name+'_outliers')
                if plot_root: plot_root.Write()
        del df_this
        
### 2D histograms
if hvar2DList:
    for hvars in hvar2DList:
        h = obj.histo2d(hvars, config)
        results = []
        s_names = []
        print (h.selections)
        for s in h.selections:
            s_name = h.name+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)[[h.varx, h.vary]]
            s_names.append(s_name)
            plot_root = plt_to_TH2(h.plot(df_this), s_name)
            plot_root.Write()
            plt.close()
        del df_this

### graphs
if grList:
    for grvar in grList:
        gr = obj.graph(grvar, config)
        for s in gr.selections:
            size = 0 
            if (":") in s: 
                s, size = s.split(":")
                size = int(size)
            s_name = gr.name+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)
            if gr.varx == "runNumber" or gr.varx == "eventTime": df_this = df_this.sort_values(by=['eventTime']) 
            for opt in gr.options: 
                if not "aggr" in opt: 
                    print("### WARNING only aggregate options are implemented for graphs, skipping ", opt)
                    continue
                print(opt.split(":")[1:])
                if len(opt.split(":")[1:]) > 1: print("### WARNING multiple aggregate variables not implemented, using ", opt.split(":")[1])
                aggr_var = opt.split(":")[1]

                plot_root = plt_to_TGraph(gr.plot(df_this, aggr_var, args, size), aggr_var + "_" + s_name, gr.binning)
                if (aggr_var == "size"): plot_root.Print()
                plot_root.Write()
                plt.close()               

            del df_this
            gc.collect()

### maps
if mapList:
    for mvars in mapList:
        map2d = obj.map2d(mvars, config)
        for s in map2d.selections:
            s_name = map2d.name+'_'+s.replace('-',"_")
            df_this = select.apply_selection(df_chain, s)
            for opt in map2d.options: 
                if not "aggr" in opt: 
                    print("### WARNING only aggregate options are implemented for maps, skipping ", opt)
                    continue
                print(opt.split(":")[1:])
                if len(opt.split(":")[1:]) > 1: print("### WARNING multiple aggregate variables not implemented, using ", opt.split(":")[1])
                aggr_var = opt.split(":")[1]
                plot_root = table_to_TH2(map2d.plot(df_this, aggr_var), s_name)
                plot_root.Write()
            del df_this
            gc.collect()

outFile.Close()

print("*** Output saved in plots/"+str(tag)+"/outPlot_"+str(year)+era+".root")



