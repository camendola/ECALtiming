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

import gc
import ROOT
import datetime
import os, sys


import psutil

process = psutil.Process(os.getpid())

# fmt: off
parser = argparse.ArgumentParser(description = "Command line parser of plotting options")

parser.add_argument("--year",      dest = "year",      help = "which year",                      default = 2016, type=int)
parser.add_argument("--tag",       dest = "tag",       help = "tag for plot",                    default = None)
parser.add_argument("--cfg",       dest = "cfg",       help = "cfg file",                        default = None)
parser.add_argument("--byrun",     dest = "byrun",     help = "split graphs by run only",        default = False, action = "store_true")
parser.add_argument("--byrunsize", dest = "byrunsize", help = "split graphs by run and by size", default = False, action = "store_true")
parser.add_argument("--bysize",    dest = "bysize",    help = "split graphs by size only",       default = False, action = "store_true")
parser.add_argument("-e", "--era", dest = "era",       help = "era",   default = None)
parser.add_argument("--debug",     dest = "debug",     help = "debug", default = False, action = "store_true")
parser.add_argument("--laser",     dest = "laser",     help = "laser", default = False, action = "store_true")
parser.add_argument("--extra",     dest = "extra",     help = "extra", default = False, action = "store_true")
parser.add_argument("--suffix",    dest = "suffix",    help = "suffix", default = None)
parser.add_argument("--color",     dest = "color",     help = "color", default = "")
# fmt: on

args = parser.parse_args()

year = args.year
fileList = "filelists/ECALELF_Run2UL_skimmed/Data_UL2016.log"
fileList_extra = "filelists/ECALELF_Run2UL_skimmed/Data_UL2016_extra.log"
if year == 2017:
    fileList = "filelists/ECALELF_Run2UL_skimmed//Data_ALCARECO_UL2017.log"
    fileList_extra = "filelists/ECALELF_Run2UL_skimmed/Data_ALCARECO_UL2017_extra.log"
if year == 2018:
    fileList = "filelists/ECALELF_Run2UL_skimmed/Data_UL2018_106X_dataRun2_UL18.log"
    fileList_extra = (
        "filelists/ECALELF_Run2UL_skimmed/Data_UL2018_106X_dataRun2_UL18_extra.log"
    )


files = [line.rstrip("\n") for line in open(fileList) if not line.startswith("#")]
files_extra = [line.rstrip("\n") for line in open(fileList_extra) if not line.startswith("#")]

print(files)
print(files_extra)

newfiles = []
newfiles_extra = []
if args.era:
    for file in files:
        if str(args.year) + args.era in file:
            newfiles.append(file)
            newfiles_extra.append(file.replace(".root", "_extra.root"))
    files = newfiles
    files_extra = newfiles_extra

newfiles = []
if args.laser:
    for file in files:
        newfiles.append(
            file.replace("skimmed", "laser").replace(".root", args.color + ".root")
        )
    files = newfiles

newfiles = []
if args.suffix:
    for file in files:
        newfiles.append(file.replace(".root", args.suffix + ".root"))
    files = newfiles

debug = args.debug

if debug:
    files = files[-1:]
    files_extra = files_extra[-1:]


print("*** Processing year " + str(args.year))
if args.byrun:
    print("*** splitting graphs by run")
if args.byrunsize:
    print("*** splitting graphs by number of events, respecting the run boundaries")
if args.bysize:
    print("*** splitting graphs by number of events")

### ECALELF original content:
# ['runNumber', 'lumiBlock', 'eventNumber', 'eventTime', 'nBX', 'isTrain', 'mcGenWeight', 'HLTfire',
#'rho', 'nPV', 'nPU', 'vtxX', 'vtxY', 'vtxZ',
#'eleID', 'chargeEle', 'recoFlagsEle', 'etaEle', 'phiEle', 'fbremEle', 'R9Ele',
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


