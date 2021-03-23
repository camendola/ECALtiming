YEAR=2018
#TAG="staggered_2021_03_15"
TAG="staggered_2021_03_21"

mkdir -p plots/$TAG/${YEAR}


mkdir -p /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}

cp index.php /eos/home-c/camendol/www/ECALtiming
cp index.php /eos/home-c/camendol/www/ECALtiming/$TAG
cp index.php /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}

#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_ieta_B1" --xlabel "i#eta seed" --ylabel "e arrival time [ns]"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_ieta_B1" --xlabel "i#eta seed" --ylabel "e arrival time [ns]"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_ieta_B1" --xlabel "i#eta seed" --ylabel "e arrival time [ns]"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1" --xlabel "i#phi seed" --ylabel "e arrival time [ns]"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1" --xlabel "i#phi seed" --ylabel "e arrival time [ns]"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1" --xlabel "i#phi seed" --ylabel "e arrival time [ns]"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "side: #eta-"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta-"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaplus_eminus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaplus_eminus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaplus_eminus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_B1_etaminus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_B1_etaminus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_B1_etaminus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta-"

#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "fbrem_vs_eta_B1"   --xlabel "#eta SC"  --ylabel "fbrem" 
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "fbrem_vs_A_B1"     --xlabel "Amp seed" --ylabel "fbrem" 
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "eta_vs_A_B1"       --xlabel "Amp seed" --ylabel "#eta SC" 


#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_ieta_Amp400_fbrem20_B1" --add "time_vs_ieta_2_ele2_Amp400_ele2_fbrem20_B2"  --xlabel "i#eta seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_ieta_Amp400_fbrem20_B1" --add "time_vs_ieta_2_ele2_Amp400_ele2_fbrem20_B2"  --xlabel "i#eta seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_ieta_Amp400_fbrem20_B1" --add "time_vs_ieta_2_ele2_Amp400_ele2_fbrem20_B2"  --xlabel "i#eta seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_minus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_minus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_minus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; side: #eta-"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eplus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eplus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eplus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eplus"   --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eplus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eplus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e+; side: #eta-"
#
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eminus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eminus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaplus_eminus"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaplus_eminus"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta+"
#python studies/xtals_staggering/slices.py --tag $TAG --hist                --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eminus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median        --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eminus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta-"
#python studies/xtals_staggering/slices.py --tag $TAG --fit --median --hist --name "time_vs_iphi_Amp400_fbrem20_B1_etaminus_eminus" --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_etaminus_eminus" --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%; charge: e-; side: #eta-"


python studies/xtals_staggering/slices_selections.py --tag $TAG --median        --name "time_vs_iphi_Amp400_fbrem20_B1_XXX"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_XXX"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"

python studies/xtals_staggering/slices_selections.py --tag $TAG --fit        --name "time_vs_iphi_Amp400_fbrem20_B1_XXX"  --add "time_vs_iphi_2_ele2_Amp400_ele2_fbrem20_B2_XXX"  --xlabel "i#phi seed" --ylabel "e arrival time [ns]" --text "A > 400; fbrem < 20%"

cp plots/$TAG/${YEAR}${ERA}/*.png /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}/
cp plots/$TAG/${YEAR}${ERA}/*.pdf /eos/home-c/camendol/www/ECALtiming/$TAG/${YEAR}${ERA}/

echo [Alt + CMD + 2click]: http://camendol.web.cern.ch/camendol/ECALtiming/$TAG/${YEAR}${ERA}
