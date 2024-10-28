// C++ recal (for large IOVs config, e.g. laser)
// compile as a usual root code:
// g++ test/recalelf_TOF.cpp -O3 -std=c++14 `root-config --libs --cflags` -lboost_filesystem -lboost_system -o bin/recalelf_TOF.exe -I /afs/cern.ch/user/c/camendol/recal/ -Wall /afs/cern.ch/user/c/camendol/recal/lib/libICManager.so /afs/cern.ch/user/c/camendol/recal/lib/ICManager.o
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
        cxxopts::Options options("./bin/recalelf_TOF.exe", "rECAL timing with TOF calibration");
	
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

	string path_calib = "/afs/cern.ch/user/c/camendol/ECALtiming/plots/staggered_2021_03_26_maps/ic-config.json";


	string input_file = opts["input"].as<string>();
	string output_file = opts["output"].as<string>();

	cout << "Input file "+input_file << endl; 

	string suffix = laser;

	cout << "Output file " + output_file << endl; 

       	cout << "@ Loading IOVs..." <<endl; 	
	cout << " - TOF calibration " << path_calib << endl;
	ICManager iovcalib(path_calib);

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
	Float_t        timeSeedSC1_corr;
	Float_t        timeSeedSC2_corr;
	Float_t        timeSecondToSeedSC1_corr;
	Float_t        timeSecondToSeedSC2_corr;

	main_tree->SetBranchAddress("runNumber",  &runNumber);
	main_tree->SetBranchAddress("eventTime",  &eventTime);
	main_tree->SetBranchAddress("xSeedSC",    &xSeedSC);
	main_tree->SetBranchAddress("ySeedSC",    &ySeedSC);
	main_tree->SetBranchAddress("timeSeedSC1_corr", &timeSeedSC1_corr);
	main_tree->SetBranchAddress("timeSeedSC2_corr", &timeSeedSC2_corr);
	main_tree->SetBranchAddress("timeSecondToSeedSC1_corr", &timeSecondToSeedSC1_corr);
	main_tree->SetBranchAddress("timeSecondToSeedSC2_corr", &timeSecondToSeedSC2_corr);

	cout << "@ Clone tree to output... " << endl; 

	TFile* recal_file = TFile::Open(output_file.c_str(), "RECREATE");
	int entries = main_tree->GetEntries();
	recal_file->cd();
	TTree * recal_tree = (TTree *) main_tree->CloneTree(0) ;
	if (debug) recal_tree->Print();

	// new
	Float_t calib1 = -999.;
	Float_t calib2 = -999.;
	
	Float_t timeSeedSC1_corr_TOF  = -999.;
	Float_t timeSeedSC2_corr_TOF  = -999.;
	Float_t timeSecondToSeedSC1_corr_TOF  = -999.;
	Float_t timeSecondToSeedSC2_corr_TOF  = -999.;

	recal_tree->Branch("calib1", &calib1, "calib1/F");
	recal_tree->Branch("calib2", &calib2, "calib2/F");
	
	recal_tree->Branch("timeSeedSC1_corr_TOF", &timeSeedSC1_corr_TOF, "timeSeedSC1_corr_TOF/F");
	recal_tree->Branch("timeSeedSC2_corr_TOF", &timeSeedSC2_corr_TOF, "timeSeedSC2_corr_TOF/F");
	recal_tree->Branch("timeSecondToSeedSC1_corr_TOF", &timeSecondToSeedSC1_corr_TOF, "timeSecondToSeedSC1_corr_TOF/F");
	recal_tree->Branch("timeSecondToSeedSC2_corr_TOF", &timeSecondToSeedSC2_corr_TOF, "timeSecondToSeedSC2_corr_TOF/F");
	
	for (int ev = 0 ; ev < entries; ++ev) 
	  {
	    if (ev % 10000 == 0)  cout << "- reading event " << ev << " of " << entries << endl ;
	    main_tree->GetEntry(ev);
	    
	    //clear variables
	    calib1 = -999.;
	    calib2 = -999.;
	   
	    
	    timeSeedSC1_corr_TOF  = -999.;
	    timeSeedSC2_corr_TOF  = -999.;

	    calib1         = iovcalib.getIC(xSeedSC[0], ySeedSC[0], 0, runNumber);          
	    calib2         = iovcalib.getIC(xSeedSC[1], ySeedSC[1], 0, runNumber);                         
	    
	    timeSeedSC1_corr_TOF  = timeSeedSC1_corr + calib1;	    
	    timeSeedSC2_corr_TOF  = timeSeedSC2_corr + calib2;
	    timeSecondToSeedSC1_corr_TOF  = timeSecondToSeedSC1_corr + calib1; // temporary
	    timeSecondToSeedSC2_corr_TOF  = timeSecondToSeedSC2_corr + calib2; // temporary
	    
	    if (debug){
	      cout << "e1" << endl;
	      cout << "ieta " << xSeedSC[0] << "iphi " << ySeedSC[0] << endl;
	      cout << "runNumber = " << runNumber << " ~~~> calib1 " << calib1 << endl; 
	      cout << "time_TOF = " <<  timeSeedSC1_corr_TOF << " time =  " <<  timeSeedSC1_corr << endl; 
	      cout<<endl;
	      cout<< "e2" << endl;
	      cout << "ieta " << xSeedSC[1] << "iphi " << ySeedSC[1] << endl;
	      cout << "runNumber = " << runNumber << " ~~~> calib2 " << calib2 << endl; 
	    }
	    recal_tree->Fill();	    
	  }
	recal_tree->Write();
	recal_file->Write();
	main_file->Close();
	recal_file->Close();
	return 0;
}

