import sys,os
from array import array
import argparse
import numpy as np
import uproot
import pandas as pd
import modules.load_data as load_data
import modules.get_ids as get_ids
from root_pandas import to_root
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', dest = 'file',
                    default=None, help="file")
parser.add_argument('-y', '--year', dest = 'year',
                    default=2017, help="year")
parser.add_argument('-e', '--extra', dest = 'extra',
                    default=None, help="extraCalib file ")
parser.add_argument('-d', '--debug', dest= 'debug', default = False, action = 'store_true')
args =parser.parse_args()

branches = ['xSeedSC','ySeedSC',
        'noiseSeedSC', 
        'eventTime','runNumber']

branches_extra = ['XRecHitSCEle1','XRecHitSCEle2',
                  'YRecHitSCEle1','YRecHitSCEle2',
                  'ZRecHitSCEle1','ZRecHitSCEle2']

#drop at the end to avoid duplicates in the ordinary tree and the extended tree
branches_todrop = ['eventTime','runNumber']

print("@@@ Loading files...")
file = args.file
file_extra = args.extra
if args.debug:
    file = "/drf/projets/cms/ca262531/ecalelf/ntuples/13TeV/ALCARERECO/PromptReco2017_103X_EtaScaleupdatedSCregressionV3/DoubleEG-Run2017B-ZSkim-Prompt-v1/297046-297723/294927-306462_Prompt_v1/pedNoise/DoubleEG-Run2017B-ZSkim-Prompt-v1-297046-297723.root"
    file_extra = "/drf/projets/cms/ca262531/ecalelf/ntuples/13TeV/ALCARERECO/PromptReco2017_103X_EtaScaleupdatedSCregressionV3/DoubleEG-Run2017B-ZSkim-Prompt-v1/297046-297723/294927-306462_Prompt_v1/pedNoise/extraCalibTree-DoubleEG-Run2017B-ZSkim-Prompt-v1-297046-297723.root"

if not os.path.isfile(file):
    print ("Could not find file:", file)
    sys.exit()
if not os.path.isfile(file_extra):
    print ("Could not find file:", file_extra)
    sys.exit()

df = load_data.load_file(file, "selected", branches)
branches_split = ["xSeedSC","ySeedSC","noiseSeedSC"]
for br in branches_split:
    if br+"[1]" in df.columns:
        df[[br+'1', br+'2']] = df[[br+'[0]',br+'[1]']]
        branches_todrop.append(br+'1')
        branches_todrop.append(br+'2')
        df = df.drop(columns = [br+'[0]',br+'[1]', br+'[2]'] )


df_extra = load_data.load_file(file_extra, "extraCalibTree", branches_extra) # taking only iX, iY, iZ of first and second by energy
df_extra1 = df_extra.stack().str[0].unstack().fillna(-999).astype("int")
df_extra1 = df_extra1.drop(columns = ['XRecHitSCEle1','XRecHitSCEle2','YRecHitSCEle1','YRecHitSCEle2'])
df_extra1.columns = ["zSeedSC1","zSeedSC2"]
df_extra2 = df_extra.stack().str[1].unstack().fillna(-999).astype("int")
df_extra2.columns = ["xSecondToSeedSC1","xSecondToSeedSC2","ySecondToSeedSC1","ySecondToSeedSC2","zSecondToSeedSC1","zSecondToSeedSC2"]
del df_extra
df = pd.concat([df, df_extra1, df_extra2], axis=1) 
del df_extra1, df_extra2

#-------------------
print("@@@ Loading fill lumi table...")

lumi_file = "/drf/projets/cms/ca262531/fill_lumi/lumi_Run1_Run2_unixTime.dat"
df_lumi_chunks = pd.read_csv(lumi_file, sep='\s+', usecols = [0, 1, 3, 6], comment = '#', chunksize=10000)
lumi_chunk_list = []
for df_lumi_chunk in tqdm(df_lumi_chunks):
    df_lumi_chunk[["Run","Fill"]] = df_lumi_chunk["Run:Fill"].str.split(":", n = 1, expand = True) 
    df_lumi_chunk["LS"] = df_lumi_chunk["LS"].str.split(":", n = 1, expand = True)[0]
    df_lumi_chunk.drop(columns = ["Run:Fill"], inplace = True)
    df_lumi_chunk = df_lumi_chunk[(df_lumi_chunk["Beam_Status"]=="STABLE_BEAMS")]
    df_lumi_chunk = df_lumi_chunk.drop(columns = ["Beam_Status"])
    lumi_chunk_list.append(df_lumi_chunk)
