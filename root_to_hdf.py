#!/usr/bin/env python

import argparse
parser = argparse.ArgumentParser(description='Convert ROOT TTree to hdf5 container.')
parser.add_argument('--year', type = int, dest='year', help='which year', default=2016)
parser.add_argument('-e', '--era', default = None, help="era")
parser.add_argument('--extra', dest='extra', help='is it extra tree', default=False, action='store_true')
parser.add_argument('--chunk-size', required=False, type=int, default=100000, help="Number of entries per iteration")
args = parser.parse_args()

import os
import uproot
import pandas
from root_pandas import read_root
from tqdm import tqdm


year = args.year 
fileList = "filelists/ECALELF_Run2UL/Data_UL2016.log"

if year ==2017: 
    fileList = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log"

if year ==2018: 
    fileList = "filelists/ECALELF_Run2UL/Data_UL2018_106X_dataRun2_UL18.log"


dest = "/afs/cern.ch/work/c/camendol/ECALtimingData/"
dest_dir = fileList.split("/")[-1].replace(".log", "")
dest = dest + dest_dir + "/"
print("Will save to  '{}'".format(dest))
if not os.path.exists(dest):
    os.makedirs(dest)


files = [line. rstrip('\n') for line in open(fileList)]
newfiles = []
if args.era:
    for file in files:
        if str(args.year)+args.era in file:
            newfiles.append(file)
    files = newfiles

tree_name = "selected"
if args.extra: 
    files = [line. rstrip('\n').replace(".root","_extra.root") for line in open(fileList)]
    tree_name = "extended"

print (files)

files = files[:1]
for name in files:
    print("@ processing file " + name)
    with uproot.open(name) as file:
        tree = file[tree_name]
        events = tree.numentries

    first_pass = True
    boolean_columns = ""

    with tqdm(total=events, unit='entries') as pbar:
        for df in read_root(name, tree_name, chunksize=args.chunk_size):
            array_columns = []
            for n in range(df.shape[1]):
                if df.dtypes[n] == object:
                    if df.infer_objects().dtypes[n] == object:
                        array_columns.append(df.columns[n])
        
                if df.dtypes[n] == bool:
                    df[df.columns[n]] = pandas.Series(df[df.columns[n]].astype(int), index=df.index)

                        
            for n in array_columns:
                if df[n].str.len().iloc[0] == 2:
                    df[[n+'1', n+'2']] = pandas.DataFrame(df[n].tolist(), index=df.index)  
                    
                if df[n].str.len().iloc[0] == 3:
                    df[[n+'1', n+'2', n+'3']] = pandas.DataFrame(df[n].tolist(), index=df.index)    
                    df = df.drop(columns=n+'3')
                    df = df.drop(columns=n)
            name = name.split("/")[-1]
            df.infer_objects().to_hdf(dest+name.replace(".root",".h5"),  tree_name, complevel=1, complib='zlib', append ='True')
            pbar.update(df.shape[0])
            first_pass = False

    print("All entries for '{}', tree '{}' have been processed.".format(name, tree_name))
print("All files are processed")
