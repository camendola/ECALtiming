{
YEAR=$1 #"2016"
TAG="2020_4_6"


mkdir -p plots/$TAG/$YEAR

ssh camendol@lxplus.cern.ch "rm -rf /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}"
#rm plots/$TAG/$YEAR/*

ssh camendol@lxplus.cern.ch "mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}"

scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming
scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG
scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}


python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed}" --ylabel "Events" --sel all 
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed}" --ylabel "Events" --sel E1_clean_e1,B1_clean_e1 --norm --legend endcaps,barrel
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2}" --ylabel "Events" --sel all 
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2}" --ylabel "Events" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee --norm --legend EE,EB,BB
#
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel EB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel BB_clean_ee
###
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel clean_ee 
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel EB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel BB_clean_ee
#
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel all
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel BB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel all
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel BB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EB_clean_ee
##
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel all
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel EB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel BB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel all
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel EE_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel EB_clean_ee
python3 scripts/plot.py --tag $TAG --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel BB_clean_ee
#
python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Mean(t_{e1}-t_{e2})" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SC" --xlabel "e_{1} SC" --zlabel "Mean(t_{e1}-t_{e2})" --sel EEminus_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SC" --xlabel "e_{1} SC" --zlabel "Mean(t_{e1}-t_{e2})" --sel EEplus_clean_ee
##
python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SM" --xlabel "e_{1} SM" --zlabel "Std(t_{e1}-t_{e2})" --sel BB_clean_ee
#python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_scSeedSC2_vs_scSeedSC1 --ylabel "e_{2} SC" --xlabel "e_{1} SC" --zlabel "Std(t_{e1}-t_{e2})" --sel EEplus_clean_ee
##
python3 scripts/plot.py --tag $TAG --year $YEAR --name  mean_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Mean(t_{e1}-t_{e2})" --sel BB_clean_ee
##
python3 scripts/plot.py --tag $TAG --year $YEAR --name  std_deltaT_ee_iTTSeedSC2_vs_iTTSeedSC1 --ylabel "e_{2} iTT" --xlabel "e_{1} iTT" --zlabel "Std(t_{e1}-t_{e2})" --sel BB_clean_ee


scp plots/$TAG/$YEAR/*.png camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/$YEAR/
scp plots/$TAG/$YEAR/*.pdf camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/$YEAR/

echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/$TAG/$YEAR
}
