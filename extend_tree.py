import sys, os
from array import array
import argparse
import numpy as np
import uproot
import pandas as pd
import modules.load_data as load_data
import modules.get_ids as get_ids
from root_pandas import to_root
from tqdm import tqdm
import gc
import functools

print = functools.partial(print, flush=True)
import psutil

process = psutil.Process(os.getpid())
print(str(float(process.memory_info().rss) / 1000000))  # in bytes

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", dest="file", default=None, help="file")
parser.add_argument("-y", "--year", dest="year", default=2017, help="year")
parser.add_argument(
    "-e", "--extra", dest="extra", default=None, help="extraCalib file "
)
parser.add_argument("-d", "--debug", dest="debug", default=False, action="store_true")

parser.add_argument("-n", "--noise", dest="noise", default=False, action="store_true")
parser.add_argument("-L", "--lumi", dest="lumi", default=False, action="store_true")
args = parser.parse_args()

branches = [
    #'noiseSeedSC',
    "eventNumber",
    "runNumber",
]

branches_extra = [
    "eventNumber",
    "rawIdRecHitSCEle1",
    "rawIdRecHitSCEle2",
]


branches_todrop = []

print("@@@ Loading files...")
file = args.file
file_extra = args.extra
if args.debug:
    file = "/afs/cern.ch/work/c/camendol/ecalelf/ntuples/13TeV/ALCARERECO/PromptReco2017_103X_EtaScaleupdatedSCregressionV3/DoubleEG-Run2017B-ZSkim-Prompt-v1/297046-297723/294927-306462_Prompt_v1/pedNoise/DoubleEG-Run2017B-ZSkim-Prompt-v1-297046-297723.root"
    file_extra = "/afs/cern.ch/work/c/camendol/ecalelf/ntuples/13TeV/ALCARERECO/PromptReco2017_103X_EtaScaleupdatedSCregressionV3/DoubleEG-Run2017B-ZSkim-Prompt-v1/297046-297723/294927-306462_Prompt_v1/pedNoise/extraCalibTree-DoubleEG-Run2017B-ZSkim-Prompt-v1-297046-297723.root"

if not os.path.isfile(file):
    print("Could not find file:", file)
    sys.exit()
if not os.path.isfile(file_extra):
    print("Could not find file:", file_extra)
    sys.exit()

df = load_data.load_file(file, "selected", branches)


initial_size = df.shape[0]
print(str(float(process.memory_info().rss) / 1000000))  #

extra_chunk_list = []
extratime_chunk_list = []

event_list = df.reset_index().eventNumber.drop_duplicates().sort_values().tolist()

for df_extra_chunk in tqdm(
    uproot.pandas.iterate(
        file_extra, "extraCalibTree", branches_extra, entrysteps=100000, flatten=False
    )
):

    df_extra_chunk = df_extra_chunk[
        df_extra_chunk["eventNumber"].isin(event_list)
    ]  # .sort_values(by=["eventNumber"]).reset_index()
    
    df_size1 = df_extra_chunk[].rawIdRecHitSCEle1.apply(
        lambda x: len(x))
    print(df_size1)
    print(df_size1.mean(), df_size1.std(), df_size1.max())
    df_size2 = df_extra_chunk.rawIdRecHitSCEle2.apply(
        lambda x: len(x))
    print(df_size2)
    print(df_size2.mean(), df_size2.std(), df_size2.max())
    df_extratime_chunk = df_extra_chunk["eventNumber"].astype("uint32")
    df_extra_chunk = df_extra_chunk.drop(columns=["eventNumber"])

    df_extra_seed_chunk = df_extra_chunk.stack().str[0].unstack().dropna().astype("int")
    df_extra_secondtoseed_chunk = (
        df_extra_chunk.stack().str[1].unstack().dropna().astype("int")
    )
    df_extra_chunk = pd.concat(
        [df_extra_seed_chunk, df_extra_secondtoseed_chunk], axis=1
    )

    del df_extra_seed_chunk, df_extra_secondtoseed_chunk
    df_extra_chunk.columns = [
        "rawIDSeedSC1",
        "rawIDSeedSC2",
        "rawIDSecondToSeedSC1",
        "rawIDSecondToSeedSC2",
    ]

    gc.collect()

    extra_chunk_list.append(df_extra_chunk)
    extratime_chunk_list.append(df_extratime_chunk)
    print(str(float(process.memory_info().rss) / 1000000))  #

