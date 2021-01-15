#!/usr/bin/env python3

import argparse
import os

from math import sqrt
from functools import reduce
from array import array

import ROOT
import recal
import ecalic 


def getICs(icmanagers, x, y, run, time, FED):
    calib       = calib_file[0].getIC(x, y, 0, run)                     # physics calibration
    calib_first = calib_file[0].getIC(x, y, 0, 315252)                      # physics calibration first 2018A run

    laserb_raw  = calib_file[1].getIC(x, y, 0, time)                    # blue laser calibration (raw deltaT w.r.t. beginning of the year)

    laserg_raw  = calib_file[2].getIC(x, y, 0, time)                    # green laser calibration (raw deltaT w.r.t. beginning of the year)
    if FED in [612,613,616,618,619,631,636]: laserg_raw = laserb_raw        # use blue laser for missing feds in green ntuples (raw deltaT w.r.t. beginning of the year) 

    laser_raw     = calib_file[3].getIC(x, y, 0, time)                  # laser calibration (blue + green) (raw deltaT w.r.t. beginning of the year)

    while laser_raw == 1: 
        time = time - 2350  # 40 mins = 2400 epochs => get back of about 39 mins to be sure to catch the previous iov 
        laser_raw     = calib_file[3].getIC(x, y, 0, time)                 

    laserb        = calib_first - laserb_raw
    laserg        = calib_first - laserg_raw
    laser         = calib_first - laser_raw
    
    return calib, laserb_raw, laserg_raw, laser_raw, laserb, laserg, laser



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Update timing calibration in existing ECALElf ntuples.')
    parser.add_argument('--input', dest='input', type=str, help='path to the ECALElf ntuple')
    parser.add_argument('-o', '--output', dest='outfile', type=str, help='Output file name')
    parser.add_argument('-e', '--era', dest='era', type=str, help='era')

    args = parser.parse_args()
    
    ecal = ecalic.icCMS().iov
    
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
    laser1b_raw = array( 'f', [ 0 ] )
    laser2b_raw = array( 'f', [ 0 ] )
    laser1b = array( 'f', [ 0 ] )
    laser2b = array( 'f', [ 0 ] )
    laser1g_raw = array( 'f', [ 0 ] )
    laser2g_raw = array( 'f', [ 0 ] )
    laser1g = array( 'f', [ 0 ] )
    laser2g = array( 'f', [ 0 ] )
    laser1_raw = array( 'f', [ 0 ] )
    laser2_raw = array( 'f', [ 0 ] )
    laser1 = array( 'f', [ 0 ] )
    laser2 = array( 'f', [ 0 ] )

    timeSeedSC1b_recal = array( 'f', [ 0 ] )
    timeSeedSC2b_recal = array( 'f', [ 0 ] )

    timeSeedSC1g_recal = array( 'f', [ 0 ] )
    timeSeedSC2g_recal = array( 'f', [ 0 ] )

    timeSeedSC1_recal = array( 'f', [ 0 ] )
    timeSeedSC2_recal = array( 'f', [ 0 ] )

    recal_tree.Branch('calib1', calib1, 'calib1/f')
    recal_tree.Branch('calib2', calib2, 'calib2/f')
    recal_tree.Branch('laser1b', laser1b, 'laser1b/f')
    recal_tree.Branch('laser2b', laser2b, 'laser2b/f')
    recal_tree.Branch('laser1b_raw', laser1b_raw, 'laser1b_raw/f')
    recal_tree.Branch('laser2b_raw', laser2b_raw, 'laser2b_raw/f')

    recal_tree.Branch('laser1g', laser1g, 'laser1g/f')
    recal_tree.Branch('laser2g', laser2g, 'laser2g/f')
    recal_tree.Branch('laser1g_raw', laser1g_raw, 'laser1g_raw/f')
    recal_tree.Branch('laser2g_raw', laser2g_raw, 'laser2g_raw/f')

    recal_tree.Branch('laser1', laser1, 'laser1/f')
    recal_tree.Branch('laser2', laser2, 'laser2/f')
    recal_tree.Branch('laser1_raw', laser1_raw, 'laser1_raw/f')
    recal_tree.Branch('laser2_raw', laser2_raw, 'laser2_raw/f')

    recal_tree.Branch('timeSeedSC1b_recal', timeSeedSC1b_recal, 'timeSeedSC1b_recal/f')
    recal_tree.Branch('timeSeedSC2b_recal', timeSeedSC2b_recal, 'timeSeedSC2b_recal/f')
    recal_tree.Branch('timeSeedSC1g_recal', timeSeedSC1g_recal, 'timeSeedSC1g_recal/f')
    recal_tree.Branch('timeSeedSC2g_recal', timeSeedSC2g_recal, 'timeSeedSC2g_recal/f')
    recal_tree.Branch('timeSeedSC1_recal', timeSeedSC1_recal, 'timeSeedSC1_recal/f')
    recal_tree.Branch('timeSeedSC2_recal', timeSeedSC2_recal, 'timeSeedSC2_recal/f')


    json_paths = ["/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json",
                  "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/"+args.era+"/ic-config_b.json",
                  "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/"+args.era+"/ic-config_g.json",
                  "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/"+args.era+"/ic-config.json"]

    icmanagers = [recal.ICManager(json_path) for json_path in json_paths]

    
    print("got calib")

    debug = False
    for evt in main_tree:
        FED = ecal[(ecal['ix'] == x & ecal['iy'] == y)].values[0]
        calib1[0], laser1b_raw[0], laser1g_raw[0], laser1_raw[0], laser1b[0], laser1g[0], laser1[0] = getICs(icmanagers,
                                                                                                             main_tree.xSeedSC[0], 
                                                                                                             main_tree.ySeedSC[0],  
                                                                                                             main_tree.runNumber, 
                                                                                                             main_tree.eventTime, 
                                                                                                             FED)

        calib2[0], laser2b_raw[0], laser2g_raw[0], laser2_raw[0], laser2b[0], laser2g[0], laser2[0] = getICs(icmanagers, 
                                                                                                             main_tree.xSeedSC[1], 
                                                                                                             main_tree.ySeedSC[1], 
                                                                                                             main_tree.runNumber, 
                                                                                                             main_tree.eventTime, 
                                                                                                             FED)    

        timeSeedSC1b_recal[0] = main_tree.timeSeedSC[0] - calib1[0] + laser1b[0]
        timeSeedSC1g_recal[0] = main_tree.timeSeedSC[0] - calib1[0] + laser1g[0]
        timeSeedSC1_recal[0] = main_tree.timeSeedSC[0] - calib1[0] + laser1[0]
    
        timeSeedSC2b_recal[0] = main_tree.timeSeedSC[1] - calib2[0] + laser2b[0]
        timeSeedSC2g_recal[0] = main_tree.timeSeedSC[1] - calib2[0] + laser2g[0]
        timeSeedSC2_recal[0] = main_tree.timeSeedSC[1] - calib2[0] + laser2[0]


        if debug:
            print ("e1")
            print ("ieta ",  str(main_tree.xSeedSC[0]), "iphi ", str(main_tree.ySeedSC[0]))
            print ("t = 0 -> runNumber = ", str(315252), "~~~> calib1 ", str(calib1_first))
            print ("runNumber = ", str(main_tree.runNumber), "~~~> calib1 ", str(calib1[0]))
            print ("eventTime = ", str(main_tree.eventTime), "~~~> laser1 ", str(laser1[0]))
            print ("")
            print ("e2")
            print ("ieta ",  str(main_tree.xSeedSC[1]), "iphi ", str(main_tree.ySeedSC[1]))
            print ("t = 0 -> runNumber = ", str(315252), "~~~> calib2 ", str(calib2_first))
            print ("runNumber = ", str(main_tree.runNumber), "~~~> calib2 ", str(calib2[0]))
            print ("eventTime = ", str(main_tree.eventTime), "~~~> laser2 ", str(laser2[0]))

            input()

        recal_tree.Fill()
    
    recal_tree.Write()
    recal_file.Close()
