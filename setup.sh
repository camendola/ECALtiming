Bif [[ $is_setup_set != 1 ]]
then
    if [[ "$HOSTNAME" == *"iclust"* ]]
    then
	export is_setup_set=1
	#kinit camendol@CERN.CH
	#cd /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_20
	#eval `scramv1 runtime -sh`
	#cd -
	#source /cvmfs/cms.cern.ch/cmsset_default.sh
	#source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-slc6-gcc8-opt/setup.sh
	#source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-centos7-gcc9-opt/setup.sh
	source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-centos7-gcc9-opt/setup.sh
	#export PATH=$PATH:/drf/projets/cms/workingcmssoft/bin 
	alias python='python3.7'
	
    elif [[ "$HOSTNAME" == *"lxplus"* ]]
    then 
	export is_setup_set=1
	source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-centos7-gcc9-opt/setup.sh
	export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/c/camendol/recal/lib
	alias python='python3.7'
    else
	export is_setup_set=1
	source /cvmfs/sft.cern.ch/lcg/views/LCG_97python3/x86_64-centos7-gcc9-opt/setup.sh
	export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/c/camendol/recal/lib
	alias python='python3.7'
    fi
fi    
    
