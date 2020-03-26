import numpy as np
import modules.load_data as load_data
import modules.config_reader as config_reader
import argparse

import matplotlib as mpl
import matplotlib.pyplot as plt

from modules.plot import *
import ROOT

parser = argparse.ArgumentParser(description='Command line parser of plotting options')

parser.add_argument('--year', type = int, dest='year', help='which year', default=2016)
parser.add_argument('--tag', dest='tag', help='tag for plot', default=None)

args = parser.parse_args()

year = args.year 
fileList = "filelists/ECALELF_Run2UL/Data_UL2016.log"
if year ==2017: fileList = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log"
if year ==2018: fileList = "filelists/ECALELF_Run2UL/Data_UL2018.log"



files = [line. rstrip('\n') for line in open(fileList)]



branches = ['runNumber','etaSCEle','phiSCEle',
#             'xSeedSC','ySeedSC',
            'nPV',
            'timeSeedSC','timeSecondToSeedSC'] # ,'amplitudeSeedSC', 'amplitudeSecondToSeedSC']
            #,'energySeedSC']
             #'laserSeedSC','alphaSeedSC']




df_chain= load_data.load_chain(files, "selected", branches)


print("entries = %d" % df_chain.shape[0])

df_chain['deltaT_ee'] = df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]']
#df_chain['deltaT_ee_abs'] = abs(df_chain['timeSeedSC[0]']-df_chain['timeSeedSC[1]'])
df_chain['deltaEta_ee'] = df_chain['etaSCEle[0]']-df_chain['etaSCEle[1]']
df_chain['deltaPhi_ee'] = df_chain['phiSCEle[0]']-df_chain['phiSCEle[1]']
#df_chain['deltaPhi_ee'] = df_chain['deltaPhi_ee'].apply(lambda x: {x + 6.28} if x < 3.14 else ({x - 6.28} if x > 3.14 else x))
df_chain['deltaT_e1_seeds'] = df_chain['timeSeedSC[0]']-df_chain['timeSecondToSeedSC[0]']
#


#df_chain['deltaA_e1_seeds'] = df_chain['amplitudeSeedSC[0]']-df_chain['amplitudeSecondToSeedSC[0]']


# big eta bins
df_chain_EB = df_chain[(abs(df_chain['etaSCEle[0]'])<1.5) & (abs(df_chain['etaSCEle[1]'])>1.5) | (abs(df_chain['etaSCEle[0]'])>1.5) & (abs(df_chain['etaSCEle[1]'])<1.5) ]
df_chain_EE = df_chain[(abs(df_chain['etaSCEle[0]'])>1.5) & (abs(df_chain['etaSCEle[1]'])>1.5)]
df_chain_BB = df_chain[(abs(df_chain['etaSCEle[0]'])<1.5) & (abs(df_chain['etaSCEle[1]'])<1.5)]

dfs_dict = {
    'EE': df_chain_EE,
    'EB': df_chain_EB,
    'BB': df_chain_BB
    }

tag = ""
if args.tag:
    tag = "_"+args.tag


outFile = ROOT.TFile.Open("plots/outPlot_"+str(year)+str(tag)+".root","RECREATE")

config = config_reader.cfg_reader("config/plots.cfg")

hvarList  = config.readListOption("general::hvariables")
hvar2DList  = config.readListOption("general::hvariables2D")
grList  = config.readListOption("general::grvariables")



if config.hasOption("general::hvariables"):
    for hvar in hvarList:
        selections = {'all': df_chain}
        if hvar in config.config['hselections']:
            for k in dfs_dict:
                if k in config.config['hselections'][hvar]: selections[k] = dfs_dict[k]
        for sel, df in selections.items():
            if not hvar in config.config['binning']: 
                print("### WARNING: no binning provided for ", hvar, ", skipping")
            binning = [float(s) for s in config.config['binning'][hvar].split(",")]
            binning[0] = int(binning[0])
            plot = plt.hist(df[hvar], binning[0], range = binning[-2:])
            plot_root = pltToTH1(plot, hvar+'_'+sel)
            plt.close()
            plot_root.Write()
    
    #if hvar in config.config['hoptions']:
    #    if "outliers" in config.config['hoptions'][hvar]:
    #        plot_outliers = outlier_aware_hist(df_chain[hvar], binning[0], binning[-2:])
    #        plot_root = pltToTH1(plot_outliers, hvar+"_outliers")
    #        plot_root.Write()

if config.hasOption("general::hvariables2D"):

    for hvars in hvar2DList:
        selections = {'all': df_chain}
        hvarx, hvary, name = hvars.split(':')
        if name in config.config['hselections2D']:
            for k in dfs_dict:
                if k in config.config['hselections2D'][name]: selections[k] = dfs_dict[k]
        for sel, df in selections.items():
            
            if not "X@"+name in config.config['binning2D']: 
                print("### WARNING: no x binning provided for ", name, ", skipping")
            if not "Y@"+name in config.config['binning2D']: 
                print("### WARNING: no y binning provided for ", name, ", skipping")
            xbinning = [float(s) for s in config.config['binning2D']["X@"+name].split(",")]
            ybinning = [float(s) for s in config.config['binning2D']["Y@"+name].split(",")]
            xbinning[0] = int(xbinning[0])
            ybinning[0] = int(ybinning[0])
            plot = plt.hist2d(df[hvarx], df[hvarx], bins = [xbinning[0],ybinning[0]], range = [xbinning[-2:], ybinning[-2:]])
            plot_root = pltToTH2(plot, name+'_'+sel)
            plot_root.Write()
            plt.close()


if config.hasOption("general::grvariables"):
    for grvar in grList:
        selections = {'all': df_chain}
        if grvar in config.config['grselections']:
            for k in dfs_dict:
                if k in config.config['grselections'][grvar]: selections[k] = dfs_dict[k]
        for sel, df in selections.items():
            xvar , yvar = grvar.split(":")
            if grvar in config.config["groptions"]:
                grArgs = config.readMultiOption("groptions::"+grvar)
                for args in grArgs:
                    if "aggr" in args:
                        aggr_options = [item for item in args.split(',') if "aggr" in item]    
                        for aggr_opt in aggr_options:
                            graph = df.groupby(xvar)[yvar]
                            aggr_var = aggr_opt.split(":")
                            aggr_var = aggr_var[1:]
                            aggr_graph = graph.agg(aggr_var)
                            name = yvar+'_vs_'+xvar
                            for i in aggr_var:
                                aggr_name = i+"_"
                            name = aggr_name + name
                            plot = aggr_graph.plot()
                            plot = pltToTGraph(plot,name+"_"+sel)
                            plot.Write()
                            plt.close()
            else:
                plot = df_chain.plot.scatter(xvar,yvar)
                plot = pltToTGraph(plot,name)  
                plt.close()
                plot.Write()
    

    
outFile.Close()