df_chain = load_data.load_chain(files, "selected")
print(df_chain.shape)
if args.extra:
    df_chain = df_chain.sort_values(by=["eventNumber"])
    df_extra = load_data.load_chain(files_extra, "extended")
    df_extra = df_extra.sort_values(by=["eventNumber"])

    df_chain = df_chain.set_index("eventNumber")
    df_chain = df_chain[~df_chain.index.duplicated(keep='first')]
    
    df_extra = df_extra.set_index("eventNumber")
    df_extra = df_extra[~df_extra.index.duplicated(keep='first')]
    df_chain = pd.concat([df_chain, df_extra], axis=1).reset_index()

    df_extra = pd.DataFrame()
    df_chain = df_chain.loc[:, ~df_chain.columns.duplicated()]


array_columns = []
for n in range(df_chain.shape[1]):
    if df_chain.dtypes[n] == object:
        if df_chain.infer_objects().dtypes[n] == object:
            array_columns.append(df_chain.columns[n])
    if df_chain.dtypes[n] == bool:
        df_chain[df_chain.columns[n]] = pd.Series(
            df_chain[df_chain.columns[n]].astype(int), index=df_chain.index
        )

print(array_columns)
for n in array_columns:
    if df_chain[n].str.len().iloc[0] == 2:
        df_chain[[n + "1", n + "2"]] = pd.DataFrame(
            df_chain[n].tolist(), index=df_chain.index
        )
    if df_chain[n].str.len().iloc[0] == 3:
        df_chain[[n + "1", n + "2", n + "3"]] = pd.DataFrame(
            df_chain[n].tolist(), index=df_chain.index
        )
        df_chain = df_chain.drop(columns=n + "3")
        df_chain = df_chain.drop(columns=n)
del array_columns
new_columns = []
for n in range(df_chain.shape[1]):
    print(df_chain.columns[n])
    new_columns.append(df_chain.columns[n].replace("[0]", "1").replace("[1]", "2"))


df_chain.columns = new_columns

print(df_chain.columns)

if args.laser:
    df_chain = df_chain.assign(
        deltaT_ee_recal=df_chain["timeSeedSC1_recal"] - df_chain["timeSeedSC2_recal"],
        new_calib1=-df_chain["calib1"] + df_chain["laser1"],
    )

if args.extra:
    df_chain = df_chain.assign(
        effA_e1=compute.effective_amplitude(
            df_chain["amplitudeSeedSC1"],
            df_chain["noiseSeedSC1"],
            df_chain["amplitudeSecondToSeedSC1"],
            df_chain["noiseSeedSC1"],
        )
    )
    df_chain = df_chain.assign(
        effA_e2=compute.effective_amplitude(
            df_chain["amplitudeSeedSC2"],
            df_chain["noiseSeedSC2"],
            df_chain["amplitudeSecondToSeedSC2"],
            df_chain["noiseSeedSC2"],
        )
    )

df_chain = df_chain.assign(
    deltaT_ee_corr_TOF=df_chain["timeSeedSC1_corr_TOF"] - df_chain["timeSeedSC2_corr_TOF"],
    #deltaT_e1_corr_TOF=df_chain["timeSeedSC1_corr_TOF"] - df_chain["timeSecondToSeedSC1_corr_TOF"]
)

tag = ""
if args.tag:
    tag = args.tag
if args.suffix:
    tag = tag + args.suffix

os.makedirs("plots/" + str(tag), exist_ok=True)

era = ""
if args.era:
    era = args.era
outFile = ROOT.TFile.Open(
    "plots/" + str(tag) + "/outPlot_" + str(year) + era + ".root", "RECREATE"
)

os.system("cp " + args.cfg + " plots/" + str(tag))

config = config_reader.cfg_reader(args.cfg)

# fmt: off
hvarList   = config.readListOption("general::hvariables")
hvar2DList = config.readListOption("general::hvariables2D")
grList     = config.readListOption("general::grvariables")
mapList    = config.readListOption("general::mvariables")
# fmt: on

