#!/usr/bin/env python
import subprocess
import glob
import os
import sys
import time
from optparse import OptionParser, make_option

parser = OptionParser(option_list=[
    make_option("-M", "--maxjobs", dest="max_jobs", type=int, default=5000,
                help="maximum number of jobs to have running (default: %defaul)"),
    make_option("-c", "--maxcpus", dest="max_cpus", type=int, default=456,
                help="maximum number of jobs to have running"),
    make_option("-d", "--dir", dest="dir", type=str, default="./",
                help="comma separated list of directory with jobs to be submitted"),
    make_option("-p", "--pattern", dest="pattern", type=str, default="job*sh",
                help="pattern of jobs to look/watch for"),
    make_option("-l", "--log", dest="logfilename", type=str, default="log_submission.log",
                help="logfile to save log data"),
    make_option("-s", "--sub", dest="subfilename", type=str, default="log_submitted.log",
                help="list of already submitted jobs"),
    make_option("-S", "--sort", dest="sort", action='store_true', default=False,
                help="sort jobs alphabetically"),
    make_option("-q", "--queue", dest="queues", action='store_true', default=False,
                help="show the queue status"),
])

(options, args) = parser.parse_args()

dir = options.dir.split(",")
pattern = options.pattern
max_cpus = options.max_cpus
max_jobs = options.max_jobs
logfilename = options.logfilename
subfilename = options.subfilename
sort = options.sort
queues = options.queues

def flog(msg):
    logfile.write("%f %s\n" % (time.time(), msg))
    logfile.flush()


def jobs():
    res = subprocess.getstatusoutput("qstat -u '*'")
    return res[0], res[1].split('\n')[2:]


def job_users(joblist):
    users = {}
    tot = 0
    for l in joblist:
        v = l.split()
        u = v[3]
        if u not in users.keys():
            users[u] = 0
        users[u] += 1
        tot += 1

    for k, n in users.items():
        print("%15s  %d" % (k, n))
    print("total running jobs:", tot)


def job_list(path):
    l = set()
    for f in glob.glob(path):
        if "job" not in f:
            print("Warning: file `" + f + "' does not look like a script, skipping.")
        l.add(f)
    return l


def job_submit(nsub, joblist, sort=False):
    print ("Going to submit", min(nsub, len(joblist)), "job(s) from a list of %d." % len(joblist))
    n = 0
    jobsortedlist = []
    if sort:
        jobsortedlist = list(joblist)
        jobsortedlist.sort(key = lambda s: int(s.split('jobs_')[1].split('.')[0])) # FIXME, hadhoc solution for "runJobsXXX.sh"
        print(jobsortedlist)
    for i in range(min(nsub, len(joblist))):
        if sort:
            job = jobsortedlist[i]
            joblist.remove(job)
        else:
            job = joblist.pop()
        res = subprocess.getstatusoutput("clubatch " + job)
        if res[0] != 0:
            print ("Error submitting job `" + job + "':", res[1])
            print ("  --> job queued again to the job list")
            joblist.add(job)
        else:
            flog(job)
            subfile.write("%s\n" % job)
            subfile.flush()
        n += 1
    return n


def job_submitted(filename):
    s = set()
    if os.path.isfile(filename):
        for l in open(filename):
            s.add(l.rstrip('\n'))
    return s


if queues:
    job_users(jobs()[1])
    sys.exit(0)

logfile = open(logfilename, "a")
submitted = job_submitted(subfilename)
subfile = open(subfilename, "a")

jlist = set()
for d in dir:
    jlist.update(job_list(d + "/" + pattern))

jlist = jlist - submitted

if not len(jlist):
    print ("No jobs found to be submitted.")
    job_users(jobs()[1])
    sys.exit(0)


while(1):
    j = jobs()
    njobs = len(j[1])
    job_users(j[1])
    nsub = min(max_jobs, max(max_cpus - 20 - njobs, 0))
    job_submit(nsub, jlist, sort)
    if len(jlist) == 0:
        sys.exit(0)
    print ("going to sleep for 5 seconds.")
    time.sleep(5)
