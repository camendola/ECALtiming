REFRUN=316995
#REFRUN=315252
#REFRUN=316998
#REFRUN=319265
#REFRUN=323391

#blue and green
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -e A 
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -e B
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -e C
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -e D
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -e D
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -e D
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -e D

#blue only
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -e A --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -e B --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -e C --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -e D --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -e D --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -e D --laser b -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -e D --laser b -r $REFRUN

#green only
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -e A --laser g -r $REFRUN 
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -e B --laser g -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -e C --laser g -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_0.root -e D --laser g -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_1.root -e D --laser g -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_2.root -e D --laser g -r $REFRUN
#./bin/recalelf.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_laser/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175_3.root -e D --laser g -r $REFRUN

### TOF
./bin/recalelf_TOF.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_TOF/snapshot_EGamma-Run2018A-ZSkim-19Nov2018-v2-315257-316995.root -e A 
#./bin/recalelf_TOF.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_TOF/snapshot_EGamma-Run2018B-ZSkim-19Nov2018-v2-317080-319310.root -e B 
#./bin/recalelf_TOF.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_TOF/snapshot_EGamma-Run2018C-ZSkim-19Nov2018-v2-319337-320065.root -e C 
#./bin/recalelf_TOF.exe -i /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_skimmed/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175.root -o /afs/cern.ch/work/c/camendol/ECALtimingData/Data_UL2018_106X_dataRun2_UL18_TOF/snapshot_EGamma-Run2018D-ZSkim-19Nov2018-v2-320500-325175.root -e D 
