import pandas as pd
import sys
import numpy as np
import dask.array as da

thismodule = sys.modules[__name__]


EBthreshold = 1.479
ADC2GEV_E = 0.060
ADC2GEV_B = 0.035

### selection defintions
def all(df):
	return df

#sub detectors
def EE(df):
	mask = (abs(df.etaSCEle1) > EBthreshold) & (abs(df.etaSCEle2) > EBthreshold)
	return mask

def EEplus(df):
	mask = (df.etaSCEle1 > EBthreshold) & (df.etaSCEle2 > EBthreshold)
	return mask

def EEminus(df):
	mask = (df.etaSCEle1 < - EBthreshold) & (df.etaSCEle2 < - EBthreshold)
	return mask

def EB(df):
	mask = ((abs(df.etaSCEle1) > EBthreshold) & (abs(df.etaSCEle2) < EBthreshold)) | ((abs(df.etaSCEle1) < EBthreshold) & (abs(df.etaSCEle2) > EBthreshold))
	return mask

def BB(df):
	mask = ((abs(df.etaSCEle1) < EBthreshold) & (abs(df.etaSCEle2) < EBthreshold))
	return mask

def E1(df):
	mask = abs(df.etaSCEle1) > EBthreshold
	return mask

def B1(df):
	mask = abs(df.etaSCEle1) < EBthreshold 
	return mask
def E2(df):
	mask = abs(df.etaSCEle2) > EBthreshold
	return mask
def B2(df):
	mask = abs(df.etaSCEle2) < EBthreshold
	return mask

# clean
def clean_ee(df):
	mask = ((abs(df.deltaT_ee) < 5)) 
	return mask

def clean_e1(df):
	mask = (abs(df.deltaT_e1_seeds) < 5) 
	return mask
def relAmp(df):
	mask =  (abs(df.amplitudeSeedSC1 - df.amplitudeSecondToSeedSC1) / (df.amplitudeSeedSC1 + df.amplitudeSecondToSeedSC1)  < 0.1)
	return mask
def central(df):
	mask = ((df.ySeedSC1 % 20 + 1) > 2) & ((df.ySeedSC1 % 20 + 1) < 18) & (abs(df.xSeedSC1) > 2) & (abs(df.ySeedSC1) < 24)
	return mask

def clean_e2(df):
	mask = (abs(df.deltaT_e2_seeds) < 5) & (df.chargeEle2 == 0)
	return mask
def relAmp2(df):
	mask =  (abs(df.amplitudeSeedSC2 - df.amplitudeSecondToSeedSC2) / (df.amplitudeSeedSC2 + df.amplitudeSecondToSeedSC2)  < 0.1)
	return mask
def central2(df):
	mask = ((df.ySeedSC2 % 20 + 1) > 2) & ((df.ySeedSC2 % 20 + 1) < 18) & (abs(df.xSeedSC2) > 2) & (abs(df.ySeedSC2) < 24)
	return mask

def longrun(df): #a 2017 run with >500/pb
	mask = (df.runNumber == 306125)
	return mask

def Early2018(df): 
	mask = (df.runNumber < 320000)
	return mask
def Late2018(df): 
	mask = (df.runNumber > 320000)
	return mask
	
#physics
def isOS(df):
	mask = ((abs(df.chargeEle1) == 1) & (df.chargeEle1 == - df.chargeEle2))
	return mask
def Zmass(df):
	#mask = (df.invMass > 85) & (df.invMass < 95)
	mask = (df.invMass > 60) & (df.invMass < 150)
	return mask
def HighR9(df):
	mask = (df.R9Ele1 > 0.94) & (df.R9Ele2 > 0.94)
	return mask
def baseline_ele(df):
	df = isOS(df)
	df = Zmass(df)
	df = HighR9(df)
	df = clean_ee(df)
	return df
def HighR9_e1(df):
	mask = (df.R9Ele1 > 0.94)
	return mask

def Run1Sel_e1(df):
	mask = (abs(df.amplitudeSeedSC1.div(df.amplitudeSecondToSeedSC1))< 1.2 & (abs(df.timeSeedSC1 - df.timeSecondToSeedSC1) < 5))
	return mask

def Run1Sel_ee(df):
	mask =  ((df.invMass > 60) & (df.invMass < 150) 
		& (df.gainSeedSC1 == 0) & (df.gainSeedSC2 == 0) & (abs(df.timeSeedSC1 - df.timeSeedSC2) < 5))
	return mask

def nosat(df):
	mask = (df.gainSeedSC1 == 0) & (df.gainSeedSC2 == 0)
	return mask

def AeffLow_ee(df):
	mask = df.effA_ee < 500
	return mask

def AeffLow_e1(df):
	mask = df.effA_e1_seeds < 500
	return mask

def AeffHigh_ee(df):
	mask = df.effA_ee >= 500
	return mask

def AeffHigh_e1(df):
	mask = df.effA_e1_seeds >= 500
	return mask


