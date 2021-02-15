import pandas as pd
import sys
import numpy as np

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
	return df[mask]

def EEplus(df):
	mask = (df.etaSCEle1 > EBthreshold) & (df.etaSCEle2 > EBthreshold)
	return df[mask]

def EEminus(df):
	mask = (df.etaSCEle1 < - EBthreshold) & (df.etaSCEle2 < - EBthreshold)
	return df[mask]

def EB(df):
	mask = ((abs(df.etaSCEle1) > EBthreshold) & (abs(df.etaSCEle2) < EBthreshold)) | ((abs(df.etaSCEle1) < EBthreshold) & (abs(df.etaSCEle2) > EBthreshold))
	return df[mask]

def BB(df):
	mask = ((abs(df.etaSCEle1) < EBthreshold) & (abs(df.etaSCEle2) < EBthreshold))
	return df[mask]

def BBl(df):
        # exclude events with laser calibration == 1
	mask = ((abs(df.etaSCEle1) < EBthreshold) & (abs(df.etaSCEle2) < EBthreshold) & (df.timeSeedSC1_recal != 0.) & (df.timeSeedSC2_recal != 0.))
	return df[mask]

def E1(df):
	mask = abs(df.etaSCEle1) > EBthreshold
	return df[mask]

def B1(df):
	mask = abs(df.etaSCEle1) < EBthreshold 
	return df[mask]
def E2(df):
	mask = abs(df.etaSCEle2) > EBthreshold
	return df[mask]
def B2(df):
	mask = abs(df.etaSCEle2) < EBthreshold
	return df[mask]


# clean
def clean_ee(df):
	mask = ((abs(df.deltaT_ee) < 5)) 
	return df[mask]

def clean_e1(df):
	mask = (abs(df.deltaT_e1_seeds) < 5) 
	return df[mask]
def relAmp(df):
	mask =  (abs(df.amplitudeSeedSC1 - df.amplitudeSecondToSeedSC1) / (df.amplitudeSeedSC1 + df.amplitudeSecondToSeedSC1)  < 0.1)
	return df[mask]
def central(df):
	mask = ((df.ySeedSC1 % 20 + 1) > 2) & ((df.ySeedSC1 % 20 + 1) < 18) & (abs(df.xSeedSC1) > 2) & (abs(df.ySeedSC1) < 24)
	return df[mask]

def clean_e2(df):
	mask = (abs(df.deltaT_e2_seeds) < 5) & (df.chargeEle2 == 0)
	return df[mask]
def relAmp2(df):
	mask =  (abs(df.amplitudeSeedSC2 - df.amplitudeSecondToSeedSC2) / (df.amplitudeSeedSC2 + df.amplitudeSecondToSeedSC2)  < 0.1)
	return df[mask]
def central2(df):
	mask = ((df.ySeedSC2 % 20 + 1) > 2) & ((df.ySeedSC2 % 20 + 1) < 18) & (abs(df.xSeedSC2) > 2) & (abs(df.ySeedSC2) < 24)
	return df[mask]

def longrun(df): #a 2017 run with >500/pb
	mask = (df.runNumber == 306125)
	return df[mask]

def Early2018(df): 
	mask = (df.runNumber < 320000)
	return df[mask]
def Late2018(df): 
	mask = (df.runNumber > 320000)
	return df[mask]

	
#physics
def isOS(df):
	mask = ((abs(df.chargeEle1) == 1) & (df.chargeEle1 == - df.chargeEle2))
	return df[mask]
def Zmass(df):
	mask = (df.invMass > 85) & (df.invMass < 95)
	return df[mask]
def HighR9(df):
	mask = (df.R9Ele1 > 0.94) & (df.R9Ele2 > 0.94)
	return df[mask]
def baseline_ele(df):
	df = isOS(df)
	df = Zmass(df)
	df = HighR9(df)
	df = clean_ee(df)
	return df
def HighR9_e1(df):
	mask = (df.R9Ele1 > 0.94)
	return df[mask]

