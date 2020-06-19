if [[ $is_setup_set != 1 ]]
then
	export is_setup_set=1
	#kinit camendol@CERN.CH
	cd /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_20
	cmsenv
	cd -
	source /cvmfs/cms.cern.ch/cmsset_default.sh
	source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/setup.sh
	alias python='python3'
	#export PYTHONPATH=/home/ca262531/.local/lib/python3.6/site-packages:${PYTHONPATH}
fi
