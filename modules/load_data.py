import pandas as pd
import uproot
import datetime
import gc

from tqdm import tqdm


def load_chain(
    ntuples,
    tree_name,
    branch=None,
    suffix=None,
    other_tree_name=None,
    other_branch=None,
):
    df_list = []
    for block in ntuples:
        print(block)
        df_b = load_file(block, tree_name, branch)
        df_list.append(df_b)
        print(datetime.datetime.utcnow())
    print("@@ Merging...")
    df = pd.concat(df_list, ignore_index=True)
    # df = dd.concat(df_list)
    del df_list
    print("@@ Merged ", datetime.datetime.utcnow())
    return df


def load_file(ntuple, tree_name, branch):
    print("@ Loading file: ", ntuple)
    file_content = uproot.open(ntuple)
    tree = file_content[tree_name]

    df_b = tree.pandas.df(branch, flatten=False)
    del file_content
    return df_b
