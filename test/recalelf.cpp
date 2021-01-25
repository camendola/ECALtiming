// C++ recal (for large IOVs config, e.g. laser)
// compile as a usual root code:
// g++ test/recalelf.cpp -O3 -std=c++14 `root-config --libs --cflags` -lboost_filesystem -lboost_system -o bin/recalelf.exe -I /afs/cern.ch/user/c/camendol/recal/ -Wall /afs/cern.ch/user/c/camendol/recal/lib/libICManager.so /afs/cern.ch/user/c/camendol/recal/lib/ICManager.o
#include "TTree.h"
#include "TFile.h"

#include "../modules/cxxopts.hpp" // v2.2.0 from https://github.com/jarro2783/cxxopts
#include <filesystem>

#include <iostream>
#include <fstream>

#include <utility>

#include "../../recal/interface/ICManager.h"

using namespace recal;
using namespace std;


pair < string, unsigned int > get_ref_era_time(unsigned int ref_run)
{
  ifstream data; 
  string era, ref_era;
  unsigned int run, time, ref_time;
  data.open("data/ref_iovs.dat"); 
  if(!data) { 
    cerr << "Error: file could not be opened" << endl;
    exit(1);
  }
  bool found = false;
  while ( !data.eof() && !found) { 
    data >> run >> era >> time ;
    if (run == ref_run)  { 
      ref_time = time;
      ref_era = era;
    }
  }
  data.close();
  return make_pair(ref_era,ref_time);
}


