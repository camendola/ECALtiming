import pandas as pd
import numpy as np

df_eras = pd.read_csv("eras.dat", sep="\t", header =None)
df_eras.columns = ["RunEra", "beginRun", "endRun", "beginTime","endTime"]
df_eras["beginTime"]  = pd.to_datetime(df_eras["beginTime"] , format='%Y-%m-%d')
df_eras["endTime"]    = pd.to_datetime(df_eras["endTime"]   , format='%Y-%m-%d')
df_eras["beginTimestamp"] = df_eras.beginTime.values.astype(np.int64) // 10 ** 9
df_eras["endTimestamp"]   = df_eras.endTime.values.astype(np.int64)   // 10 ** 9
df_eras["beginTimestampLong"] = df_eras.beginTimestamp.values.astype(np.int64) << 32
df_eras["endTimestampLong"]   = df_eras.endTimestamp.values.astype(np.int64) << 32

print(df_eras)

df_eras2016 = df_eras[df_eras["RunEra"].str.contains("2016")]
df_eras2017 = df_eras[df_eras["RunEra"].str.contains("2017")]
df_eras2018 = df_eras[df_eras["RunEra"].str.contains("2018")]

print()
print("****2016")

for index, row in df_eras2016.iterrows():
    print("conddb_dumper -O EcalPedestals -t EcalPedestals_timestamp_UltraLegacy_2016_v1 -j -o /eos/home-c/camendol/ECAL_UL_dump/EcalPedestals"+str(row["RunEra"])+".dat -b "+str(row["beginTimestampLong"])+" -e "+str(row["endTimestampLong"]))

print()
print("****2017")
for index, row in df_eras2017.iterrows():
    print("conddb_dumper -O EcalPedestals -t EcalPedestals_timestamp_UltraLegacy_2017_v1 -j -o /eos/home-c/camendol/ECAL_UL_dump/EcalPedestals"+str(row["RunEra"])+".dat -b "+str(row["beginTimestampLong"])+" -e "+str(row["endTimestampLong"]))

print()
print("****2018")
for index, row in df_eras2018.iterrows():
    print("conddb_dumper -O EcalPedestals -t EcalPedestals_timestamp_2018_12February2019_collisions_blue_laser -j -o /eos/home-c/camendol/ECAL_UL_dump/EcalPedestals"+str(row["RunEra"])+".dat -b "+str(row["beginTimestampLong"])+" -e "+str(row["endTimestampLong"]))

