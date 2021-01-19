// C++ recal (for large IOVs config, e.g. laser)
// compile as a usual root code:
// g++ test/recalelf.cpp -O3 -std=c++14 `root-config --libs --cflags` -lboost_filesystem -lboost_system -o bin/recalelf.exe -I /afs/cern.ch/user/c/camendol/recal/ -Wall /afs/cern.ch/user/c/camendol/recal/lib/libICManager.so /afs/cern.ch/user/c/camendol/recal/lib/ICManager.o
#include "TTree.h"
#include "TFile.h"

#include "../modules/cxxopts.hpp" // v2.2.0 from https://github.com/jarro2783/cxxopts
#include <filesystem>

#include <tuple>

#include "../../recal/interface/ICManager.h"

using namespace recal;
using namespace std;


int main(int argc, char* argv[])
{
        cxxopts::Options options("./bin/recalelf.exe", "rECAL timing with laser calibration");
	
        options.add_options()
	  ("d,debug", "enable debugging printouts",                        cxxopts::value<bool>()->default_value("false"))
	  ("y,year",  "year to process",                cxxopts::value<string>()->default_value("2018"))
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
       
        bool debug = opts["debug"].as<bool>();

        string year   = opts["year"].as<string>();
        string era    = opts["era"].as<string>();
	string laser  = opts["laser"].as<string>();

	string path_calib = "/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json"; 
	//string path_calib = "/afs/cern.ch/work/c/camendol/CalibIOVs/dummy.json"; 
	string path_laser = "/afs/cern.ch/work/c/camendol/LaserIOVs/"+year+"/"+era+"/ic-config"+laser+".json"; 
	//string path_laser = "/afs/cern.ch/work/c/camendol/LaserIOVs/"+year+"/A/dummy.json"; 
	string input_file = opts["input"].as<string>();
	string output_file = opts["output"].as<string>();
	cout << "Input file "+input_file << endl; 
	cout << "Output file " + output_file.replace(output_file.end() - 5, output_file.end(), laser+".root") << endl; 

	
	cout << "@ Loading IOVs..." <<endl; 	
	cout << " - physics calibration " << path_calib << endl;
	ICManager iovcalib(path_calib);

	cout << " - laser calibration " << path_laser << endl;
	ICManager iovlaser(path_laser);
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
	TFile* recal_file = TFile::Open(output_file.replace(output_file.end() - 5, output_file.end(), laser+".root").c_str(), "RECREATE");
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

	recal_tree->Branch("calib1", &calib1, "calib1/f");
	recal_tree->Branch("calib2", &calib2, "calib2/f");

	recal_tree->Branch("laser1", &laser1, "laser1/f");
	recal_tree->Branch("laser2", &laser2, "laser2/f");
	recal_tree->Branch("laser1_raw", &laser1_raw, "laser1_raw/f");
	recal_tree->Branch("laser2_raw", &laser2_raw, "laser2_raw/f");
	
	recal_tree->Branch("timeSeedSC1_recal", &timeSeedSC1_recal, "timeSeedSC1_recal/f");
	recal_tree->Branch("timeSeedSC2_recal", &timeSeedSC2_recal, "timeSeedSC2_recal/f");
	  

	for (int ev = 0 ; ev < entries; ++ev) 
	  {
	    if (ev % 10000 == 0)  cout << "- reading event " << ev << " of " << entries << endl ;
	    main_tree->GetEntry(ev);
	    float calib1_first = 0;
	    float calib2_first = 0;

	    //clear variables
	    calib1 = -999.;
	    calib2 = -999.;
	    
	    laser1_raw = -999.;
	    laser2_raw = -999.;
	    laser1 = -999.;
	    laser2 = -999.;
	    
	    timeSeedSC1_recal  = -999.;
	    timeSeedSC2_recal  = -999.;

	    calib1         = iovcalib.getIC(xSeedSC[0], ySeedSC[0], 0, runNumber);                     // physics calibration
	    calib1_first   = iovcalib.getIC(xSeedSC[0], ySeedSC[0], 0, 315252);                        // physics calibration first 2018A run
	    laser1_raw     = iovlaser.getIC(xSeedSC[0], ySeedSC[0], 0, eventTime);                     // laser calibration (blue + green) (raw deltaT w.r.t. beginning of the year)
	    
	    // 40 mins = 2400 timestamp epochs => get back of about 39 mins to be sure to catch the previous iov 
	    int steps_back = 0;
	    unsigned int time = eventTime;
	    while (laser1_raw == 1. && time > 1524931327 && steps_back < 5){
	      time = time - 2350 ;
	      laser1_raw     = iovlaser.getIC(xSeedSC[0], ySeedSC[0], 0, time);
	    
	      steps_back += 1;
	    }  
	    laser1         = calib1_first - laser1_raw;
	    
	    
	    calib2         = iovcalib.getIC(xSeedSC[1], ySeedSC[1], 0, runNumber);                     // physics calibration
	    calib2_first   = iovcalib.getIC(xSeedSC[1], ySeedSC[1], 0, 315252);                        // physics calibration first 2018A run
	    laser2_raw     = iovlaser.getIC(xSeedSC[1], ySeedSC[1], 0, eventTime);                     // laser calibration (blue + green) (raw deltaT w.r.t. beginning of the year)
	    
	    // 40 mins = 2400 timestamp epochs => get back of about 39 mins to be sure to catch the previous iov 
	    steps_back = 0;
	    time = eventTime;
	    while (laser2_raw == 1. && time > 1524931327 && steps_back < 5){
	      time = time - 2350 ;
	      laser2_raw     = iovlaser.getIC(xSeedSC[1], ySeedSC[1], 0, time);
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

