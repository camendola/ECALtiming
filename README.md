# ECAL timing
Code for ECAL timing performance evaluation with [ECALElf](https://project-cms-ecal-calibration.web.cern.ch/project-cms-ecal-calibration/ECALELF_doc/dd/d7a/group__NTUPLESTRUCTURE.html) ntuples.

## Skim ECALElf ntuples
Reduce ECALElf with common selections (e.g. Z mass) and with minimal set of variables

```
./bin/skim.exe -y <year>
```

or file by file

```
./bin/skim.exe -i <input> -o <output>
```

## Produce skimmed extraCalibTree ECALElf ntuples
Uses rechits variables stored in extraCalibTree to retrieve electronic and geometric indexes of the two crystals with highest deposited energy for each SC
```
python extend_tree.py -y <YEAR> -e <extracalibTree_ECALElf_file>      -f <main_ECALElf_file>
```
Optional: recorded luminosity; add noise from ECAL db. 

## Produce plots
Produce `.root` files with plots out of the skimmed ECALElf ntuples. 

Supported: 1D and 2D histograms, graphs, 2D maps

```
python main.py --tag <output_tag> --cfg config/<config_file> --year <year> (--e <era>)
```

Additional options:

`--extra`: merge extraCalibTree files	
	   
`--laser`: merge rECAL-ed files with laser timing calibration
	   
	   `--color`: which laser

## General: sumbit to lxplus condor system
```
python scripts/submit_condor.py -f <commands file> -p <commands pattern> (-q <job_flavour> --tag <jobs_folder_name>) 	
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