# concat the list into dataframe 
df_lumi = pd.concat(lumi_chunk_list)
group = df_lumi.groupby("Run").agg({'Recorded(/ub)':'sum', 'LS':'count', 'Fill':'first'}).reset_index()
df['Fill'] = df['runNumber'].map(group.astype('int').set_index('Run')['Fill'])
df['LumiSections'] = df['runNumber'].map(group.astype('int').set_index('Run')['LS'])
df['RecordedLumi'] = df['runNumber'].map(group.astype({'Run':'int'}).set_index('Run')['Recorded(/ub)'])
df['RunLenght'] = 23*df['LumiSections'] # run lenght in seconds

del df_lumi, group

#---------------------

print("@@@ Appending DetIDs and geometric/electronic elements...")

df = get_ids.appendIdxs(df, "1")
df = get_ids.appendIdxs(df, "2")
df = get_ids.appendIdxs(df, "1", "SecondToSeed")
df = get_ids.appendIdxs(df, "2", "SecondToSeed")    


print("@@@ Loading IOVs: EcalPedestals (Run 2 UL)")

dump_file = "/drf/projets/cms/ca262531/ECALconditions_dumps/EcalPedestals"+str(args.year)+".dat"
#conddb_dumper -O EcalPedestals -t EcalPedestals_timestamp_UL_Run1_Run2_v1 -j -o /eos/home-c/camendol/ECAL_UL_dump/EcalPedestals.dat --b 6234602014664294400
dump_chunk_list = []  # append each chunk df here 
df_dump_chunks = pd.read_csv(dump_file, chunksize=500000, sep='\s+',  header=None, usecols = [4, 5, 7], names = ["noise","begin", "DetID"])
for df_dump_chunk in tqdm(df_dump_chunks):  
    df_dump_chunk = df_dump_chunk.astype({'noise':'float', 'DetID':'int32', 'begin':'int32'})
    df_dump_chunk["begin"] = (df_dump_chunk["begin"].values  >> 32)
    dump_chunk_list.append(df_dump_chunk)
# concat the list into dataframe 
df_dump = pd.concat(dump_chunk_list)
df_dump["end"] = df_dump["begin"].shift(-1)
df_dump.loc[max(df_dump.index), ["end"]] = 1591695307
df_dump.astype({'end':'int32'})

df_red = df_dump[["begin","end"]].drop_duplicates()
    
#---------------------

print ("@@@ Matching IOVs...")
time = df.eventTime.values
begin = df_red.begin.values
end = df_red.end.values

i, j = np.where((time[:, None] >= begin) & (time[:, None] < end))


df = pd.DataFrame(
    np.column_stack([df.values[i], df_red.values[j]]),
    columns=df.columns.append(df_red.columns)
)

del df_red

print ("@@@ Mapping Ecal pedestals by time and crystal...")

print(df.set_index(['EcalDetIDSeedSC1','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])))
print(df.set_index(['EcalDetIDSeedSC2','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float'))
df['noiseSeedSC1_GT'] = df.set_index(['EcalDetIDSeedSC1','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float')
df['noiseSeedSC2_GT'] = df.set_index(['EcalDetIDSeedSC2','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float')

print(df.set_index(['EcalDetIDSecondToSeedSC1','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])))
print(df.set_index(['EcalDetIDSecondToSeedSC2','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float'))
df['noiseSecondToSeedSC1_GT'] = df.set_index(['EcalDetIDSecondToSeedSC1','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float')
df['noiseSecondToSeedSC2_GT'] = df.set_index(['EcalDetIDSecondToSeedSC2','begin']).index.map((df_dump[['DetID','noise','begin']].set_index(['DetID','begin'])['noise'])).astype('float')


del df_dump

#don't save the quantities that exist already in the original tree
df = df.drop(columns = branches_todrop)

outfile_name = file.replace(".root", "_extra.root")
print("@@@ Saving output file ", outfile_name)
df.to_root(outfile_name, key = "extended", mode='w') # recreate mode
del df

