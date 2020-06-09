import os, sys
import argparse
import time

parser = argparse.ArgumentParser()

parser.add_argument('-y', '--year', type=int,
                    default=2017, help="year")
parser.add_argument('-t', '--tag',
                    default = None, help="tag")

args =parser.parse_args()


year = args.year 
fileList = "filelists/ECALELF_Run2UL/Data_UL2016.log"
fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2016_extra.log"
if year ==2017: 
    fileList = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017_extra.log"
if year ==2018: 
    fileList = "filelists/ECALELF_Run2UL/Data_UL2018.log"
    fileList_extra = "filelists/ECALELF_Run2UL/Data_UL2018_extra.log"


files = [line. rstrip('\n') for line in open(fileList)]
files_extra = [line. rstrip('\n') for line in open(fileList_extra)]

if not args.tag: 
	tag = "extend_trees_"+str(args.year)
else:
	tag= args.tag

if os.path.exists (tag) : os.system ('rm -f ' + tag + '/*')
else                    : os.system ('mkdir -p ' + tag)

n = 0
submit_file = open (tag + '/submit.sh', 'w')
for file, file_extra in zip(files,files_extra):
	job_file = open (tag+ '/job_'+str(args.year)+'_'+ str(n)+'.sh', 'w')
	job_file.write ('#!/bin/bash\n')
	job_file.write ('echo ${is_setup_set}\n')
	job_file.write ('if [[ $is_setup_set != 1 ]]\n')
	job_file.write ('then\n')
	job_file.write ('	export is_setup_set=1\n')
	job_file.write ('	cd /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_20;\n')
	job_file.write ('	eval `scram r -sh`;\n')
	job_file.write ('	cd /home/ca262531/ECALtiming;\n')
	job_file.write ('	source /cvmfs/cms.cern.ch/cmsset_default.sh;\n')
	job_file.write ('	source /cvmfs/sft.cern.ch/lcg/views/LCG_96python3/x86_64-slc6-gcc8-opt/setup.sh;\n')
	job_file.write ('fi\n')
	job_file.write ('cd /home/ca262531/ECALtiming;\n')
	command = "python extend_tree.py --file " + file + " --extra " + file_extra + " --year " + str(year) 
	command += ' >& ' + tag + '/job_'+str(args.year)+'_'+ str(n)+'.log;\n'
	job_file.write(command)
	job_file.write ('touch ' + tag + '/done_'+ str(n)+';\n')
	job_file.close()
	os.system ('chmod u+rwx ' + tag+ '/job_'+str(args.year)+'_'+ str(n)+'.sh')
	submit = "clubatch "+ tag + "/job_"+str(args.year)+"_"+ str(n)+".sh"
	os.system(submit)
	time.sleep(0.1)
	submit_file.write (submit + '\n')
	n = n + 1
submit_file.close()

