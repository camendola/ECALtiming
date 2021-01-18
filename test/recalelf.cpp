// C++ recal (for large IOVs config, e.g. laser)
// compile as a usual root code:
// g++ test/recalelf.cpp -O3 -std=c++14 `root-config --libs --cflags` -lboost_filesystem -lboost_system -o bin/recalelf.exe -I /afs/cern.ch/user/c/camendol/recal/ -Wall /afs/cern.ch/user/c/camendol/recal/lib/libICManager.so /afs/cern.ch/user/c/camendol/recal/lib/ICManager.o

#include "TTree.h"
#include "TFile.h"

#include "../modules/cxxopts.hpp" // v2.2.0 from https://github.com/jarro2783/cxxopts
#include <filesystem>

#include "../../recal/interface/ICManager.h"

using namespace recal;
using namespace std;

int main(int argc, char* argv[])
{
        cxxopts::Options options("./bin/recalelf.exe", "rECAL with lasers");
	
        options.add_options()
	  ("d,debug", "enable debugging printouts",                        cxxopts::value<bool>()->default_value("false"))
	  ("y,year",  "year to process",           cxxopts::value<int>())
	  ("e, era",  "era to process",            cxxopts::value<int>())
	  ("i,input", "input files to process",    cxxopts::value<string >())
	  ("o,output", "output file",              cxxopts::value<string >())
	  ("h,help",  "print this usage and exit");
	
        auto opts = options.parse(argc, argv);
	
        if (opts.count("help")) {
	  cout << options.help() << endl;
	  exit(0);
        }
       
        bool debug = opts["debug"].as<bool>();
	
	cout << "@ Loading IOVs..." <<endl; 	
	ICManager icmancalib("/afs/cern.ch/work/c/camendol/CalibIOVs/ic-config.json");
	ICManager icmanlaser("/afs/cern.ch/work/c/camendol/LaserIOVs/2018/B/ic-config.json");
	cout << "~~~> Done" <<endl; 	
	string input_file = opts["input"].as<string>();
	TFile* main_file  = new TFile (input_file, "recreate");
	
	
	return 0;
}

