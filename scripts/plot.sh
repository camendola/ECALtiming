{
YEAR=$1 #"2016"
ERA=$2
TAG="2021_1_26_laser_b_ref316995"

#TAG="2021_1_26_laser_b_ref316998"
#TAG="2021_1_26_laser_b_ref323391"
#TAG="GTnew_22Dec2020_2018"
#TAG="2021_2_2"
#TAG="2021_3_16_laser_g_ref316995"
mkdir -p plots/$TAG/${YEAR}${ERA}


mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}

cp index.php /eos/home-c/camendol/www/ECALtiming
cp index.php /eos/home-c/camendol/www/ECALtiming/$TAG
cp index.php /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}

#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed} [ns]" --ylabel "Events" --sel all 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed} [ns]" --ylabel "Events" --sel E1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1 --norm --legend endcaps,barrel
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed} [ns]" --ylabel "Events" --sel B1_clean_e1 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed} [ns]" --ylabel "Events" --sel B1_clean_e1_TT32_e1 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel all 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel EE_Run1Sel_ee_HighR9,EB_Run1Sel_ee_HighR9,BB_Run1Sel_ee_HighR9 --norm --legend EE,EB,BB
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel EE_baseline_ele,EB_baseline_ele,BB_baseline_ele --norm --legend EE,EB,BB
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel EE_clean_ee_isOS,EB_clean_ee_isOS,BB_isOS --norm --legend EE,EB,BB
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel EE_clean_ee_Zmass,EB_clean_ee_Zmass,BB_clean_ee_Zmass --norm --legend EE,EB,BB
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t [ns]" --sel clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t [ns]" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t [ns]" --sel EB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t [ns]" --sel BB_clean_ee
####
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t [ns]" --sel clean_ee 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t [ns]" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t [ns]" --sel EB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t [ns]" --sel BB_clean_ee
## 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_vs_effA_ee --xlabel "A_{eff}" --ylabel "#Delta t [ns]" --zlabel "#Events" --sel BB_Run1Sel_ee_HighR9 --logz 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_vs_effA_e1_seeds --xlabel "A_{eff}" --ylabel "#Delta t [ns]" --zlabel "#Events" --sel B1_Run1Sel_e1_HighR9_e1 --logz 

#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_vs_effA_ee --xlabel "A_{eff}" --ylabel "#Delta t [ns]" --zlabel "#Events"--sel BB_baseline_ele --logz 
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel all
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel EB_clean_ee

#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel EE_Run1Sel_ee_HighR9,EB_Run1Sel_ee_HighR9,BB_Run1Sel_ee_HighR9 --legend EE-EE,EE-EB,EB-EB --show_eras --show

#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_deltaT_ee_vs_runNumber --ylabel "#sigma eff [ns]" --xlabel "runNumber" --sel EE_Run1Sel_ee,EB_Run1Sel_ee,BB_Run1Sel_ee --legend EE-EE,EE-EB,EB-EB --showeras --show
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_deltaT_ee_vs_runNumber --ylabel "#sigma eff [ns]" --xlabel "runNumber" --sel BB_Run1Sel_ee --showeras --show --showhw

#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_deltaT_e1_seeds_vs_runNumber --ylabel "#sigma eff [ns]"     --xlabel "runNumber" --sel B1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1_diffRO,B1_Run1Sel_e1_HighR9_e1_sameRO --legend local,diffRO,sameRO

#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(#Delta t) [ns]" --xlabel "runNumber" --sel B1_Run1Sel_e1_HighR9_e1,B1_Run1Sel_e1_HighR9_e1_diffRO,B1_Run1Sel_e1_HighR9_e1_sameRO --legend local,diffRO,sameRO


#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel all
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel EB_clean_ee
###
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel all
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TR7
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TR8
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel all
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TR7
#python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel BB_clean_ee_TR8
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee --zmin -0.25 --zmax 0.17
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32 --zmin -1.2 --zmax 2.8
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass --zmin -0.25 --zmax 0.17
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 --zmin -0.25 --zmax 0.17

#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee --zmin 0.25 --zmax 0.82
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32 --zmin 0 --zmax 2.5
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass --zmin 0.25 --zmax 0.82
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 --zmin 0.25 --zmax 0.82

###
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 


#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass 
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 --zmin -0.3 --zmax 0.3

#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee --zmin -0.3 --zmax 0.3
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass --zmin -0.3 --zmax 0.3
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 --zmin -0.3 --zmax 0.3

#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee --zmin 0.4 --zmax 0.7
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_Zmass --zmin 0.4 --zmax 0.7
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_TRTSeedSC2_vs_TRTSeedSC1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_HighR9 --zmin 0.4 --zmax 0.7


