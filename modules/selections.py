import pandas as pd
import sys

thismodule = sys.modules[__name__]


EBthreshold = 1.479
### selection defintions
def all(df):
	return df

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
def SM1(df):
	mask = (df.smEBSeedSC1 == 1) & (df.smEBSeedSC2 == 1)


def clean_ee(df):
	mask = abs(df.deltaT_ee) < 5
	return df[mask]

def clean_e1(df):
	mask = abs(df.deltaT_e1_seeds) < 5
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
