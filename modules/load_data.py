import pandas as pd
import uproot
import datetime


def load_chain(ntuples, tree_name, branch):
    df = []
    for block in ntuples:
        print ('@ Loading file: ',block)
        file_content = uproot.open(block)
        tree = file_content[tree_name]
        df_b = tree.pandas.df(branch)
        df.append(df_b)
        print (datetime.datetime.utcnow())
    print ('@ Merging...')
    df = pd.concat(df, ignore_index=True)
    print ('@ Merged ', datetime.datetime.utcnow())
    return df


