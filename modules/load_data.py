import pandas as pd
import uproot
import datetime


def load_chain(ntuples, tree_name, branch, firsthit = False):
    df = []
    for block in ntuples:
        print ('@ Loading file: ',block)
        file_content = uproot.open(block)
        tree = file_content[tree_name]
        df_b = tree.pandas.df(branch, flatten = False)
        if firsthit: df_b = df_b.stack().str[0].unstack()
        df.append(df_b)
        del df_b
        print (datetime.datetime.utcnow())
    print ('@@ Merging...')
    df = pd.concat(df, ignore_index=True)
    print ('@@ Merged ', datetime.datetime.utcnow())
    return df

def load_file(ntuple, tree_name, branch, firsthit = False):
    print ('@ Loading file: ',ntuple)
    file_content = uproot.open(ntuple)
    tree = file_content[tree_name]
    df_b = tree.pandas.df(branch, flatten = False)
    if firsthit: df_b = df_b.stack().str[0].unstack()
    return df_b