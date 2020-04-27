TAG="2020_4_6"
mkdir -p plots/$TAG/allYears

ssh camendol@lxplus.cern.ch "mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}"

scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming
scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG
scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}

ssh camendol@lxplus.cern.ch "rm -rf /eos/home-c/camendol/www/ECALtiming/$TAG/allYears"
ssh camendol@lxplus.cern.ch "mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/allYears"

scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/allYears

python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "Run number" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee --legend EE,EB,BB
python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2}}) [ns]" --xlabel "Run number" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee   --legend EE,EB,BB
#
python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee --legend EE,EB,BB
python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2}) [ns]" --xlabel "nPV" --sel EE_clean_ee,EB_clean_ee,BB_clean_ee   --legend EE,EB,BB
#
python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number" --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_e1_seeds_vs_runNumber --ylabel "Std(t_{seed}-t_{secondSeed}) [ns]" --xlabel "Run number"   --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#
python3 scripts/plotAllYears.py --tag $TAG --name mean_deltaT_e1_seeds_vs_nPV --ylabel "Mean(t_{seed}-t_{secondSeed}) [ns]" --xlabel "nPV" --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
python3 scripts/plotAllYears.py --tag $TAG --name std_deltaT_e1_seeds_vs_nPV --ylabel "Std(t_{seed}-t_{secondSeed}) [ns]" --xlabel "nPV"   --sel clean_e1,E1_clean_e1,B1_clean_e1 --legend all,endcap,barrel
#


scp plots/$TAG/allYears/*.png camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/allYears/
scp plots/$TAG/allYears/*.pdf camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/$TAG/allYears/


echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/$TAG/allYears
