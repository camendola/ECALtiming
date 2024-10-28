import pandas as pd
import numpy as np
import ecalic


df_TRT = pd.read_csv("modules/utils/TRT.csv", comment="#")
df_TRT["TTs"] = df_TRT["TTs"].str.split()
df_TRT = (
    df_TRT.join(df_TRT.TTs.apply(pd.Series))
    .drop("TTs", 1)
    .set_index([u"Subdetector", u"FED", u"TR", u"Dee", u"Sector", u"DRing"])
    .stack()
    .reset_index()
    .drop("level_6", 1)
    .rename(columns={0: "TTs"})
)
df_TRT = df_TRT.apply(lambda x: x.str.strip() if x.dtype == "object" else x)


def twos_comp(val, bits):
    return np.where(val < 0, val + (1 << bits), val)


# https://github.com/cms-sw/cmssw/blob/master/DataFormats/EcalDetId/interface/EcalSubdetector.h
DetMask = 0xF
# ECAL = 1
SubdetMask = 0x7
# EB = 1
# EE = 2

# BARREL
# https://github.com/cms-sw/cmssw/blob/master/DataFormats/EcalDetId/interface/EBDetId.h
def getEBDetId(ieta, iphi):
    ieta = ieta.astype("int")
    iphi = iphi.astype("int")
    id_det = ((3 & DetMask) << 28) | ((1 & SubdetMask) << 25)
    id = (
        (
            np.where(
                (ieta.values > 0), (0x10000 | (ieta.values << 9)), (-ieta.values) << 9
            )
        )
        | (iphi.values & 0x1FF)
    ).astype("int")
    id = twos_comp(id, 17).astype("int")
    id = id_det | id
    return id


def geticEB(ieta, iphi, positiveZ):
    crystalsInPhi = 20  # per SM
    crystalsInEta = 85  # per SM
    crystalsPerSM = 1700
    ie = abs(ieta) - 1
    ic = (ie * crystalsInPhi) + np.where(
        positiveZ,
        (crystalsInPhi - ((iphi - 1) % crystalsInPhi)),
        ((iphi - 1) % crystalsInPhi + 1),
    )
    return ic


def getSM(iphi, positiveZ):
    crystalsInPhi = 20  # per SM
    id = (iphi - 1) / crystalsInPhi + 1
    id = id #.astype("int")
    return np.where(positiveZ, id, id + 18)


def VFE_EB(ieta):
    ie = abs(ieta)
    ieInTT = (ie.astype("int") % 17) + 1
    return (ieInTT.astype("int") % 5) + 1


def TRT(iTT, isEB):
    TR = np.where(
        isEB,
        iTT.fillna(1)
        .astype("int")
        .map(
            (
                df_TRT[(df_TRT["Subdetector"] == "BARREL")][["TTs", "TR"]]
                .astype("int")
                .set_index(["TTs"])["TR"]
            )
        ),
        np.nan,
    )
    return TR


# ENDCAPS
iYoffset = [0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0]
np_iYoffset = np.asarray(iYoffset)
QuadColLimits = [0, 8, 17, 27, 36, 45, 54, 62, 70, 76, 79]
np_QuadColLimits = np.asarray(QuadColLimits)

# https://github.com/cms-sw/cmssw/blob/master/DataFormats/EcalDetId/interface/EEDetId.h
def getEEDetId(ix, iy, positiveZ):
    id = ((3 & DetMask) << 28) | ((2 & SubdetMask) << 25)
    id = (
        id
        | (iy.values & 0x7F)
        | ((ix.values & 0x7F) << 7)
        | np.where(positiveZ, 0x4000, 0)
    )
    return id


def iquadrant(ix, iy):
    return np.where(
        ix.values > 50, np.where(iy.values > 50, 1, 4), np.where(iy.values > 50, 2, 3)
    )


def getSC(ix, iy, isEB):

    iquad = np.where(isEB, 3, iquadrant(ix, iy))

    jx = np.where(isEB, 1, 1 + (ix - 1) / 5)
    jy = np.where(isEB, 1, 1 + (iy - 1) / 5)
    jx = jx.astype("int")
    jy = jy.astype("int")

    icol = np.where((iquad == 1) | (iquad == 4), jx - 10, 11 - jx)
    irow = np.where((iquad == 1) | (iquad == 2), jy - 10, 11 - jy)
    icol = icol.astype("int")
    icol = np.where(icol < 11, icol, int(1))

    maxCinSC = 316
    nSCinQuadrant = maxCinSC / 4
    # max SC = 316

    yoff = np_iYoffset[icol.astype("int")]
    qOff = nSCinQuadrant * (iquad - 1)
    iscOne = np_QuadColLimits[icol.astype("int") - 1] + irow - yoff

    return np.where(
        yoff >= irow,
        -1,
        np.where(np_QuadColLimits[icol.astype("int")] < iscOne, -2, iscOne + qOff),
    ).astype("int")


def appendIdxs(df, pair_idx, seed="Seed"):

    detID = "rawID" + seed + "SC" + pair_idx
    ecal = ecalic.icCMS().iov

    ecal = ecal.reset_index().set_index(["cmsswId"])

    df["iTT" + seed + "SC" + pair_idx] = df.set_index([detID]).index.map(ecal.ccu)

    df["iX" + seed + "SC" + pair_idx] = df.set_index([detID]).index.map(ecal["ix"])
    df["iY" + seed + "SC" + pair_idx] = df.set_index([detID]).index.map(ecal.iy)

    FED = df.set_index([detID]).index.map(ecal.FED)
    isEB = (FED > 609) & (FED < 646)

    ##positiveZ()
    ##https://github.com/cms-sw/cmssw/blob/master/DataFormats/EcalDetId/interface/EBDetId.h#L76
    ##https://github.com/cms-sw/cmssw/blob/master/DataFormats/EcalDetId/interface/EEDetId.h#L174
    positiveZ = np.where(
        isEB, df[detID].values & 0x10000, df[detID].values & 0x4000
    ).astype("int")
    df["sc" + seed + "SC" + pair_idx] = np.where(
        isEB,
        getSM(df["iX" + seed + "SC" + pair_idx], positiveZ),
        getSC(
            df["iX" + seed + "SC" + pair_idx], df["iY" + seed + "SC" + pair_idx], isEB
        ),
    )  # SM for EB, SC for EE

    # df["VFE"+seed+"SC"+pair_idx]      = np.where(isEB, VFE_EB(df[ieta]),     np.nan)
    # df["TRT"+seed+"SC"+pair_idx]      = np.where(isEB, TRT(df["iTT"+seed+"SC"+pair_idx], isEB),     np.nan)

    df = df.drop(columns=["iX" + seed + "SC" + pair_idx, "iY" + seed + "SC" + pair_idx])
    return df
