# ECAL timing
Code for ECAL timing performance evaluation with [ECALElf](https://project-cms-ecal-calibration.web.cern.ch/project-cms-ecal-calibration/ECALELF_doc/dd/d7a/group__NTUPLESTRUCTURE.html) ntuples.

## Sumbit to lxplus condor system
```
python scripts/sumbit_condor.py -f <commands file> (-q <job_flavour> --tag <jobs_folder_name>) 	
```

Job flavours:
```
espresso     = 20 minutes
microcentury = 1 hour
longlunch    = 2 hours
workday      = 8 hours
tomorrow     = 1 day
testmatch    = 3 days
nextweek     = 1 week
```

