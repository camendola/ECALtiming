import pandas as pd
import os, sys
import json


directory = "/afs/cern.ch/user/c/camendol/ECALtiming/plots/staggered_2021_03_26_maps/" 

filelist = []
begin = []
iov = []

i = 0

df_eras = pd.read_csv("data/eras.dat", usecols = [0,1], names=["eras","first"], header = None, delimiter="\t")
df_eras = df_eras[(df_eras["eras"].str.contains("2018"))]

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        print(directory + filename)
        filelist.append(directory + filename)
        era = filename.split("_")[0][-1]
        print (era)
        print(df_eras)
        first = df_eras[(df_eras["eras"] == "2018"+era)]["first"]
        print (first)
        begin.append(first)
        iov.append("ERA_" + str(i))
        i += 1


df = pd.DataFrame({"file": filelist, "begin": begin, "iov": iov})
df["begin"] = df["begin"].astype("int")
df = df.reset_index().set_index("iov").drop(columns=["index"])
df = df[~df.index.duplicated(keep="first")]
print(df)

result = df.to_json(orient="index")

parsed = json.loads(result)
full = {}
full["IOVs"] = parsed
print(json.dumps(full, indent=4))

with open(directory + "ic-config.json", "w") as outfile:
    outfile.write(json.dumps(full, indent=4))

print("saved to " + directory + "ic-config.json")

