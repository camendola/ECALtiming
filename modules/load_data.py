import pandas as pd
import uproot
import datetime


def load_chain(ntuples, tree_name, branch = None, suffix = None):
    df = []
    for block in ntuples:
        if suffix: block.replace(".root", "_"+suffix+".root")
        print ('@ Loading file: ',block)
        file_content = uproot.open(block)
        tree = file_content[tree_name]
        if branch: 
            df_b = tree.pandas.df(branch, flatten = False)
        else: 
            df_b = tree.pandas.df(flatten = False) 
        df.append(df_b)
        del df_b, file_content
        print (datetime.datetime.utcnow())
    print ('@@ Merging...')
    df = pd.concat(df, ignore_index=True)
    print ('@@ Merged ', datetime.datetime.utcnow())
    return df

def load_file(ntuple, tree_name, branch):
    print ('@ Loading file: ',ntuple)
    file_content = uproot.open(ntuple)
    tree = file_content[tree_name]
    df_b = tree.pandas.df(branch, flatten = False)
    del file_content
    return df_b