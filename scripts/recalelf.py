#!/usr/bin/env python3

import argparse
import os

from math import sqrt
from functools import reduce
from array import array

import ROOT
import recal

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Update timing calibration in existing ECALElf ntuples.')
    parser.add_argument('--in', dest='infile', type=str, help='path to the ECALElf ntuple')
    parser.add_argument('-o', '--output', dest='outfile', type=str, help='Output file name')
    parser.add_argument('-e', '--era', dest='era', type=str, help='era')

    args = parser.parse_args()
    

    main_file = ROOT.TFile.Open(args.infile)
    main_tree = main_file.Get('selected')    
    main_tree.BuildIndex("runNumber", "eventNumber")
    print("opened")
    recal_file = ROOT.TFile.Open(args.outfile, 'RECREATE')
    recal_tree = main_tree.CloneTree(0) #ROOT.TTree('recal_tree', 'Recalibrated')
    #main_tree.CloneTree(0)
    recal_tree.Print()
    print("cloned")

    calib1 = array( 'f', [ 0 ] )
    calib2 = array( 'f', [ 0 ] )
    laser1 = array( 'f', [ 0 ] )
    laser2 = array( 'f', [ 0 ] )
    timeSeedSC1_recal = array( 'f', [ 0 ] )
    timeSeedSC2_recal = array( 'f', [ 0 ] )

    recal_tree.Branch('calib1', calib1, 'calib1/f')
    recal_tree.Branch('calib2', calib2, 'calib2/f')
    recal_tree.Branch('laser1', laser1, 'laser1/f')
    recal_tree.Branch('laser2', laser2, 'laser2/f')
    recal_tree.Branch('timeSeedSC1_recal', timeSeedSC1_recal, 'timeSeedSC1_recal/f')
    recal_tree.Branch('timeSeedSC2_recal', timeSeedSC2_recal, 'timeSeedSC2_recal/f')



    path_calib = "/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json"
    path_laser = "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/"+args.era+"/ic-config.json"
    icman_calib = recal.ICManager(path_calib)    
    icman_laser = recal.ICManager(path_laser)    
    
    print("got calib")
    i = 0
    
    for evt in main_tree:
        
        calib1[0] = icman_calib.getIC(main_tree.xSeedSC[0],
                                   main_tree.ySeedSC[0],
                                   0,
                                   main_tree.runNumber)

        calib1_first = icman_calib.getIC(main_tree.xSeedSC[0],
                                         main_tree.ySeedSC[0],
                                         0,
                                         315252)

        laser1[0] = calib1_first - icman_laser.getIC(main_tree.xSeedSC[0],
                                                  main_tree.ySeedSC[0],
                                                  0,
                                                  main_tree.eventTime)

        timeSeedSC1_recal[0] = main_tree.timeSeedSC[0] - calib1[0] + laser1[0]

        calib2[0] = icman_calib.getIC(main_tree.xSeedSC[1],
                                   main_tree.ySeedSC[1],
                                   0,
                                   main_tree.runNumber)
        calib2_first = icman_calib.getIC(main_tree.xSeedSC[1],
                                         main_tree.ySeedSC[1],
                                         0,
                                         315252)
        laser2[0] = calib2_first - icman_laser.getIC(main_tree.xSeedSC[1],
                                                  main_tree.ySeedSC[1],
                                                  0,
                                                  main_tree.eventTime)

        timeSeedSC2_recal[0] = main_tree.timeSeedSC[1] - calib2[0] + laser2[0]

        #if (calib1_first > 10 or  calib2_first > 10 or calib1[0]  > 10 or calib2[0]  > 10 or laser1[0]  > 10 or  laser2[0]  > 10 or timeSeedSC1_recal[0]  > 10 or timeSeedSC2_recal[0] > 10 ):
        #    print ("===> ", calib1_first, calib2_first, calib1[0], calib2[0], laser1[0], laser2[0],timeSeedSC1_recal[0], timeSeedSC2_recal[0])

        recal_tree.Fill()
    
    recal_tree.Write()
    recal_file.Close()