def AeffVHigh_ee(df):
	mask = df.effA_ee >= 700
	return mask

def AeffVHigh_e1(df):
	mask = df.effA_e1_seeds >= 700
	return mask


def Fill2018(df):
	mask = ((df.runNumber >= 319575) & (df.runNumber <= 319579))
	return mask

def Fill2017(df):
	mask = ((df.runNumber >= 306151) & (df.runNumber <= 306171))
	return mask

def Fill2016(df):
	mask = ((df.runNumber >= 275809) & (df.runNumber <= 275848))
	return mask

def sameRO(df):
	mask = ((df.iTTSeedSC1 == df.iTTSecondToSeedSC1) & (df.scSeedSC1 == df.scSecondToSeedSC1))
	return mask

def diffRO(df):
	mask = ((df.iTTSeedSC1 != df.iTTSecondToSeedSC1))
	return mask


def HighEta_e1(df):
	mask = ((df.etaEle1 > 1.3) & (df.etaEle1 < 1.5))
	return mask

def LowEta_e1(df):
	mask = ((df.etaEle1 < - 1.3) & (df.etaEle1 > - 1.5))
	return mask

#def Run1Sel_e1(df):
#	mask = (((df.ele1E) < 120) 
#			& (abs(df.energySeedSC1.div(df.energySecondToSeedSC1))< 1.2))
#	return mask
#
#def Run1Sel_ee(df):
#	mask = (((df.ele1E) < 120) 
#			& ((df.ele2E) < 120) 
#			& ((df.ele1E) > 10) 
#			& ((df.ele2E) > 10) 
#			& (df.invMass > 60) & (df.invMass < 150))
#	return mask

# amplitude slices
def Amp0to300(df):
	mask = (df.amplitudeSeedSC1 < 300) & (df.amplitudeSeedSC2 < 300)
	return mask

def Amp300to600(df):
	mask = (df.amplitudeSeedSC1 > 300) & (df.amplitudeSeedSC2 > 300) & (df.amplitudeSeedSC1 < 600) & (df.amplitudeSeedSC2 < 600)
	return mask

def Amp600to900(df):
	mask = (df.amplitudeSeedSC1 > 600) & (df.amplitudeSeedSC2 > 600) & (df.amplitudeSeedSC1 < 900) & (df.amplitudeSeedSC2 < 900)
	return mask

def Amp900to1200(df):
	mask = (df.amplitudeSeedSC1 > 900) & (df.amplitudeSeedSC2 > 900) & (df.amplitudeSeedSC1 < 1200) & (df.amplitudeSeedSC2 < 1200)
	return mask

def Amp1200to1500(df):
	mask = (df.amplitudeSeedSC1 > 1200) & (df.amplitudeSeedSC2 > 1200) & (df.amplitudeSeedSC1 < 1500) & (df.amplitudeSeedSC2 < 1500)
	return mask

def Amp1500to1800(df):
	mask = (df.amplitudeSeedSC1 > 1500) & (df.amplitudeSeedSC2 > 1500) & (df.amplitudeSeedSC1 < 1800) & (df.amplitudeSeedSC2 < 1800)
	return mask

def Amp1800to2500(df):
	mask = (df.amplitudeSeedSC1 > 1800) & (df.amplitudeSeedSC2 > 1800) & (df.amplitudeSeedSC1 < 2500) & (df.amplitudeSeedSC2 < 2500)
	return mask

def Amp2500toInf(df):
	mask = (df.amplitudeSeedSC1 > 2500) & (df.amplitudeSeedSC2 > 2500) 
	return mask

# geometry and electronics 
def SM34(df):
	mask = (df.scSeedSC1 == 34) | (df.scSeedSC2 == 34)
	return mask
def TT32(df):
	mask = (df.iTTSeedSC1 == 32) | (df.iTTSeedSC2 == 32)
	return mask
def TT32_e1(df):
	mask = (df.iTTSeedSC1 == 32) 
	return mask
def TR7(df):
	mask = (df.TRTSeedSC1 == 7) | (df.TRTSeedSC2 == 7)
	return mask
def TR8(df):
	mask = (df.TRTSeedSC1 == 8) | (df.TRTSeedSC2 == 8)
	return mask
def TR1_6(df):
	mask = (df.TRTSeedSC1 < 7 ) | (df.TRTSeedSC2 < 7)
	return mask

### functions
def apply_selection(df, full_selection):
        break_selections = full_selection.split("-")
        mask = None
        for selection_name in break_selections:
                if not hasattr(thismodule, selection_name):
                        print("### WARNING " + selection_name + " is not defined, skipping")
                        continue
                this_mask = getattr(thismodule, selection_name)(df)
                print(selection_name)
                #print (this_mask.compute())
                #print(df[this_mask].compute())
                mask = np.logical_and(mask, this_mask) if mask else this_mask
        print (mask)
        df = df[mask]
        return df
