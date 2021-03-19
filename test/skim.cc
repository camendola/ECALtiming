// C++ version of the python analysis
// - hopefully to fix memory issues
// compile as a usual root code, e.g.
// g++ test/skim.cc -O3 -std=c++14 `root-config --libs --cflags` -lboost_filesystem -lboost_system -o bin/skim.exe

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RResultPtr.hxx"
#include "ROOT/RVec.hxx"

#include "../modules/functions.cc"

#include "../modules/cxxopts.hpp" // v2.2.0 from https://github.com/jarro2783/cxxopts
#include <boost/filesystem.hpp>

#define eb_threshold "1.479"

using namespace std;

using RVec_f = const ROOT::RVec<float> &;


ROOT::RVec<float> time_correction_vtx(float z, RVec_f eta, RVec_f t)
{
        ROOT::RVec<float> t_corr(2);
        auto l = 130. * cosh(eta[0]);
        t_corr = t - (sqrt(l * l + z * z - 2 * z * l * tanh(eta)) - l) * 0.0299792458;
        return t_corr;
}





vector<string> retrieve_files(string filelist)
{
        vector<string> f;
	ifstream file(filelist);
	string str; 
	while (getline(file, str)) f.emplace_back(str);

        return f;
}

int main (int argc, char ** argv)
{
        cxxopts::Options options("bin/skim.exe", "ECAL timing analysis");

        options.add_options()
                ("d,debug", "enable debugging printouts",                        cxxopts::value<bool>()->default_value("false"))
                ("y,year",  "years to process (comma separated list)",           cxxopts::value<int>())
                ("i,input", "input files to process",                            cxxopts::value<vector<string> >())
                ("o,output", "output snapshot",                                  cxxopts::value<vector<string> >())
                ("r,runlist", "runs to process (comma separated list)",          cxxopts::value<vector<unsigned int> >())
                ("s,snapshot", "save a snapshot tree",                           cxxopts::value<bool>()->default_value("true"))
                ("m,multithread", "parallel threads",                            cxxopts::value<bool>()->default_value("false"))
                ("h,help",  "print this usage and exit")
                ;

        auto opts = options.parse(argc, argv);

        if (opts.count("help")) {
                cout << options.help() << endl;
                exit(0);
        }

        // debug might also be declared global if needed in some external functions
        // and initialized here
        bool debug = opts["debug"].as<bool>();
        bool snapshot = opts["snapshot"].as<bool>();

        // retrieving input files either from the specified year(s) or
        // from a provided comma-separated list of input file names
        vector<int> year;
        vector<string> input_files;
        vector<string> output_files;
	string filelist = "";
	if (opts.count("year")) {
                int y = opts["year"].as<int>();
		if (y == 2016) {
		  filelist = "filelists/ECALELF_Run2UL/Data_UL2016.log";
		} else if (y == 2017) {
		  filelist = "filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log";
		} else if (y == 2018) {
		  filelist = "filelists/ECALELF_Run2UL/Data_UL2018_106X_dataRun2_UL18.log";
		}
		auto v = retrieve_files(filelist);
		input_files.insert(input_files.end(), v.begin(), v.end());
		
        } else if (opts.count("input") && opts.count("output")) {
                input_files  = opts["input"].as<vector<string>>();
		output_files = opts["output"].as<vector<string>>();
		
        } else {
                cerr << "error: please specify one option between `year' and `input'/`output' \n";
                cout << options.help() << endl;
                exit(1); 
        }

        cout << "Going to skim the following files:\n";
	for (auto & s : input_files)  cout << s << "\n";
	
        for (auto & s : input_files) 
	  {
	    cout << "@@@ Skimming:\n";
	    cout << s << "\n";

	    if (opts["multithread"].as<bool>()) ROOT::EnableImplicitMT();
	    ROOT::RDataFrame df("selected", s);

	    // selections

	    // geometry
	    auto clean_ee      = "abs(deltaT_ee) < 5";
	    auto clean_e_0     = "abs(deltaT_e) < 5";
   
	    // detector
	    auto no_saturation = "gainSeedSC[0] == 0 && gainSeedSC[1] == 0";
	    
	    // physics
	    auto z_mass        = "invMass > 60 && invMass < 150";
	    auto high_r9       = "R9Ele[0] > 0.94 && R9Ele[1] > 0.94";
	    
	    // to debug columns
	    if(debug) for (auto & el : df.GetColumnNames()) cout << el << "\n";
	    
	    // new quantities
	    //ROOT::RDF::RNode fn = df, comm = df;
	    ROOT::RDF::RNode fn = df;
	    
	    fn = df.Define("deltaT_ee", "timeSeedSC[0] - timeSeedSC[1]")
	      .Define("deltaT_e", "(timeSeedSC - timeSecondToSeedSC)")
	      .Define("deltaT_e1", "deltaT_e[0]")
	      .Define("deltaT_e2", "deltaT_e[1]")
	      .Define("A_e1", "amplitudeSeedSC[0] / noiseSeedSC[0]")
	      .Define("A_e2", "amplitudeSeedSC[1] / noiseSeedSC[1]")
	      .Define("effA_ee", "A_e1 * A_e2 / sqrt(A_e1 * A_e1 + A_e2 * A_e2)")
	      .Define("timeSeedSC_corr", time_correction_vtx, {"vtxZ", "etaSCEle", "timeSeedSC"})
	      .Define("timeSeedSC1_corr", "timeSeedSC_corr[0]")
	      .Define("timeSeedSC2_corr", "timeSeedSC_corr[1]")
	      .Define("deltaT_ee_corr", "timeSeedSC_corr[0] - timeSeedSC_corr[1]")
	      .Define("timeSecondToSeedSC_corr", time_correction_vtx, {"vtxZ", "etaSCEle", "timeSecondToSeedSC"})
	      .Define("timeSecondToSeedSC1_corr", "timeSecondToSeedSC_corr[0]")
	      .Define("timeSecondToSeedSC2_corr", "timeSecondToSeedSC_corr[1]")
	      .Define("deltaT_e_corr", "(timeSeedSC_corr - timeSecondToSeedSC_corr)")
	      .Define("deltaT_e1_corr", "(timeSeedSC_corr - timeSecondToSeedSC_corr)[0]")
	      .Define("deltaT_e2_corr", "(timeSeedSC_corr - timeSecondToSeedSC_corr)[1]")
	      .Define("year", "runNumber >= 273158 && runNumber <= 284044 ? 2016 :"
		      "runNumber >= 297050 && runNumber <= 306460 ? 2017 :"
		      "runNumber >= 315257 && runNumber <= 325172 ? 2018 : 0");
	      
	    // reasonable quality selections and no gain switch
	    fn = fn.Filter(z_mass, "Z mass").Filter(high_r9, "high R9").Filter(no_saturation, "no sat.");
	    
	    
	    // save a snapshot of the variables used in the analysis
	    // for faster reload
	    if (snapshot) {
	      cout << "~~~> Going to snapshot...\n";
	      string output = "";
	      string path = ""; 
	      if (opts.count("year")){
		string dest = "/afs/cern.ch/work/c/camendol/ECALtimingData/";
		string dest_dir = "";
		string file_out = "";
		size_t pos = filelist.find_last_of("/");
		if (pos != string::npos)	dest_dir = filelist.substr(pos+1);
		size_t pos_ext = dest_dir.find_last_of(".");
		if (pos_ext != string::npos)   dest_dir = dest_dir.substr(0, pos_ext);
		size_t pos_file = s.find_last_of("/");
		if (pos_file != string::npos)  file_out = s.substr(pos_file+1);
	    
		path = dest+dest_dir+"_skimmed";
		cout << dest+dest_dir+"_skimmed/snapshot_"+file_out<< endl;
		output = path+"/snapshot_"+file_out;
	    
	      } else {
		output = output_files[(&s - &input_files[0])];
		cout << output << endl;
		size_t pos = output.find_last_of("/");
		if (pos != string::npos)        path = output.substr(0,pos+1);	
	      }
	      
	      boost::filesystem::create_directory(path);

	      auto sn = fn.Snapshot("selected",output, 
				      {
					//event
					"runNumber", "eventNumber", "eventTime", "year",
					  //SC
					  "etaSCEle", "phiSCEle", "fbremEle","chargeEle", 
					  //seed 
					  "amplitudeSeedSC", "timeSeedSC", "timeSeedSC1_corr", "timeSeedSC2_corr", "deltaT_ee", "deltaT_ee_corr", "effA_ee", "noiseSeedSC",
					  "ySeedSC", "xSeedSC", 
					  //second to seed
					  "amplitudeSecondToSeedSC", "timeSecondToSeedSC", "timeSecondToSeedSC1_corr","timeSecondToSeedSC2_corr", 
					  "deltaT_e1", "deltaT_e2", "deltaT_e1_corr", "deltaT_e2_corr"
					  }
				      );
	      cout << "...done\n";
	      
	    }
	  }
        return 0;
}
