// C++ version of the python analysis
// - hopefully to fix memory issues
// compile as a usual root code, e.g.
//   g++ main.cc -O3 -std=c++14 `root-config --libs --cflags`

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RResultPtr.hxx"
#include "ROOT/RVec.hxx"

#include "modules/functions.cc"

#include "modules/cxxopts.hpp" // v2.2.0 from https://github.com/jarro2783/cxxopts

#define eb_threshold "1.479"

using RVec_f = const ROOT::RVec<float> &;


ROOT::RVec<float> time_correction_vtx(float z, RVec_f eta, RVec_f t)
{
        ROOT::RVec<float> t_corr(2);
        auto l = 130. * cosh(eta[0]);
        t_corr = t - (sqrt(l * l + z * z - 2 * z * l * tanh(eta)) - l) * 0.0299792458;
        return t_corr;
}


std::vector<unsigned int> retrieve_run_list(ROOT::RDF::RNode df, int year)
{
        std::string fname = "runs_" + std::to_string(year) + ".list";
        FILE * fd = fopen(fname.c_str(), "r");
        std::vector<unsigned int> run_list;
        if (!fd || year == -1) {
                ROOT::RDF::RResultPtr<std::vector<unsigned int> > runs = df.Take<unsigned int>("runNumber");
                auto tmp = runs.GetValue();
                std::sort(tmp.begin(), tmp.end());
                auto last = std::unique(tmp.begin(), tmp.end());
                tmp.erase(last, tmp.end());
                run_list = std::move(tmp);
                FILE * fd = fopen(fname.c_str(), "w");
                for (auto & r : run_list) fprintf(fd, "%d\n", r);
                fclose(fd);
        } else {
                int r;
                while (fscanf(fd, "%d", &r) != EOF) run_list.emplace_back(r);
        }
        return run_list;
}


std::vector<std::string> retrieve_files(int year)
{
        std::vector<std::string> f;
        if (year == 2016) {
                std::ifstream file("filelists/ECALELF_Run2UL/Data_UL2016.log");
                std::string str; 
                while (std::getline(file, str)) f.emplace_back(str);
        } else if (year == 2017) {
                //std::ifstream file("filelists/ECALELF_Run2UL/Data_UL2017.log");
                std::ifstream file("filelists/ECALELF_Run2UL/Data_ALCARECO_UL2017.log");
                std::string str; 
                while (std::getline(file, str)) f.emplace_back(str);
        } else if (year == 2018) {
                std::ifstream file("filelists/ECALELF_Run2UL/Data_UL2018.log");
                std::string str; 
                while (std::getline(file, str)) f.emplace_back(str);
        }
        return f;
}



