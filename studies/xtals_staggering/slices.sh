python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_ieta_B1" --xlabel "i#eta" --ylabel "e arrival time [ns]"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_ieta_B1" --xlabel "i#eta" --ylabel "e arrival time [ns]"
python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1" --xlabel "i#phi" --ylabel "e arrival time [ns]"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1" --xlabel "i#phi" --ylabel "e arrival time [ns]"

python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaplus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "side: #eta+"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaplus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "side: #eta+"
python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaminus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "side: #eta-"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaminus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "side: #eta-"

python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaplus_eplus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaplus_eplus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaminus_eplus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta-"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaminus_eplus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta-"

python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaplus_eminus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaplus_eminus"   --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e+; side: #eta+"
python studies/xtals_staggering/slices.py --fit --median        --name "time_vs_iphi_B1_etaminus_eminus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta-"
python studies/xtals_staggering/slices.py --fit --median --hist --name "time_vs_iphi_B1_etaminus_eminus"  --xlabel "i#phi" --ylabel "e arrival time [ns]" --text "charge: e-; side: #eta-"