#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_Zmass
#python3 scripts/plot.py --tag $TAG --year $YEAR --name iTTSeedSC2_vs_1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "#Events" --sel BB_clean_ee_HighR9

#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_Zmass
#python3 scripts/plot.py --tag $TAG --year $YEAR --name TRTSeedSC2_vs_1 --ylabel "e_{2} TRT" --xlabel "e_{1} TRT" --zlabel "#Events" --sel BB_clean_ee_HighR9

#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_Zmass
#python3 scripts/plot.py --tag $TAG --year $YEAR --name scSeedSC2_vs_1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "#Events" --logz --sel BB_clean_ee_HighR9

#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_TT32_SM34
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp0to300
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp300to600
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp600to900
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp900to1200
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp1200to1500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp1500to1800
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp1800to2500
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Amp2500toInf
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_baseline_ele
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_isOS
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_Zmass
#python3 scripts/plot.py --tag $TAG --year $YEAR --name VFESeedSC2_vs_1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "#Events" --sel BB_clean_ee_HighR9

#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32_SM34
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32_SM34
#
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_TT32
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_SM34
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee_SM34
#
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Mean(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_VFESeedSC2_vs_VFESeedSC1 --ylabel "e_{2} VFE" --xlabel "e_{1} VFE" --zlabel "Std(t_{e1}-t_{e2}) [ns]" --sel BB_clean_ee



##### RECAL COMPARISONS
### FULL YEAR
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber,mean_deltaT_ee_recal_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib   --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_calib1_vs_runNumber,mean_laser1_vs_runNumber --ylabel "Mean(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_deltaT_ee_vs_runNumber,effs_deltaT_ee_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_timeSeedSC1_vs_runNumber,effs_timeSeedSC1_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib   --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_calib1_vs_runNumber,effs_laser1_vs_runNumber --ylabel "Mean(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee,deltaT_ee_recal --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib # 
#
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber,mean_deltaT_ee_recal_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras #  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend ECALELF,ECALELF+rECAL --showeras #  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee_higheta --legend ECALELF,ECALELF+rECAL --showeras #  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras #  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_calib1_vs_runNumber,mean_laser1_vs_runNumber --ylabel "Mean(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras #  --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_deltaT_ee_vs_runNumber,effs_deltaT_ee_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras #  --era $ERA
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_timeSeedSC1_vs_runNumber,effs_timeSeedSC1_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras #  --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name effs_calib1_vs_runNumber,effs_laser1_vs_runNumber --ylabel "#sigma_{eff}(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib --showeras # --era $ERA
##
#python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee,deltaT_ee_recal --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel BBl_Run1Sel_ee --legend ECALELF,ECALELF+rECAL # 



python3 scripts/plot_green.py --tag $TAG --year $YEAR --name deltaT_ee,deltaT_ee_recal --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Norm. events" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --norm

#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber,mean_deltaT_ee_recal_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --showeras #  --era $ERA
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend ECALELF,ECALELF+rECAL_b,ECALELF+rECAL_g --showeras #  --era $ERA
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee_higheta --legend ECALELF,ECALELF+rECAL_b,ECALELF+rECAL_g --showeras #  --era $ERA
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name mean_timeSeedSC1_vs_runNumber,mean_timeSeedSC1_recal_vs_runNumber --ylabel "Mean(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --showeras #  --era $ERA
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name mean_calib1_vs_runNumber,mean_laser1_vs_runNumber --ylabel "Mean(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --showeras #  --era $ERA
##
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name effs_deltaT_ee_vs_runNumber,effs_deltaT_ee_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}-t_{e2}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --showeras #  --era $ERA
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name effs_timeSeedSC1_vs_runNumber,effs_timeSeedSC1_recal_vs_runNumber --ylabel "#sigma_{eff}(t_{e1}) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g --showeras #  --era $ERA
##
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name effs_calib1_vs_runNumber,effs_laser1_vs_runNumber --ylabel "#sigma_{eff}(t_{e1} calib) [ns]" --xlabel "runNumber" --sel BBl_Run1Sel_ee --legend physics_calib,laser_calib_b,laser_calib_g  --showeras # --era $ERA
##
#python3 scripts/plot_green.py --tag $TAG --year $YEAR --name deltaT_ee,deltaT_ee_recal --xlabel "t_{e1}-t_{e2} [ns]" --ylabel "Events" --sel BBl_Run1Sel_ee --legend ECALELF,ECALELF+rECAL_b,ECALELF+rECAL_g # 

cp plots/$TAG/${YEAR}${ERA}/*.png /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}/
cp plots/$TAG/${YEAR}${ERA}/*.pdf /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}/

echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/$TAG/${YEAR}${ERA}
}