int main (int argc, char ** argv)
{
        cxxopts::Options options("a.out", "ECAL timing analysis");

        options.add_options()
                ("d,debug", "enable debugging printouts", cxxopts::value<bool>()->default_value("false"))
                ("y,year",  "years to process (comma separated list)",           cxxopts::value<std::vector<int> >())
                ("i,input", "input files to process",     cxxopts::value<std::vector<std::string> >())
                ("m,minimal", "the input tree contains only the minimal variables for the analysis", cxxopts::value<bool>()->default_value("false"))
                ("r,runlist", "runs to process (comma separated list)", cxxopts::value<std::vector<unsigned int> >())
                ("s,snapshot", "save a snapshot tree after common selections, containing the minimal variables needed in the analysis, and exit", cxxopts::value<bool>()->default_value("false"))
                ("h,help",  "print this usage and exit")
                ;

        auto opts = options.parse(argc, argv);

        if (opts.count("help")) {
                std::cout << options.help() << std::endl;
                exit(0);
        }

        // debug might also be declared global if needed in some external functions
        // and initialized here
        bool debug = opts["debug"].as<bool>();

        bool minimal = opts["minimal"].as<bool>();
        bool snapshot = opts["snapshot"].as<bool>();

        // retrieving input files either from the specified year(s) or
        // from a provided comma-separated list of input file names
        std::vector<int> year;
        std::vector<std::string> input_files;
        if (opts.count("year")) {
                year = opts["year"].as<std::vector<int>>();
                for (auto y : year) {
                        auto v = retrieve_files(y);
                        input_files.insert(input_files.end(), v.begin(), v.end());
                }
        } else if (opts.count("input")) {
                input_files = opts["input"].as<std::vector<std::string>>();
        } else {
                std::cerr << "error: please specify one option between `year' and `input'\n";
                std::cout << options.help() << std::endl;
                exit(1); 
        }

        std::cout << "Going to analyze the following files:\n";
        for (auto & s : input_files) std::cout << s << "\n";

        ROOT::EnableImplicitMT();
        ROOT::RDataFrame df("selected", input_files);

        // selections

        // geometry
        auto ee            = "abs(etaSCEle[0]) > " eb_threshold " && abs(etaSCEle[1]) > " eb_threshold;
        auto ee_plus       = "etaSCEle[0] > " eb_threshold " && etaSCEle[1] > " eb_threshold;
        auto ee_minus      = "etaSCEle[0] < -" eb_threshold " && etaSCEle[1] < -" eb_threshold;
        auto be            = "(abs(etaSCEle[0]) > " eb_threshold " && abs(etaSCEle[1]) < " eb_threshold ") || "
                             "(abs(etaSCEle[0]) < " eb_threshold " && abs(etaSCEle[1]) > " eb_threshold ")";
        auto bb            = "abs(etaSCEle[0]) < " eb_threshold " && abs(etaSCEle[1]) < " eb_threshold;

        auto no_borders_0  = "((ySeedSC[0] % 20 + 1) > 2) && ((ySeedSC[0] % 20 + 1) < 18) && (abs(xSeedSC[0]) > 2) && (abs(ySeedSC[0]) < 24)";
        auto no_borders_1  = "((ySeedSC[1] % 20 + 1) > 2) && ((ySeedSC[1] % 20 + 1) < 18) && (abs(xSeedSC[1]) > 2) && (abs(ySeedSC[1]) < 24)";

        // objects
        auto clean_ee      = "abs(delta_t_ee) < 5";

        auto clean_e_0     = "abs(deltaT_e0_seeds) < 5";
        auto rel_ampl_0    = "abs(amplitudeSeedSC[0] - amplitudeSecondToSeedSC[0]) / (amplitudeSeedSC[0] + amplitudeSecondToSeedSC[0]) < 0.1)";

        auto clean_e_1     = "abs(deltaT_e1_seeds) < 5";
        auto rel_ampl_1    = "abs(amplitudeSeedSC[1] - amplitudeSecondToSeedSC[1]) / (amplitudeSeedSC[1] + amplitudeSecondToSeedSC[1]) < 0.1)";

        auto no_saturation = "gainSeedSC[0] == 0 && gainSeedSC[1] == 0";

        // physics
        auto z_mass        = "invMass > 60 && invMass < 150";
        auto high_r9       = "R9Ele[0] > 0.94 && R9Ele[1] > 0.94";

        // to debug columns
        //for (auto & el : df.GetColumnNames()) std::cout << el << "\n";

        // new quantities
        ROOT::RDF::RNode fn = df, comm = df;
        if (!minimal) {
                fn = df.Define("delta_t_ee", "timeSeedSC[0] - timeSeedSC[1]")
                        .Define("delta_eta_ee", "etaSCEle[0] - etaSCEle[1]")
                        .Define("delta_phi_ee", "ROOT::VecOps::DeltaPhi(phiSCEle[0], phiSCEle[1])")
                        .Define("t_e0", "timeSeedSC[0]")
                        .Define("t_e1", "timeSeedSC[0]")
                        .Define("delta_t_e0", "timeSeedSC[0] - timeSecondToSeedSC[0]")
                        .Define("delta_t_e1", "timeSeedSC[1] - timeSecondToSeedSC[1]")
                        .Define("delta_a_e0", "amplitudeSeedSC[0] - amplitudeSecondToSeedSC[0]")
                        .Define("delta_a_e1", "amplitudeSeedSC[1] - amplitudeSecondToSeedSC[1]")
                        .Define("aeff_e0", "amplitudeSeedSC[0] / noiseSeedSC[0]")
                        .Define("aeff_e1", "amplitudeSeedSC[1] / noiseSeedSC[1]")
                        .Define("aeff_ee", "aeff_e0 * aeff_e1 / sqrt(aeff_e0 * aeff_e0 + aeff_e1 * aeff_e1)")
                        .Define("t_seed_corr", time_correction_vtx, {"vtxZ", "etaSCEle", "timeSeedSC"})
                        .Define("t_seed_corr_e0", "t_seed_corr[0]")
                        .Define("t_second_to_seed_corr", time_correction_vtx, {"vtxZ", "etaSCEle", "timeSecondToSeedSC"})
                        .Define("delta_t_e_corr", "t_seed_corr - t_second_to_seed_corr")
                        .Define("delta_t_ee_corr", "t_seed_corr[0] - t_seed_corr[1]")
                        .Define("year", "runNumber >= 273158 && runNumber <= 284044 ? 2016 :"
                                "runNumber >= 297050 && runNumber <= 306460 ? 2017 :"
                                "runNumber >= 315257 && runNumber <= 325172 ? 2018 : 0");

                // reasonable quality selections and no gain switch
                comm = fn.Filter(z_mass, "Z mass").Filter(high_r9, "high R9").Filter(clean_ee, "delta_t_ee").Filter(no_saturation, "no sat.");
        }

        // save a snapshot of the variables used in the analysis
        // for faster reload
        if (snapshot) {
                if (debug) std::cout << "Going to snapshot...\n";
                auto sn = comm.Snapshot("selected", "snapshot.root", {"runNumber", "eventNumber", "eventTime", "year",
                              "etaSCEle", "phiSCEle", "vtxZ",
                              "t_seed_corr_e0",
                              "aeff_ee", "t_e0", "t_e1", "delta_t_e_corr", "delta_t_ee_corr"});
                if (debug) std::cout << "...done\n";
                return 0;
        }
        /*
         * below this point, all the used variables need to be also in the snapshot list
         * to make the `minimal' option works
         */

        // histogram and graph collectors
        std::vector<ROOT::RDF::RResultPtr<TH1D> > hc_h1d;
        std::vector<ROOT::RDF::RResultPtr<TH2D> > hc_h2d;
        std::vector<ROOT::RDF::RResultPtr<TProfile> > hc_p;
        std::vector<const TGraph *> hc_g;

        // common selections
        auto eb_eb = comm.Filter(bb, "EB-EB");
        auto eb_ee = comm.Filter(be, "EB-EE");
        auto ee_ee = comm.Filter(ee, "EE-EE");

        // delta t per year
        hc_h1d.emplace_back(eb_eb.Histo1D({"delta_t_ee_corr_eb_eb", "", 200, -5, 5.}, "delta_t_ee_corr"));
        hc_h1d.emplace_back(eb_ee.Histo1D({"delta_t_ee_corr_eb_ee", "", 200, -5, 5.}, "delta_t_ee_corr"));
        hc_h1d.emplace_back(ee_ee.Histo1D({"delta_t_ee_corr_ee_ee", "", 200, -5, 5.}, "delta_t_ee_corr"));
        hc_h1d.emplace_back(eb_eb.Histo1D({"delta_t_e_corr_eb_eb",  "", 200, -5, 5.}, "delta_t_e_corr"));
        hc_h1d.emplace_back(eb_ee.Histo1D({"delta_t_e_corr_eb_ee",  "", 200, -5, 5.}, "delta_t_e_corr"));
        hc_h1d.emplace_back(ee_ee.Histo1D({"delta_t_e_corr_ee_ee",  "", 200, -5, 5.}, "delta_t_e_corr"));

        // time bias vs. vertex
        hc_h2d.emplace_back(eb_eb.Filter("etaSCEle[0] > 1.3").Histo2D(  {"ele0_t_vs_vtx",          "", 50, -15, 15, 50, -1, 1}, "vtxZ", "t_e0"));
        hc_p  .emplace_back(eb_eb.Filter("etaSCEle[0] > 1.3").Profile1D({"ele0_t_vs_vtx_pfx",      "", 50, -15, 15}, "vtxZ", "t_e0"));
        hc_h2d.emplace_back(eb_eb.Filter("etaSCEle[0] > 1.3").Histo2D(  {"ele0_t_corr_vs_vtx",     "", 50, -15, 15, 50, -1, 1}, "vtxZ", "t_seed_corr_e0"));
        hc_p  .emplace_back(eb_eb.Filter("etaSCEle[0] > 1.3").Profile1D({"ele0_t_corr_vs_vtx_pfx", "", 50, -15, 15}, "vtxZ", "t_seed_corr_e0"));

        // run list
        // if a run_list file does not exists, compute it
        // N.B. the copy to vector triggers lazy actions, so better to be run only
        // when necessary, and use the values cached in a file otherwise
        std::vector<unsigned int> run_list;
        if (opts.count("runlist")) {
                run_list = opts["runlist"].as<std::vector<unsigned int>>();
        } else if (year.size()) {
                for (auto y : year) {
                        auto v = retrieve_run_list(comm, y);
                        run_list.insert(run_list.end(), v.begin(), v.end());
                }
        } else {
                // if no year and no runlist provided, recompute it
                run_list = retrieve_run_list(comm, -1);
        }

        //for (auto & r : run_list) std::cout << r << "\n";

        // delta_t vs effective amplitude
        hc_h2d.emplace_back(eb_eb.Histo2D({"global_delta_t_vs_aeff", "", 100, 0, 2500, 50, -3, 3}, "aeff_ee", "delta_t_ee_corr"));

        // take values for eff_sigma vs effective amplitude
        auto nbins = 10;
        auto m = 0.;
        auto M = 1500.;
        std::vector<ROOT::RDF::RResultPtr<std::vector<float> > > t_corr;
        std::vector<ROOT::RDF::RResultPtr<double> > a_mean;
        for (int i = 0; i < nbins; ++i) {
                auto bmin = m + (M - m) / nbins * i;
                auto bmax = m + (M - m) / nbins * (i + 1);
                // bin selection for Aeff
                auto bin_values = eb_eb.Filter("aeff_ee > " + std::to_string(bmin) + " && aeff_ee < " + std::to_string(bmax));
                t_corr.emplace_back(bin_values.Take<float>("delta_t_ee_corr"));
                a_mean.emplace_back(bin_values.Mean("aeff_ee"));
                // also get the 1D histogram corresponding to the distribution in the bin
                // - this could actually be retrieved directly from the 2D histogram above
                auto hname = "delta_t_ee_corr_bin" + std::to_string(i) + "_" + std::to_string((int)bmin) + "_" + std::to_string((int)bmax);
                hc_h1d.emplace_back(bin_values.Histo1D({hname.c_str(), "", 100, -2, 2.}, "delta_t_ee_corr"));
        }
        auto bin_values = eb_eb.Filter("aeff_ee > " + std::to_string(M));
        t_corr.emplace_back(bin_values.Take<float>("delta_t_ee_corr"));
        a_mean.emplace_back(bin_values.Mean("aeff_ee"));

        // entries vs run number
        int run_min = run_list.front() - 100;
        int run_max = run_list.back()  + 100;
        hc_h1d.emplace_back(eb_eb.Histo1D({"eb_eb_entries_vs_run", "", run_max - run_min, (float)run_min, (float)run_max}, "runNumber"));
        hc_h1d.emplace_back(eb_eb.Filter("aeff_ee > 500").Histo1D({"eb_eb_aeff500_entries_vs_run", "", run_max - run_min, (float)run_max, (float)run_min}, "runNumber"));

        // take values for eff_sigma vs run number
        std::vector<ROOT::RDF::RResultPtr<std::vector<float> > > t_corr_run;
        std::vector<ROOT::RDF::RResultPtr<double> > a_mean_run;
        std::vector<ROOT::RDF::RResultPtr<long long unsigned int> > count_run;
        for (auto r : run_list) {
                auto filtered = eb_eb.Filter("aeff_ee > 500 && runNumber == " + std::to_string(r));
                t_corr_run.emplace_back(filtered.Take<float>("delta_t_ee_corr"));
                a_mean_run.emplace_back(filtered.Mean("aeff_ee"));
                count_run.emplace_back(filtered.Count());
        }

        /*
         * all instant operations below this point - whenever possible
         */

        eb_eb.Report()->Print();

        // this triggers the execution of all the lazy operations
        // by dereferencing one of the pointers
        auto g_dt_effsigma_aeff = new TGraph(); g_dt_effsigma_aeff->SetNameTitle("delta_t_effsigma_vs_aeff", "delta_t_effsigma_vs_aeff");
        auto g_dt_stddev_aeff   = new TGraph(); g_dt_stddev_aeff  ->SetNameTitle("delta_t_stddev_vs_aeff", "delta_t_stddev_vs_aeff");
        auto g_dt_mean_aeff     = new TGraph(); g_dt_mean_aeff    ->SetNameTitle("delta_t_mean_vs_aeff", "delta_t_mean_vs_aeff");
        for (size_t i = 0; i < t_corr.size(); ++i) {
                g_dt_effsigma_aeff ->SetPoint(i, *a_mean[i], eff_sigma(*t_corr[i]));
                g_dt_stddev_aeff   ->SetPoint(i, *a_mean[i], stddev(*t_corr[i]));
                g_dt_mean_aeff     ->SetPoint(i, *a_mean[i], mean(*t_corr[i]));
        }
        hc_g.emplace_back(g_dt_effsigma_aeff);
        hc_g.emplace_back(g_dt_stddev_aeff);

        auto g_dt_effsigma_run = new TGraph(); g_dt_effsigma_run->SetNameTitle("delta_t_effsigma_vs_run", "delta_t_effsigma_vs_run");
        auto g_dt_mean_run     = new TGraph(); g_dt_mean_run->SetNameTitle("delta_t_mean_vs_run", "delta_t_mean_vs_run");
        int cnt = 0;
        for (size_t i = 0; i < t_corr_run.size(); ++i) {
                // remove runs with less than 50 entries
                if (debug) std::cout << "--> run " << run_list[i] << ": " << (*t_corr_run[i]).size() << " entries.\n";
                if ((*t_corr_run[i]).size() > 50) {
                        g_dt_effsigma_run->SetPoint(cnt, (float)run_list[i], eff_sigma(*t_corr_run[i]));
                        g_dt_mean_run    ->SetPoint(cnt, (float)run_list[i], mean(*t_corr_run[i]));
                        ++cnt;
                }
        }
        hc_g.emplace_back(g_dt_effsigma_run);
        hc_g.emplace_back(g_dt_mean_run);

        // save histograms
        std::string s = "";
        for (auto y : year) s += "_" + std::to_string(y);
        auto fout = TFile::Open(("out_plots" + s + ".root").c_str(), "recreate");
        for (auto h : hc_h1d) h->Write(); 
        for (auto h : hc_h2d) h->Write(); 
        for (auto p : hc_p)   p->Write(); 
        for (auto g : hc_g)   g->Write(); 
        fout->Close();

        return 0;
}