int main(int argc, char* argv[])
{
        cxxopts::Options options("./bin/recalelf.exe", "rECAL timing with laser calibration");
	
        options.add_options()
	  ("d,debug", "enable debugging printouts",                        cxxopts::value<bool>()->default_value("false"))
	  ("y,year",  "year to process",                cxxopts::value<string>()->default_value("2018"))
	  ("r,ref",   "reference run",                  cxxopts::value<unsigned int>()->default_value("315252"))
	  ("e, era",  "era to process",                 cxxopts::value<string>()->default_value("B"))
	  ("i,input", "input files to process",         cxxopts::value<string >())
	  ("l,laser", "which laser? g, b or empty",     cxxopts::value<string >()->default_value(""))
	  ("o,output", "output file",                   cxxopts::value<string >())
	  ("h,help",  "print this usage and exit");
	
        auto opts = options.parse(argc, argv);
	
        if (opts.count("help")) {
	  cout << options.help() << endl;
	  exit(0);
        }
       
        bool debug            = opts["debug"].as<bool>();
        string year           = opts["year"].as<string>();
        string era            = opts["era"].as<string>();
	string laser          = opts["laser"].as<string>();
	unsigned int ref_run  = opts["ref"].as<unsigned int>();
	pair <string, unsigned int> ref_era_time = get_ref_era_time(ref_run);

	string path_calib = "/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json"; 
	string path_laser = "/afs/cern.ch/work/c/camendol/LaserIOVs/"+year+"/"+era+"/ic-config"+laser+".json"; 
	string path_laser_ref = "/afs/cern.ch/work/c/camendol/LaserIOVs/"+year+"/"+ref_era_time.first+"/ic-config"+laser+".json"; 
	if (debug) {
	  path_calib = "/afs/cern.ch/work/c/camendol/CalibIOVs/dummy.json"; 
	  path_laser = "/afs/cern.ch/work/c/camendol/LaserIOVs/"+year+"/A/dummy.json"; 
	}

	string input_file = opts["input"].as<string>();
	string output_file = opts["output"].as<string>();

	cout << "Input file "+input_file << endl; 

	string suffix = laser;
	suffix = suffix + "_ref" + to_string(ref_run);
	output_file.replace(output_file.end() - 5, output_file.end(), suffix+".root");

	cout << "Output file " + output_file << endl; 

       	cout << "@ Loading IOVs..." <<endl; 	
	cout << " - physics calibration " << path_calib << endl;
	ICManager iovcalib(path_calib);

	cout << " - laser calibration " << path_laser << endl;
	ICManager iovlaser(path_laser);

	cout << " - laser calibration (reference) " << path_laser_ref << endl;
	ICManager iovlaser_ref(path_laser_ref, ref_era_time.second);	

	cout << "~~~> Done" <<endl; 	
	
	cout << "@ Load input ntuple... " << endl; 
	TFile* main_file  = new TFile (input_file.c_str());
	TTree* main_tree = (TTree *) main_file->Get("selected");
	main_tree->BuildIndex("runNumber", "eventNumber");

	// old
	UInt_t         runNumber;
	UInt_t         eventTime;
	Short_t        xSeedSC[3];
	Short_t        ySeedSC[3];
	Float_t        timeSeedSC[3];

	main_tree->SetBranchAddress("runNumber",  &runNumber);
	main_tree->SetBranchAddress("eventTime",  &eventTime);
	main_tree->SetBranchAddress("xSeedSC",    &xSeedSC);
	main_tree->SetBranchAddress("ySeedSC",    &ySeedSC);
	main_tree->SetBranchAddress("timeSeedSC", &timeSeedSC);

	cout << "@ Clone tree to output... " << endl; 

	TFile* recal_file = TFile::Open(output_file.c_str(), "RECREATE");
	int entries = main_tree->GetEntries();
	recal_file->cd();
	TTree * recal_tree = (TTree *) main_tree->CloneTree(0) ;
	if (debug) recal_tree->Print();

	// new
	Float_t calib1 = -999.;
	Float_t calib2 = -999.;
	
	Float_t laser1_raw = -999.;
	Float_t laser2_raw = -999.;
	Float_t laser1 = -999.;
	Float_t laser2 = -999.;
      
	Float_t timeSeedSC1_recal  = -999.;
	Float_t timeSeedSC2_recal  = -999.;

	recal_tree->Branch("calib1", &calib1, "calib1/F");
	recal_tree->Branch("calib2", &calib2, "calib2/F");

	recal_tree->Branch("laser1", &laser1, "laser1/F");
	recal_tree->Branch("laser2", &laser2, "laser2/F");
	recal_tree->Branch("laser1_raw", &laser1_raw, "laser1_raw/F");
	recal_tree->Branch("laser2_raw", &laser2_raw, "laser2_raw/F");
	
	recal_tree->Branch("timeSeedSC1_recal", &timeSeedSC1_recal, "timeSeedSC1_recal/F");
	recal_tree->Branch("timeSeedSC2_recal", &timeSeedSC2_recal, "timeSeedSC2_recal/F");
	  

	for (int ev = 0 ; ev < entries; ++ev) 
	  {
	    if (ev % 10000 == 0)  cout << "- reading event " << ev << " of " << entries << endl ;
	    main_tree->GetEntry(ev);
	    float calib1_first = 0;
	    float calib2_first = 0;
	    float laser1_first = 0;
	    float laser2_first = 0;

	    //clear variables
	    calib1 = -999.;
	    calib2 = -999.;
	    
	    laser1_raw = -999.;
	    laser2_raw = -999.;
	    laser1 = -999.;
	    laser2 = -999.;
	    
	    timeSeedSC1_recal  = -999.;
	    timeSeedSC2_recal  = -999.;

	    calib1         = iovcalib.getIC(xSeedSC[0], ySeedSC[0], 0, runNumber);                         // physics calibration
	    
	    
	    calib1_first   = iovcalib.getIC(xSeedSC[0], ySeedSC[0], 0, ref_run);                           // physics calibration reference
	    laser1_first   = iovlaser_ref.getIC(xSeedSC[0], ySeedSC[0], 0, ref_era_time.second);           // laser calibration reference
	  
	    if (laser1_first == 1.0) continue;
	    laser1_raw     = iovlaser.getIC(xSeedSC[0], ySeedSC[0], 0, eventTime) - laser1_first;          // laser calibration (raw deltaT w.r.t. beginning of the year)
	    
	    // 40 mins = 2400 timestamp epochs => get back of about 39 mins to be sure to catch the previous iov 
	    int steps_back = 0;
	    unsigned int time = eventTime;
	    while (laser1_raw == 1. && time > 1524931327 && steps_back < 5){
	      time = time - 2350 ;
	      laser1_raw     = iovlaser.getIC(xSeedSC[0], ySeedSC[0], 0, time) - laser1_first;
	      steps_back += 1;
	    }  
	    laser1         = calib1_first - laser1_raw; 
	    
	    
	    calib2         = iovcalib.getIC(xSeedSC[1], ySeedSC[1], 0, runNumber);                         // physics calibration

	    calib2_first   = iovcalib.getIC(xSeedSC[1], ySeedSC[1], 0, ref_run);                           // physics calibration reference
	    laser2_first   = iovlaser_ref.getIC(xSeedSC[1], ySeedSC[1], 0, ref_era_time.second);           // laser calibration reference
	  
	    if (laser2_first == 1.0) continue;	    
	    laser2_raw     = iovlaser.getIC(xSeedSC[1], ySeedSC[1], 0, eventTime) - laser2_first;          // laser calibration (blue + green) (raw deltaT w.r.t. beginning of the year)
	    
	    // 40 mins = 2400 timestamp epochs => get back of about 39 mins to be sure to catch the previous iov 
	    steps_back = 0;
	    time = eventTime;
	    while (laser2_raw == 1. && time > 1524931327 && steps_back < 5){
	      time = time - 2350 ;
	      laser2_raw     = iovlaser.getIC(xSeedSC[1], ySeedSC[1], 0, time) - laser2_raw;
	      steps_back += 1;
	    }  
	    laser2       = calib2_first - laser2_raw; 
	    
	    timeSeedSC1_recal  = timeSeedSC[0] - calib1 + laser1;	    
	    timeSeedSC2_recal  = timeSeedSC[1] - calib2 + laser2;
	    
	    if (debug){
	      cout << "e1" << endl;
	      cout << "ieta " << xSeedSC[0] << "iphi " << ySeedSC[0] << endl;
	      cout << "runNumber = " << runNumber << " ~~~> calib1 " << calib1 << endl; 
	      cout << "eventTime = " << eventTime << " ~~~> laser1 " << laser1 << endl;
	      cout<<endl;
	      cout<< "e2" << endl;
	      cout << "ieta " << xSeedSC[1] << "iphi " << ySeedSC[1] << endl;
	      cout << "runNumber = " << runNumber << " ~~~> calib2 " << calib2 << endl; 
	      cout << "eventTime = " << eventTime << " ~~~> laser2 " << laser2 << endl;
	    }
	    recal_tree->Fill();	    
	  }
	recal_tree->Write();
	recal_file->Write();
	main_file->Close();
	recal_file->Close();
	return 0;
}

