# if [ ! -d "/eos/home-c/camendol/www" ]; then
#     kinit camendol@CERN.CH
#     /opt/exp_soft/cms/t3/eos-login -username camendol
# fi

YEAR=2016
target='/eos/home-c/camendol/www/ECALtiming/2020_03_25_$YEAR'

mdkir plots/2020_03_25_$YEAR_test
ssh camendol@lxplus.cern.ch "mkdir /eos/home-c/camendol/www/ECALtiming/2020_03_25_2016_test"

scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming
scp index.php camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/2020_03_25_$YEAR_test

python3 scripts/plot.py --year $YEAR --name deltaT_e1_seeds --xlabel "e t_{seed}-t_{secondSeed}" --ylabel "Events" --sel all --tag test
python3 scripts/plot.py --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2}" --ylabel "Events" --sel all 
python3 scripts/plot.py --year $YEAR --name deltaT_ee --xlabel "t_{e1}-t_{e2}" --ylabel "Events" --sel EE,EB,BB --norm

#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel all 
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel EE
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel EB
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaEta_ee --xlabel "#Delta #eta" --ylabel "#Delta t" --sel BB
##
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel all 
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel EE
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel EB
#python3 scripts/plot.py --year $YEAR --name deltaT_ee_vs_deltaPhi_ee --xlabel "#Delta #phi" --ylabel "#Delta t" --sel BB

python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel all
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EE
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel BB
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_runNumber --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EB
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel all
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EE
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel BB
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_runNumber --ylabel "Std(t_{e1}-t_{e2})" --xlabel "runNumber" --sel EB
#
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel all
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel EE
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel EB
python3 scripts/plot.py --year $YEAR --name mean_deltaT_ee_vs_nPV --ylabel "Mean(t_{e1}-t_{e2})" --xlabel "nPV" --sel BB
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel all
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel EE
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel EB
python3 scripts/plot.py --year $YEAR --name std_deltaT_ee_vs_nPV --ylabel "Std(t_{e1}-t_{e2})" --xlabel "nPV" --sel BB
#
python3 scripts/plot.py --year $YEAR --name mean_deltaT_e1_seeds_vs_runNumber --ylabel "Mean(t_{seed}-t_{secondSeed})" --xlabel "runNumber" --sel all
python3 scripts/plot.py --year $YEAR --name std_deltaT_e1_seeds_vs_runNumber --ylabel "Std(t_{seed}-t_{secondSeed})" --xlabel "runNumber" --sel all
#
python3 scripts/plot.py --year $YEAR --name mean_deltaT_e1_seeds_vs_nPV --ylabel "Mean(t_{seed}-t_{secondSeed})" --xlabel "nPV" --sel all
python3 scripts/plot.py --year $YEAR --name std_deltaT_e1_seeds_vs_nPV --ylabel "Std(t_{seed}-t_{secondSeed})" --xlabel "nPV" --sel all

scp plots/2020_03_25_$YEAR_test/*.png camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/2020_03_25_$YEAR_test/
scp plots/2020_03_25_$YEAR_test/*.pdf camendol@lxplus.cern.ch:/eos/home-c/camendol/www/ECALtiming/2020_03_25_$YEAR_test/


echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/2020_03_25_$YEAR_test