toPlot = []
if hvarList:
    for hvar in hvarList:
        toPlot.append(hvar)
if hvar2DList:
    for hvars in hvar2DList:
        hvarx, hvary, name = hvars.split(":")
        toPlot.append(hvarx)
        toPlot.append(hvary)
if grList:
    for grvar in grList:
        gvarx, gvary = grvar.split(":")
        toPlot.append(gvarx)
        toPlot.append(gvary)
if mapList:
    for mvars in mapList:
        mvarx, mvary, mvarz = mvars.split(":")
        toPlot.append(mvarx)
        toPlot.append(mvary)
        toPlot.append(mvarz)

for var in toPlot:
    if not var in df_chain:
        print("### ERROR: missing variable: " + var)
        sys.exit()


### 1D histograms
if hvarList:
    for hvar in hvarList:
        h = obj.histo1d(hvar, config)
        results = []
        s_names = []
        for s in h.selections:
            s_name = h.var + "_" + s.replace("-", "_")
            df_this = select.apply_selection(df_chain, s)[h.var]
            plot_root = plt_to_TH1(h.plot(df_this), s_name)
            plot_root.Write()
            plt.close()
            if "outliers" in h.options:
                plot_root = plt_to_TH1(
                    h.outlier_aware_hist(df_this), s_name + "_outliers"
                )
                if plot_root:
                    plot_root.Write()
        del df_this

### 2D histograms
if hvar2DList:
    for hvars in hvar2DList:
        h = obj.histo2d(hvars, config)
        results = []
        s_names = []
        for s in h.selections:
            s_name = h.name + "_" + s.replace("-", "_")
            df_this = select.apply_selection(df_chain, s)[[h.varx, h.vary]]
            s_names.append(s_name)
            do_density = False
            if "density" in h.options:
                do_density = True
            plot_root = plt_to_TH2(h.plot(df_this, do_density), s_name)
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
            s_name = gr.name + "_" + s.replace("-", "_")
            df_this = select.apply_selection(df_chain, s)
            if gr.varx == "runNumber" or gr.varx == "eventTime":
                df_this = df_this.sort_values(by=["eventTime"])
            for opt in gr.options:
                if not "aggr" in opt:
                    print(
                        "### WARNING only aggregate options are implemented for graphs, skipping ",
                        opt,
                    )
                    continue
                print(opt.split(":")[1:])
                if len(opt.split(":")[1:]) > 1:
                    print(
                        "### WARNING multiple aggregate variables not implemented, using ",
                        opt.split(":")[1],
                    )
                aggr_var = opt.split(":")[1]

                plot_root = plt_to_TGraph(
                    gr.plot(df_this, aggr_var, args, size),
                    aggr_var + "_" + s_name,
                    gr.binning,
                )
                if aggr_var == "size":
                    plot_root.Print()
                plot_root.Write()
                plt.close()

            del df_this
            gc.collect()

### maps
if mapList:
    for mvars in mapList:
        map2d = obj.map2d(mvars, config)
        for s in map2d.selections:
            s_name = map2d.name + "_" + s.replace("-", "_")
            df_this = select.apply_selection(df_chain, s)
            for opt in map2d.options:
                if not "aggr" in opt:
                    print(
                        "### WARNING only aggregate options are implemented for maps, skipping ",
                        opt,
                    )
                    continue
                print(opt.split(":")[1:])

                aggr_var = opt.split(":")[1]
                dump = False # dump table in rECAL style
                if len(opt.split(":")[1:]) > 1:
                    if "dump" in opt.split(":")[2]: dump = True
                plot_root = table_to_TH2(map2d.plot(df_this, aggr_var, ("plots/" + str(tag) + "/"+ str(year) + era) if dump else None), aggr_var + "_" + s_name)
                plot_root.Write()

                    
            del df_this
            gc.collect()

outFile.Close()

print("*** Output saved in plots/" + str(tag) + "/outPlot_" + str(year) + era + ".root")