df_extra = pd.concat(extra_chunk_list)
df_extratime = pd.concat(extratime_chunk_list)
del extra_chunk_list, extratime_chunk_list
df_extra = (
    pd.concat([df_extra, df_extratime], axis=1).reset_index().drop(columns="index")
)

del df_extratime

df = df.set_index("eventNumber")
df = df[~df.index.duplicated(keep="first")]

df_extra = df_extra.set_index("eventNumber")
df_extra = df_extra[~df_extra.index.duplicated(keep="first")]
df = pd.concat([df, df_extra], axis=1).reset_index()

types = {
    "rawIDSeedSC1": "int",
    "rawIDSeedSC2": "int",
    "rawIDSecondToSeedSC1": "int",
    "rawIDSecondToSeedSC2": "int",
}

df = df.dropna().astype(types)
del df_extra

gc.collect()
df_extra = pd.DataFrame()
df_extratime = pd.DataFrame()

print(str(float(process.memory_info().rss) / 1000000))  #
# -------------------
if args.lumi:
    print("@@@ Loading fill lumi table...")

    lumi_file = "/afs/cern.ch/work/c/camendol/fill_lumi/lumi_Run1_Run2_unixTime.dat"
    df_lumi_chunks = pd.read_csv(
        lumi_file, sep="\s+", usecols=[0, 1, 3, 6], comment="#", chunksize=5000
    )
    lumi_chunk_list = []
    for df_lumi_chunk in tqdm(df_lumi_chunks):
        df_lumi_chunk[["Run", "Fill"]] = df_lumi_chunk["Run:Fill"].str.split(
            ":", n=1, expand=True
        )
        df_lumi_chunk["LS"] = df_lumi_chunk["LS"].str.split(":", n=1, expand=True)[0]
        df_lumi_chunk = df_lumi_chunk[
            (df_lumi_chunk["Beam_Status"] == "STABLE_BEAMS")
        ].drop(columns=["Beam_Status", "Run:Fill"])
        lumi_chunk_list.append(df_lumi_chunk)
    # concat the list into dataframe
    df_lumi = pd.concat(lumi_chunk_list)
    del lumi_chunk_list
    group = (
        df_lumi.groupby("Run")
        .agg({"Recorded(/ub)": "sum", "LS": "count", "Fill": "first"})
        .reset_index()
    )
    df["Fill"] = df["runNumber"].map(group.astype("int").set_index("Run")["Fill"])
    df["LumiSections"] = df["runNumber"].map(group.astype("int").set_index("Run")["LS"])
    df["RecordedLumi"] = df["runNumber"].map(
        group.astype({"Run": "int"}).set_index("Run")["Recorded(/ub)"]
    )
    df["LumiInst"] = df["RecordedLumi"] / 23000

    print(str(float(process.memory_info().rss) / 1000000))  #
    del df_lumi, group

    gc.collect()
    df_lumi = pd.DataFrame()
    group = pd.DataFrame()
# ---------------------
print("before appending:", str(process.memory_info().rss / 1000000))  #
print("@@@ Appending DetIDs and geometric/electronic elements...")

df = get_ids.appendIdxs(df, "1").dropna()
df = get_ids.appendIdxs(df, "2").dropna()
df = get_ids.appendIdxs(df, "1", "SecondToSeed").dropna()
df = get_ids.appendIdxs(df, "2", "SecondToSeed").dropna()

print("after appending:", str(float(process.memory_info().rss) / 1000000))  #

