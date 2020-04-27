import numpy as np
import modules.load_data as load_data
import modules.config_reader as config_reader
import modules.selections as select
import modules.get_ids as get_ids
from modules.plot import *

import argparse

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt


import pandas as pd

import ROOT
import datetime
import os

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', type = int, dest='year', help='which year', default=2016)
parser.add_argument('--tag', dest='tag', help='tag for plot', default=None)

args = parser.parse_args()

year = args.year 
fileList = "filelists/ECALELF_Run2UL/Data_UL2016.log"
if year ==2017: fileList = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log"
if year ==2018: fileList = "filelists/ECALELF_Run2UL/Data_UL2018.log"



files = [line. rstrip('\n') for line in open(fileList)]

#files = files[:1]

branches = ['runNumber','etaSCEle','phiSCEle',
            'xSeedSC','ySeedSC',
            'nPV',
            'timeSeedSC','timeSecondToSeedSC','amplitudeSeedSC', 'amplitudeSecondToSeedSC']
             #'laserSeedSC','alphaSeedSC']




df_chain= load_data.load_chain(files, "selected", branches)


print("entries = %d" % df_chain.shape[0])

df_chain['deltaT_ee'] = df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]']
#df_chain['deltaT_ee_abs'] = abs(df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]'])
df_chain['deltaEta_ee'] = df_chain['etaSCEle[0]']-df_chain['etaSCEle[1]']
df_chain['deltaPhi_ee'] = df_chain['phiSCEle[0]']-df_chain['phiSCEle[1]']
df_chain['deltaPhi_ee'] = np.where(df_chain['deltaPhi_ee']< -3.14, df_chain['deltaPhi_ee'] + 6.28, 
    np.where(df_chain['deltaPhi_ee']< -3.14,df_chain['deltaPhi_ee'] - 6.28, df_chain['deltaPhi_ee']))
df_chain['deltaT_e1_seeds'] = df_chain['timeSeedSC[0]']-df_chain['timeSecondToSeedSC[0]']
df_chain['deltaA_e1_seeds'] = df_chain['amplitudeSeedSC[0]']-df_chain['amplitudeSecondToSeedSC[0]']

df_chain['etaSCEle1'] = df_chain['etaSCEle[0]']
df_chain['etaSCEle2'] = df_chain['etaSCEle[1]']

df_chain[['xSeedSC1', 'xSeedSC2']]  = df_chain[['xSeedSC[0]','xSeedSC[1]']]
df_chain[['ySeedSC1', 'ySeedSC2']]  = df_chain[['ySeedSC[0]','ySeedSC[1]']]

df_chain = get_ids.appendIdxs(df_chain, "1")
df_chain = get_ids.appendIdxs(df_chain, "2")

#print(df_chain["iTTSeedSC1"])


tag = ""
if args.tag:
    tag = args.tag
    os.makedirs("plots/"+str(tag), exist_ok = True)

outFile = ROOT.TFile.Open("plots/"+str(tag)+"/outPlot_"+str(year)+".root","RECREATE")

config = config_reader.cfg_reader("config/plots.cfg")

hvarList  = config.readListOption("general::hvariables")
hvar2DList  = config.readListOption("general::hvariables2D")
grList  = config.readListOption("general::grvariables")
mapList  = config.readListOption("general::mvariables")


if config.hasOption("general::hvariables"):
    for hvar in hvarList:

        if not hvar in config.config['binning']: 
            print("### WARNING: no binning provided for ", hvar, ", skipping")
            continue
        binning = [float(s) for s in config.config['binning'][hvar].split(",")]
        binning[0] = int(binning[0])
        if hvar in config.config["hselections"]: 
            hselections = config.readOption("hselections::"+hvar).split(",")
        else:
            hselections = ["all"]
        for hselection in hselections:
            hselection = hselection.strip()
            df_this = select.apply_selection(df_chain,hselection)
            plot = plt.hist(df_this[hvar], binning[0], range = binning[-2:])
            
            plot_root = plt_to_TH1(plot, hvar+'_'+hselection.replace('-',"_"))
            plot_root.Write()
            plt.close()
            if hvar in config.config['hoptions']:
                if "outliers" in config.config['hoptions'][hvar]:
                    plot_outliers = outlier_aware_hist(df_chain[hvar], binning[0], binning[-2:])
                    plot_root = plt_to_TH1(plot_outliers, hvar+'_'+hselection.replace('-',"_")+'_outliers')
                    plot_root.Write()


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
        if name in config.config["hselections2D"]: 
            hselections = config.readOption("hselections2D::"+name).split(",")
        else:
            hselections = ["all"]
        for hselection in hselections:
            hselection = hselection.strip()    
            df_this = select.apply_selection(df_chain, hselection)
            plot = plt.hist2d(df_this[hvarx], df_this[hvary], bins = [xbinning[0],ybinning[0]], range = [xbinning[-2:], ybinning[-2:]])
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
                for opt in gropts:
                    opt = opt.strip()
                    if "aggr" in opt:
                        graph = df_this.groupby(xvar)[yvar]
                        aggr_var = opt.split(":")
                        aggr_var = aggr_var[1:]
                        aggr_graph = graph.agg(aggr_var)
                        name = yvar+'_vs_'+xvar
                        for i in aggr_var:
                            aggr_name = i+"_"
                        name = aggr_name + name
                        plot = aggr_graph.plot()
                        plot = plt_to_TGraph(plot,name+"_"+grselection.replace('-',"_"))
                        plt.close()
                        plot.Write()
                    else:
                        plot = df_chain.plot.scatter(xvar,yvar)
                        plot = plt_to_TGraph(plot,name)  
                        plt.close()
                        plot.Write()


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



    
outFile.Close()
