#!/usr/bin/env python3

import argparse
import os

from math import sqrt
from functools import reduce
from array import array

import ROOT
import recal
import ecalic 

def getICs(icmanagers, x, y, run, time, ecal, whichlaser = ""):
    calib       = icmanagers[0].getIC(x, y, 0, run)                     # physics calibration
    calib_first = icmanagers[0].getIC(x, y, 0, 315252)                  # physics calibration first 2018A run
    laser_raw     = icmanagers[1].getIC(x, y, 0, time)                  # laser calibration (blue + green) (raw deltaT w.r.t. beginning of the year)

    # 40 mins = 2400 timestamp epochs => get back of about 39 mins to be sure to catch the previous iov 
    FED = ecal[(ecal['ix'] == x) & (ecal['iy'] == y)]["FED"].values[0]
    if not (whichlaser == "g" and FED in [612,613,616,618,619,631,636]):     #these are missing in all green iovs...
        steps_back = 0
        while laser_raw == 1 and steps_back < 5: 
            time = time - 2350  
            laser_raw     = icmanagers[1].getIC(x, y, 0, time)                 
            steps_back += 1
    laser         = calib_first - laser_raw
    
    return calib, laser_raw,  laser



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Update timing calibration in existing ECALElf ntuples.')
    parser.add_argument('-i', '--input',  dest='infile',   type=str, help='path to the ECALElf ntuple')
    parser.add_argument('-o', '--output', dest='outfile',  type=str, help='Output file name')
    parser.add_argument('-e', '--era',    dest='era',      type=str, help='era')
    parser.add_argument('-l', '--laser',  dest='laser',    type=str, help='which laser ', default = "")

    args = parser.parse_args()
    
    ecal = ecalic.icCMS().iov
    
    main_file = ROOT.TFile.Open(args.infile)
    main_tree = main_file.Get('selected')    
    main_tree.BuildIndex("runNumber", "eventNumber")
    print("opened")

    recal_file = ROOT.TFile.Open(args.outfile.replace(".root", args.laser+".root"), 'RECREATE')
    recal_tree = main_tree.CloneTree(0) #ROOT.TTree('recal_tree', 'Recalibrated')
    #main_tree.CloneTree(0)
    recal_tree.Print()
    print("cloned")


    laser1_raw = array( 'f', [ 0 ] )
    laser2_raw = array( 'f', [ 0 ] )
    laser1 = array( 'f', [ 0 ] )
    laser2 = array( 'f', [ 0 ] )

    calib1 = array( 'f', [ 0 ] )
    calib2 = array( 'f', [ 0 ] )

    timeSeedSC1_recal = array( 'f', [ 0 ] )
    timeSeedSC2_recal = array( 'f', [ 0 ] )

    recal_tree.Branch('calib1', calib1, 'calib1/f')
    recal_tree.Branch('calib2', calib2, 'calib2/f')

    recal_tree.Branch('laser1', laser1, 'laser1/f')
    recal_tree.Branch('laser2', laser2, 'laser2/f')
    recal_tree.Branch('laser1_raw', laser1_raw, 'laser1_raw/f')
    recal_tree.Branch('laser2_raw', laser2_raw, 'laser2_raw/f')

    recal_tree.Branch('timeSeedSC1_recal', timeSeedSC1_recal, 'timeSeedSC1_recal/f')
    recal_tree.Branch('timeSeedSC2_recal', timeSeedSC2_recal, 'timeSeedSC2_recal/f')


    #json_paths = ["/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json",
    #              "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/"+args.era+"/ic-config"+args.laser+".json"]

    json_paths = ["/afs/cern.ch/work/c/camendol/CalibIOVs/dummy.json",
                  "/afs/cern.ch/work/c/camendol/LaserIOVs/2018/A/dummy.json"]

    icmanagers = []
    for json_path in json_paths:
        print (json_path)
        icmanagers.append(recal.ICManager(json_path))
    
    print("got calib")

    debug = False
    i = 0
    for evt in main_tree:
        print (i)
        i += 1
        calib1[0], laser1_raw[0], laser1[0]  = getICs(icmanagers,
                                                      main_tree.xSeedSC[0], 
                                                      main_tree.ySeedSC[0],  
                                                      main_tree.runNumber, 
                                                      main_tree.eventTime, 
                                                      ecal, args.laser)

        calib2[0], laser2_raw[0], laser2[0] = getICs(icmanagers, 
                                                     main_tree.xSeedSC[1], 
                                                     main_tree.ySeedSC[1], 
                                                     main_tree.runNumber, 
                                                     main_tree.eventTime, 
                                                     ecal, args.laser)    

        timeSeedSC1_recal[0]  = main_tree.timeSeedSC[0] - calib1[0] + laser1[0]
    
        timeSeedSC2_recal[0]  = main_tree.timeSeedSC[1] - calib2[0] + laser2[0]


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
        if i ==50: break

    recal_tree.Write()
    recal_file.Close()