if args.noise:
    print("@@@ Loading IOVs: EcalPedestals (Run 2 UL)")
    era = file.split("Run" + str(args.year))[1][0]
    print(process.memory_info().rss)  #
    print("@@@ Run" + str(args.year) + str(era))
    dump_file = (
        "/afs/cern.ch/work/c/camendol/ECALconditions_dumps/EcalPedestalsRun"
        + str(args.year)
        + str(era)
        + ".dat"
    )

    dump_chunk_list = []  # append each chunk df here
    df_dump_chunks = pd.read_csv(
        dump_file,
        chunksize=10000,
        sep="\s+",
        header=None,
        usecols=[4, 5, 7],
        names=["noise", "begin", "DetID"],
    )
    for df_dump_chunk in tqdm(df_dump_chunks):
        df_dump_chunk["begin"] = df_dump_chunk["begin"].values >> 32
        df_dump_chunk = df_dump_chunk.astype(
            {"noise": "float", "DetID": "int32", "begin": "int32"}
        )
        dump_chunk_list.append(df_dump_chunk)
    # concat the list into dataframe
    df_dump = pd.concat(dump_chunk_list)
    del dump_chunk_list

    df_dump["end"] = df_dump["begin"].shift(-1)
    df_dump.loc[max(df_dump.index), ["end"]] = 1591695307
    df_dump.astype({"end": "int32"})
    df_red = df_dump[["begin", "end"]].drop_duplicates()
    gc.collect()

    print(str(float(process.memory_info().rss) / 1000000))  #
    # ---------------------

    print("@@@ Matching IOVs...")
    print(str(float(process.memory_info().rss) / 1000000))

    chunk_list = []
    for g, df_chunk in df.groupby(np.arange(len(df)) // 50000):

        i, j = np.where(
            (df_chunk.eventTime.values[:, None] >= df_red.begin.values)
            & (df_chunk.eventTime.values[:, None] < df_red.end.values)
        )
        df_chunk = pd.DataFrame(
            np.column_stack([df_chunk.values[i], df_red.values[j]]),
            columns=df_chunk.columns.append(df_red.columns),
        )
        chunk_list.append(df_chunk)
        del i, j
        gc.collect()

        df = pd.concat(chunk_list)
        del chunk_list

        print("added begin end", str(float(process.memory_info().rss) / 1000000))

        print(df.shape[0])
        del df_red
        gc.collect()
        df_red = pd.DataFrame()
        print(process.memory_info().rss)  #
        print("@@@ Mapping Ecal pedestals by time and crystal...")
        chunk_list = []
        for g, df_chunk in df.groupby(np.arange(len(df)) // (initial_size / 20)):
            print(
                "@@@ Going over chunks...",
                str(float(process.memory_info().rss) / 1000000),
            )
            print(df_chunk.shape[0])
            df_chunk["noiseSeedSC1_GT"] = (
                df_chunk.set_index(["EcalDetIDSeedSC1", "begin"])
                .index.map(
                    (
                        df_dump[["DetID", "noise", "begin"]].set_index(
                            ["DetID", "begin"]
                        )["noise"]
                    )
                )
                .astype("float")
            )
            df_chunk["noiseSeedSC2_GT"] = (
                df_chunk.set_index(["EcalDetIDSeedSC2", "begin"])
                .index.map(
                    (
                        df_dump[["DetID", "noise", "begin"]].set_index(
                            ["DetID", "begin"]
                        )["noise"]
                    )
                )
                .astype("float")
            )
            df_chunk["noiseSecondToSeedSC1_GT"] = (
                df_chunk.set_index(["EcalDetIDSecondToSeedSC1", "begin"])
                .index.map(
                    (
                        df_dump[["DetID", "noise", "begin"]].set_index(
                            ["DetID", "begin"]
                        )["noise"]
                    )
                )
                .astype("float")
            )
            df_chunk["noiseSecondToSeedSC2_GT"] = (
                df_chunk.set_index(["EcalDetIDSecondToSeedSC2", "begin"])
                .index.map(
                    (
                        df_dump[["DetID", "noise", "begin"]].set_index(
                            ["DetID", "begin"]
                        )["noise"]
                    )
                )
                .astype("float")
            )
            chunk_list.append(df_chunk)
        df = pd.concat(chunk_list)
        del chunk_list
        print(df.shape[0])

        del df_dump
        gc.collect()

        df_dump = pd.DataFrame()

# don't save the quantities that exist already in the original tree
df = df.drop(columns=branches_todrop)
gc.collect()

outfile_name = file.replace(".root", "_extra.root")
print("@@@ Saving output file ", outfile_name)
#df.to_root(outfile_name, key="extended", mode="w")  # recreate mode

final_size = df.shape[0]
if initial_size > final_size:
    print("HEADS UP! final size is smaller than initial size")
    print("initial ", str(initial_size))
    print("final   ", str(final_size))
