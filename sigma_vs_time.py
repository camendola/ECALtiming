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
parser.add_argument('--byrun', dest='byrun', help='split by run only', default=False, action ='store_true')
parser.add_argument('--byrunsize', dest='byrunsize', help='split by run and by size', default=False, action ='store_true')
parser.add_argument('--bysize', dest='bysize', help='split by size only', default=False, action ='store_true')

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

print("*** Processing year "+str(args.year))
if args.byrun:     print("*** splitting by run")
if args.byrunsize: print("*** splitting by number of events, respecting the run boundaries")
if args.bysize:    print("*** splitting by number of events")

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



branches = ['runNumber','etaSCEle',
            'eventTime',
            'timeSeedSC','timeSecondToSeedSC','amplitudeSeedSC', 'amplitudeSecondToSeedSC',
            'noiseSeedSC', 'R9Ele',
            'chargeEle', 'invMass']



df_original= load_data.load_chain(files, "selected", branches)
#df_extra= load_data.load_chain(files_extra, "extraCalibTree", branches_extra, firsthit = True) # taking only X, Y, Z of first hit
#df_chain = pd.concat([df_original, df_extra], axis=1) 

df_chain = df_original
print("entries = %d" % df_chain.shape[0])
del df_original


#flat columns
branches_split = ["chargeEle","etaSCEle", "amplitudeSeedSC", "amplitudeSecondToSeedSC","R9Ele"]
for br in branches_split:
    if br+"[1]" in df_chain:
        df_chain[[br+'1', br+'2']] = df_chain[[br+'[0]',br+'[1]']]


df_chain['deltaT_ee'] = df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]']

df_chain['deltaT_e1_seeds'] = df_chain['timeSeedSC[0]']-df_chain['timeSecondToSeedSC[0]']
#df_chain['deltaT_e1_seeds'] = df_chain['deltaT_e1_seeds'].div(np.sqrt(2))

df_chain['deltaT_e2_seeds'] = df_chain['timeSeedSC[1]']-df_chain['timeSecondToSeedSC[1]']

df_chain['deltaA_e1_seeds'] = df_chain['amplitudeSeedSC[0]']-df_chain['amplitudeSecondToSeedSC[0]']
df_chain['deltaA_e2_seeds'] = df_chain['amplitudeSeedSC[1]']-df_chain['amplitudeSecondToSeedSC[1]']


df_chain['effA_ee'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[0]'],
                                                        df_chain['noiseSeedSC[0]'],
                                                        df_chain['amplitudeSeedSC[1]'],
                                                        df_chain['noiseSeedSC[1]'])

df_chain['effA_e1_seeds'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[0]'],
                                                        df_chain['noiseSeedSC[0]'],
                                                        df_chain['amplitudeSecondToSeedSC[0]'],
                                                        df_chain['noiseSeedSC[0]'])

df_chain['effA_e2_seeds'] = compute.effective_amplitude(df_chain['amplitudeSeedSC[1]'],
                                                        df_chain['noiseSeedSC[1]'],
                                                        df_chain['amplitudeSecondToSeedSC[1]'],
                                                        df_chain['noiseSeedSC[1]'])
#df_chain['responseSeedSC1'] = compute.relative_response(df_chain['laserSeedSC[0]'],df_chain['alphaSeedSC[0]'])
#df_chain['responseSeedSC2'] = compute.relative_response(df_chain['laserSeedSC[1]'],df_chain['alphaSeedSC[1]'])

#df_chain = get_ids.appendIdxs(df_chain, "1")
#df_chain = get_ids.appendIdxs(df_chain, "2")


tag = ""
if args.tag:
    tag = args.tag
    os.makedirs("plots_sigma/"+str(tag), exist_ok = True)

outFile = ROOT.TFile.Open("plots_sigma/"+str(tag)+"/outPlot_"+str(year)+".root","RECREATE")

config = config_reader.cfg_reader(args.cfg)


grList  = config.readListOption("general::grvariables")

toPlot = []

if grList:
    for grvar in grList:
        gvarx, gvary = grvar.split(':')
        toPlot.append(gvarx)
        toPlot.append(gvary)


for var in toPlot:
    if not var in df_chain:
        print("### ERROR: missing variable: "+ var)
        sys.exit()


df_chain = df_chain.sort_values(by=['eventTime'])

if config.hasOption("general::grvariables"):
    for grvar in grList:
        if grvar in config.config["grselections"]: 
            grselections = config.readOption("grselections::"+grvar).split(",")
        else:
            grselections = ["all"]
        xvar , yvar = grvar.split(":")
        for grselection in grselections:
            grselection = grselection.strip()
            if (":") in grselection: 
                grselection, size = grselection.split(":")
                size = int(size)
                print (grselection,size)
            df_this = select.apply_selection(df_chain,grselection)
            df_this = df_this.sort_values(by=['eventTime'])
            if grvar in config.config["groptions"]:
                gropts = config.readOption("groptions::"+grvar).split(",")
                custom_binning = False
                binning = []
                mid = []
                for opt in gropts:
                    opt = opt.strip()
                    if "aggr" in opt:
                        aggr_var = opt.split(":")
                        aggr_var = aggr_var[1:]
                        if args.byrun:
                            graph = df_this.groupby(xvar)[yvar]
                            xlabel = xvar
                        elif args.byrunsize:
                            xlabel = xvar
                            graph = df_this.groupby([xvar, df_this.groupby(xvar).cumcount() // size])[xlabel,yvar]
                        elif args.bysize:
                            xlabel = 'runNumber'
                            graph = df_this.groupby(np.arange(len(df_this)) // size)[xlabel,yvar]
                        if hasattr(compute, aggr_var[0]):
                            if args.bysize:
                                aggr_graph = graph.agg({xlabel:'mean', yvar:getattr(compute, aggr_var[0])})
                            else:
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
                        if args.byrun:
                            plot = aggr_graph.plot()
                        elif args.bysize:
                            plot = aggr_graph.plot(x = xvar, y = yvar)
                        else:
                            plot = aggr_graph.unstack().plot()
                        plot = plt_to_TGraph(plot,name+"_"+grselection.replace('-',"_"), mid, binning)
                        plt.close()
                        plot.Write()
                    else:
                        plot = df_chain.plot(xvar,yvar)
                        plot = plt_to_TGraph(plot,name)  
                        plt.close()
                        plot.Write()
            del df_this, graph

outFile.Close()
print("*** Output saved in plots_sigma/"+str(tag)+"/outPlot_"+str(year)+".root")