def Run1Sel_e1(df):
        mask = (((df.amplitudeSeedSC1 * np.where(abs(df.etaSCEle1) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120) 
                & ((df.amplitudeSecondToSeedSC1 * np.where(abs(df.etaSCEle1) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120)
                & abs(df.amplitudeSeedSC1.div(df.amplitudeSecondToSeedSC1))< 1.2)
        
        return df[mask]

def Run1Sel_e2(df):
        mask = (((df.amplitudeSeedSC2 * np.where(abs(df.etaSCEle2) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120) 
                & ((df.amplitudeSecondToSeedSC2 * np.where(abs(df.etaSCEle2) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120)
                & abs(df.amplitudeSeedSC2.div(df.amplitudeSecondToSeedSC2))< 1.2)
        
        return df[mask]

def Run1Sel_ee(df):
        mask = (((df.amplitudeSeedSC1 * np.where(abs(df.etaSCEle1) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120)
                & ((df.amplitudeSeedSC2 * np.where(abs(df.etaSCEle2) > EBthreshold, ADC2GEV_E, ADC2GEV_B)) < 120)
                & (abs(df.timeSeedSC1 - df.timeSeedSC2) < 5))
                #& (df.invMass > 60) & (df.invMass < 150))
       
        #mask =  ((df.invMass > 60) & (df.invMass < 150)
        #        & (abs(df.timeSeedSC1 - df.timeSeedSC2) < 5))
        return df[mask]

def loweta(df):
        mask = (abs(df.etaSCEle1) < 0.4)
        return df[mask]

def higheta(df):
        mask = (abs(df.etaSCEle1) > 1.2)
        return df[mask]

def AeffLow_ee(df):
	mask = df.effA_ee < 500
	return df[mask]

def AeffLow_e1(df):
	mask = df.effA_e1_seeds < 500
	return df[mask]

def AeffHigh_ee(df):
	mask = df.effA_ee >= 500
	return df[mask]

def AeffHigh_e1(df):
	mask = df.effA_e1_seeds >= 500
	return df[mask]


def AeffVHigh_ee(df):
	mask = df.effA_ee >= 700
	return df[mask]

def AeffVHigh_e1(df):
	mask = df.effA_e1_seeds >= 700
	return df[mask]


def Fill2018(df):
	mask = ((df.runNumber >= 319575) & (df.runNumber <= 319579))
	return df[mask]

def Fill2017(df):
	mask = ((df.runNumber >= 306151) & (df.runNumber <= 306171))
	return df[mask]

def Fill2016(df):
	mask = ((df.runNumber >= 275809) & (df.runNumber <= 275848))
	return df[mask]

def sameRO(df):
	mask = ((df.iTTSeedSC1 == df.iTTSecondToSeedSC1) & (df.scSeedSC1 == df.scSecondToSeedSC1))
	return df[mask]

def diffRO(df):
	mask = ((df.iTTSeedSC1 != df.iTTSecondToSeedSC1))
	return df[mask]


def HighEta_e1(df):
	mask = ((df.etaEle1 > 1.3) & (df.etaEle1 < 1.5))
	return df[mask]

def LowEta_e1(df):
	mask = ((df.etaEle1 < - 1.3) & (df.etaEle1 > - 1.5))
	return df[mask]

#def Run1Sel_e1(df):
#	mask = (((df.ele1E) < 120) 
#			& (abs(df.energySeedSC1.div(df.energySecondToSeedSC1))< 1.2))
#	return df[mask]
#
#def Run1Sel_ee(df):
#	mask = (((df.ele1E) < 120) 
#			& ((df.ele2E) < 120) 
#			& ((df.ele1E) > 10) 
#			& ((df.ele2E) > 10) 
#			& (df.invMass > 60) & (df.invMass < 150))
#	return df[mask]

# amplitude slices
def Amp0to300(df):
	mask = (df.amplitudeSeedSC1 < 300) & (df.amplitudeSeedSC2 < 300)
	return df[mask]

def Amp300to600(df):
	mask = (df.amplitudeSeedSC1 > 300) & (df.amplitudeSeedSC2 > 300) & (df.amplitudeSeedSC1 < 600) & (df.amplitudeSeedSC2 < 600)
	return df[mask]

def Amp600to900(df):
	mask = (df.amplitudeSeedSC1 > 600) & (df.amplitudeSeedSC2 > 600) & (df.amplitudeSeedSC1 < 900) & (df.amplitudeSeedSC2 < 900)
	return df[mask]

def Amp900to1200(df):
	mask = (df.amplitudeSeedSC1 > 900) & (df.amplitudeSeedSC2 > 900) & (df.amplitudeSeedSC1 < 1200) & (df.amplitudeSeedSC2 < 1200)
	return df[mask]

def Amp1200to1500(df):
	mask = (df.amplitudeSeedSC1 > 1200) & (df.amplitudeSeedSC2 > 1200) & (df.amplitudeSeedSC1 < 1500) & (df.amplitudeSeedSC2 < 1500)
	return df[mask]

def Amp1500to1800(df):
	mask = (df.amplitudeSeedSC1 > 1500) & (df.amplitudeSeedSC2 > 1500) & (df.amplitudeSeedSC1 < 1800) & (df.amplitudeSeedSC2 < 1800)
	return df[mask]

def Amp1800to2500(df):
	mask = (df.amplitudeSeedSC1 > 1800) & (df.amplitudeSeedSC2 > 1800) & (df.amplitudeSeedSC1 < 2500) & (df.amplitudeSeedSC2 < 2500)
	return df[mask]

def Amp2500toInf(df):
	mask = (df.amplitudeSeedSC1 > 2500) & (df.amplitudeSeedSC2 > 2500) 
	return df[mask]

# geometry and electronics 
def SM34(df):
	mask = (df.scSeedSC1 == 34) | (df.scSeedSC2 == 34)
	return df[mask]
def TT32(df):
	mask = (df.iTTSeedSC1 == 32) | (df.iTTSeedSC2 == 32)
	return df[mask]
def TT32_e1(df):
	mask = (df.iTTSeedSC1 == 32) 
	return df[mask]
def TR7(df):
	mask = (df.TRTSeedSC1 == 7) | (df.TRTSeedSC2 == 7)
	return df[mask]
def TR8(df):
	mask = (df.TRTSeedSC1 == 8) | (df.TRTSeedSC2 == 8)
	return df[mask]
def TR1_6(df):
	mask = (df.TRTSeedSC1 < 7 ) | (df.TRTSeedSC2 < 7)
	return df[mask]

### functions
def apply_selection(df, full_selection):
	break_selections = full_selection.split("-")
	for selection_name in break_selections:
		if not hasattr(thismodule, selection_name):
				print("### WARNING " + selection_name + " is not defined, skipping")
				continue
		df = getattr(thismodule, selection_name)(df)
	return df
