#TAG="2020_6_9_dT"
TAG="2021_2_2"
mkdir -p plots/$TAG/allYears

#ssh camendol@lxplus.cern.ch "mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}"
##
#scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming
#scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG
#scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}
##
#ssh camendol@lxplus.cern.ch "rm -rf /eos/home-c/camendol/www/ECALtiming/$TAG/allYears"
#ssh camendol@lxplus.cern.ch "mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/allYears"
##
cp index.php /eos/home-c/camendol/www/ECALtiming/$TAG/allYears

python3 scripts/plotAllYears.py --tag $TAG --name effs_deltaT_ee_vs_runNumber --ylabel "eff #sigma (t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel BB_Run1Sel_ee --legend EB-EB --showeras --showhw
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee   --legend EE,EB,BB
##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee   --legend EE,EB,BB
##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number" --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_e1_seeds_vs_runNumber --ylabel "Std(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number"   --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number" --sel Run1Sel_e1_HighR9_e1,E1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1 --legend all,endcap,barrel
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_e1_seeds_vs_runNumber --ylabel "Std(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number"   --sel Run1Sel_e1_HighR9_e1,E1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1 --legend all,endcap,barrel

##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_nPV --ylabel "Mean(t_{seed}-t_{secondSeed}) [ns]" --xlabel "nPV" --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_e1_seeds_vs_nPV --ylabel "Std(t_{seed}-t_{secondSeed}) [ns]" --xlabel "nPV"   --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#

#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel EE_baseline_ele,EB_baseline_ele,BB_baseline_ele --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel  EE_baseline_ele,EB_baseline_ele,BB_baseline_ele   --legend EE,EB,BB
##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_baseline_ele,EB_baseline_ele,BB_baseline_ele --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_baseline_ele,EB_baseline_ele,BB_baseline_ele   --legend EE,EB,BB
####
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel EE_Run1Sel_ee_HighR9,EB_Run1Sel_ee_HighR9,BB_Run1Sel_ee_HighR9 --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name effs_deltaT_ee_vs_runNumber --ylabel "#sigma(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel  EE_Run1Sel_ee_HighR9,EB_Run1Sel_ee_HighR9,BB_Run1Sel_ee_HighR9   --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number"   --sel Run1Sel_e1_HighR9_e1,E1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1   --legend all,endcap,barrel
#python3 scripts/plotAllYears.py --tag $TAG --name effs_deltaT_e1_seeds_vs_runNumber --ylabel "#sigma(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel Run1Sel_e1_HighR9_e1,E1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1   --legend all,endcap,barrel
#
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel EE_clean_ee_isOS,EB_clean_ee_isOS,BB_clean_ee_isOS --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel  EE_clean_ee_isOS,EB_clean_ee_isOS,BB_clean_ee_isOS   --legend EE,EB,BB
##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee_isOS,EB_clean_ee_isOS,BB_clean_ee_isOS --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee_isOS,EB_clean_ee_isOS,BB_clean_ee_isOS   --legend EE,EB,BB
###
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel EE_clean_ee_HighR9,EB_clean_ee_HighR9,BB_clean_ee_HighR9 --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel  EE_clean_ee_HighR9,EB_clean_ee_HighR9,BB_clean_ee_HighR9   --legend EE,EB,BB
##
#python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee_HighR9,EB_clean_ee_HighR9,BB_clean_ee_HighR9 --legend EE,EB,BB
#python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee_HighR9,EB_clean_ee_HighR9,BB_clean_ee_HighR9   --legend EE,EB,BB

#python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_e1_seeds_vs_runNumber --ylabel "# events" --xlabel "Run number" --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_runNumber --ylabel "eff #sigma [ns]" --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 --legend ,, 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_runNumber   --ylabel "A_{eff}"         --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 --legend ,,
#
##python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_e1_seeds_vs_runNumber --ylabel "# events" --xlabel "Run number" --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_runNumber --ylabel "#sigma (#Delta t) [ns]" --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_runNumber   --ylabel "A_{eff}"                --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_runNumber --ylabel "#sigma (#Delta t) [ns]" --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffVHigh_e1 --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_runNumber   --ylabel "A_{eff}"                --xlabel "Run number"   --sel B1_Run1Sel_e1_HighR9_e1_AeffVHigh_e1 --legend " "
#
##python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_ee_vs_runNumber --ylabel "# events" --xlabel "Run number"          --sel BB_Run1Sel_ee_HighR9_AeffLow_ee 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_runNumber --ylabel "eff #sigma [ns]" --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffLow_ee --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_runNumber   --ylabel "A_{eff}"         --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffLow_ee --legend " "
#
##python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_ee_vs_runNumber --ylabel "# events" --xlabel "Run number"          --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_runNumber --ylabel "eff #sigma [ns]" --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_runNumber   --ylabel "A_{eff}"         --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_runNumber --ylabel "eff #sigma [ns]" --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffVHigh_ee --legend " "
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_runNumber   --ylabel "A_{eff}"         --xlabel "Run number"   --sel BB_Run1Sel_ee_HighR9_AeffVHigh_ee --legend " "

#python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_e1_seeds_vs_runNumber --ylabel "# events" --xlabel "Run number" --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_eventTime --ylabel "eff #sigma [ns]" --xlabel "Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 --legend ,, 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_eventTime   --ylabel "Mean A_{eff}"         --xlabel "Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffLow_e1 --legend ,,

#python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_e1_seeds_vs_eventTime --ylabel "# events" --xlabel "Event Time (timestamp)" --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_eventTime --ylabel "#sigma (#Delta t) [ns]" --xlabel "Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_eventTime   --ylabel "Mean A_{eff}"                --xlabel "Event Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffHigh_e1 --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_e1_seeds_vs_eventTime --ylabel "#sigma (#Delta t) [ns]" --xlabel "Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffVHigh_e1 --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_e1_seeds_vs_eventTime   --ylabel "Mean A_{eff}"                --xlabel "Time (timestamp)"   --sel B1_Run1Sel_e1_HighR9_e1_AeffVHigh_e1 --legend ,,
#
##python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_ee_vs_eventTime --ylabel "# events" --xlabel "Event Time (timestamp)"          --sel BB_Run1Sel_ee_HighR9_AeffLow_ee 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_eventTime --ylabel "eff #sigma [ns]" --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffLow_ee --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_eventTime   --ylabel "Mean A_{eff}"         --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffLow_ee --legend ,,
#
##python3 scripts/plotAllYears.py --tag $TAG --sigma --name size_deltaT_ee_vs_eventTime --ylabel "# events" --xlabel "Event Time (timestamp)"          --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee 
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_eventTime --ylabel "eff #sigma [ns]" --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_eventTime   --ylabel "Mean A_{eff}"         --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffHigh_ee --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name effs_deltaT_ee_vs_eventTime --ylabel "eff #sigma [ns]" --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffVHigh_ee --legend ,,
#python3 scripts/plotAllYears.py --tag $TAG --sigma --name mean_effA_ee_vs_eventTime   --ylabel "Mean A_{eff}"         --xlabel "Time (timestamp)"   --sel BB_Run1Sel_ee_HighR9_AeffVHigh_ee --legend ,,


cp -r plots/$TAG/allYears/*.png /eos/home-c/camendol/www/ECALtiming/$TAG/allYears/
cp -r plots/$TAG/allYears/*.pdf /eos/home-c/camendol/www/ECALtiming/$TAG/allYears/
#

echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/$TAG/allYears
