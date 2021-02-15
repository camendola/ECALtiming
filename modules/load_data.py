import pandas as pd
import uproot
import datetime
import gc
from root_pandas import read_root

import dask
import dask.dataframe as dd

from tqdm import tqdm

import ROOT

def load_read_root(ntuple, tree_name, branch):
    print("@ processing file " + ntuple)
    
    dfs=[]
    
    for df in read_root(ntuple, tree_name, columns = branch, chunksize=100000):
        #print(df)
        array_columns = []
        for n in range(df.shape[1]):
            if df.dtypes[n] == object:
                if df.infer_objects().dtypes[n] == object:
                    array_columns.append(df.columns[n])
    
            if df.dtypes[n] == bool:
                df[df.columns[n]] = pd.Series(df[df.columns[n]].astype(int), index=df.index)
        
        for n in array_columns:
            if df[n].str.len().iloc[0] == 2:
                df[[n+'1', n+'2']] = pd.DataFrame(df[n].tolist(), index=df.index)
            if df[n].str.len().iloc[0] == 3:
                df[[n+'1', n+'2', n+'3']] = pd.DataFrame(df[n].tolist(), index=df.index)
                df = df.drop(columns=n+'3')
                df = df.drop(columns=n)
        dfs.append(df)
        assert(not df.empty)
    
    df = pd.concat(dfs)         
    del dfs
    return df

def load_chain(ntuples, tree_name, branch = None, suffix = None, other_tree_name = None, other_branch = None):
    df_list = []
    for block in ntuples:
        print (block)
        #df_b = load_read_root(block, tree_name, branch)
        #df_b = load_hdf_file(block, tree_name, branch)
        df_b = load_file(block, tree_name, branch)
        #df_b = load_read_root(block, tree_name, branch)
        if suffix: 
            block = block.replace(".root", "_"+suffix+".root")
            df_b = load_file(block, other_tree_name, other_branch)
            #df_b_other = load_file(block, other_tree_name, other_branch).fillna(-999.)
            #df_chunk_list = []
            #for g, df_chunk in df_b.groupby('runNumber'):
            #    df_chunk = pd.merge(df_chunk, df_b_other, on='runNumber', how = 'inner')
            #    df_chunk_list.append(df_chunk)
            #del df_b_other
            #df_b = pd.concat(df_chunk_list, axis = 1)
            
            list_df_b_other = []
            list_df_chunk   = []
            for df_b_other in read_root(block, other_tree_name, columns = other_branch, chunksize=100000):
                df_b_chunk = pd.merge(df_b, df_b_other, on='eventTime', how = 'inner')
                list_df_b_other.append(df_b_other)
                list_df_chunk.append(df_b_chunk)
                print (list_df_chunk)
            df_b = pd.concat(list_df_chunk)
            del list_df_b_other, list_df_chunk
            gc.collect()
        df_list.append(df_b)
        print (datetime.datetime.utcnow())
    print ('@@ Merging...')
    df = pd.concat(df_list, ignore_index=True)
    #df = dd.concat(df_list)
    del df_list
    print ('@@ Merged ', datetime.datetime.utcnow())
    return df

def load_file(ntuple, tree_name, branch):
    print ('@ Loading file: ',ntuple)
    file_content = uproot.open(ntuple)
    tree = file_content[tree_name]
    
    df_b = tree.pandas.df(branch, flatten = False)
    del file_content
    return df_b


def load_hdf(ntuples_list, tree_name, branch, chunksize = None):
    df = dd.read_hdf(ntuples_list, key = tree_name, columns = branch)
    return df

@dask.delayed
def load_hdf_file(ntuple, tree_name, branch, chunksize = None):
    print ('@ Loading file: ',ntuple)
    df_b = dd.read_hdf(ntuple, key = tree_name, columns = branch)
    return df_b



    


