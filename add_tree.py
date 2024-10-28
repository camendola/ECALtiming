import sys,os
from array import array
import argparse
import numpy as np
import uproot
import pandas as pd
import modules.load_data as load_data
import modules.get_ids as get_ids
from root_pandas import to_root


def appendIdxs(df, pair_idx):
    eta = "etaSCEle"+pair_idx
    iz_col = np.where(df[eta] > 0, 1, -1)
    ix = "xSeedSC"+pair_idx
    iy = "ySeedSC"+pair_idx
    ieta = ix
    iphi = iy


    isEB = abs(df[eta]) < 1.479
    #isEB = df["ZRecHitSCEle"+pair_idx] == 0
    df["EcalDetIDSeedSC"+pair_idx] = np.where(isEB, get_ids.getEBDetId(df[ieta], df[iphi]), get_ids.getEEDetId(df[ix], df[iy],iz_col))

    return df

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--name', type=str, required=False,
                    default="noiseSeedSC_test", help="Output branch name")
parser.add_argument('-y', '--year', type=int,
                    default=2017, help="year")
args =parser.parse_args()


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
files = files[:1]
files_extra = files_extra[:1]
#---------------------

print("@@@ Loading IOVs: EcalPedestals (Run 2 UL)")
dump_file = "/drf/projets/cms/ca262531/ECALconditions_dumps/EcalPedestals.dat"
#conddb_dumper -O EcalPedestals -t EcalPedestals_timestamp_UL_Run1_Run2_v1 -j -o /eos/home-c/camendol/ECAL_UL_dump/EcalPedestals.dat --b 6234602014664294400
df_dump = pd.read_csv(dump_file, sep='\s+',  header=None, usecols = [0, 1, 4, 5, 6 , 7], names = ["iX", "iY", "noise","begin", "end", "DetID"])
df_dump["begin"] = (df_dump["begin"].values  >> 32)
df_dump["end"]   = (df_dump["end"].values    >> 32)
df_red = df_dump[["begin","end"]].drop_duplicates()

#---------------------

branches = ['xSeedSC','ySeedSC','etaSCEle',
        'noiseSeedSC', 
        'eventTime']

branches_extra = ['XRecHitSCEle1','XRecHitSCEle2',
                  'YRecHitSCEle1','YRecHitSCEle2',
                  'ZRecHitSCEle1','ZRecHitSCEle2']

print("@@@ Loop on files")
for file, file_extra in zip(files, files_extra):
    if not os.path.isfile(file):
        print ("Could not find file:", file)
        sys.exit()

    df, uproot_file = load_data.load_file(file, "selected", branches)
    print (df['eventTime'])
    branches_split = ["etaSCEle","xSeedSC","ySeedSC","noiseSeedSC"]
    for br in branches_split:
        if br+"[1]" in df:
            df[[br+'1', br+'2']] = df[[br+'[0]',br+'[1]']]


    df_extra, temp = load_data.load_file(file_extra, "extraCalibTree", branches_extra) # taking only X, Y, Z of first and second by energy
    del temp
    df_extra1 = df_extra.stack().str[0].unstack()
    df_extra1 = df_extra1.drop(columns = ['XRecHitSCEle1','XRecHitSCEle2','YRecHitSCEle1','YRecHitSCEle2'])
    df_extra1.columns = ["zSeedSC1","zSeedSC2"]
    df_extra2 = df_extra.stack().str[1].unstack()
    df_extra2.columns = ["xSecondToSeedSC1","xSecondToSeedSC2","ySecondToSeedSC1","ySecondToSeed2","zSecondToSeed1","zSecondToSeed2"]
    df = pd.concat([df, df_extra1, df_extra2], axis=1) 
    del df_extra1, df_extra2

    print("@@@ Appending DetIDs and geometric/electronic elements...")
    df = appendIdxs(df, "1")
    df = appendIdxs(df, "2")
    
    time = df.eventTime.values
    begin = df_red.begin.values
    end = df_red.end.values
    
    print ("@@@ Matching IOVs...")
    i, j = np.where((time[:, None] >= begin) & (time[:, None] < end))
    
    df = pd.DataFrame(
        np.column_stack([df.values[i], df_red.values[j]]),
        columns=df.columns.append(df_red.columns)
    )
    
    print ("@@@ Mapping Ecal pedestals by time and crystal...")
    df['noiseSeedSC1_GT'] = df.set_index(['EcalDetIDSeedSC1','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise']))
    df['noiseSeedSC2_GT'] = df.set_index(['EcalDetIDSeedSC2','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise']))

    outfile_name = file.replace(".root", "_extra.root")
    print("@@@ Saving output file ", outfile_name)
    df.to_root(outfile_name, key = "extended", mode='w') # recreate mode


