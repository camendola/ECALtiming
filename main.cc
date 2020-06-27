// C++ version of the python analysis
// - hopefully to fix memory issues
// compile as a usual root code, e.g.
//   g++ main.cc -O3 -std=c++14 `root-config --libs --cflags`

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RResultPtr.hxx"
#include "ROOT/RVec.hxx"

#include "modules/functions.cc"

#define debug        0
#define eb_threshold "1.479"

using RVec_f = const ROOT::RVec<float> &;


ROOT::RVec<float> time_correction_vtx(float z, RVec_f eta, RVec_f t)
{
        ROOT::RVec<float> t_corr(2);
        auto l = 130. * cosh(eta[0]);
        t_corr = t - (sqrt(l * l + z * z - 2 * z * l * tanh(eta)) - l) * 0.0299792458;
        return t_corr;
}


std::vector<unsigned int> retrieve_run_list(ROOT::RDF::RNode df)
{
        FILE * fd = fopen("runs.list", "r");
        std::vector<unsigned int> run_list;
        if (!fd) {
                ROOT::RDF::RResultPtr<std::vector<unsigned int> > runs = df.Take<unsigned int>("runNumber");
                auto tmp = runs.GetValue();
                std::sort(tmp.begin(), tmp.end());
                auto last = std::unique(tmp.begin(), tmp.end());
                tmp.erase(last, tmp.end());
                run_list = std::move(tmp);
                FILE * fd = fopen("runs.list", "w");
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
        std::vector<std::string> input_files = retrieve_files(2016);
        for (auto & s : input_files) std::cout << s << "\n";

        ROOT::EnableImplicitMT();
        //ROOT::RDataFrame df("selected", input_files);
        ROOT::RDataFrame df("selected", "/home/ferri/data/ecalelf/ntuples/13TeV/ALCARERECO/103X_dataRun2_v6_ULBaseForICs_FinalEtaSv2_newRegV1/DoubleEG-ZSkim-Run2016B-07Aug17_ver2/273150-275376/271036-284044_PromptReco/pedNoise/DoubleEG-ZSkim-Run2016B-07Aug17_ver2-273150-275376.root");

        // selections

        // geometry
        auto ee           = "abs(etaSCEle[0]) > " eb_threshold " && abs(etaSCEle[1]) > " eb_threshold;
        auto ee_plus      = "etaSCEle[0] > " eb_threshold " && etaSCEle[1] > " eb_threshold;
        auto ee_minus     = "etaSCEle[0] < -" eb_threshold " && etaSCEle[1] < -" eb_threshold;
        auto be           = "(abs(etaSCEle[0]) > " eb_threshold " && abs(etaSCEle[1]) < " eb_threshold ") || "
                            "(abs(etaSCEle[0]) < " eb_threshold " && abs(etaSCEle[1]) > " eb_threshold ")";
        auto bb           = "abs(etaSCEle[0]) < " eb_threshold " && abs(etaSCEle[1]) < " eb_threshold;

        auto no_borders_0 = "((ySeedSC[0] % 20 + 1) > 2) && ((ySeedSC[0] % 20 + 1) < 18) && (abs(xSeedSC[0]) > 2) && (abs(ySeedSC[0]) < 24)";
        auto no_borders_1 = "((ySeedSC[1] % 20 + 1) > 2) && ((ySeedSC[1] % 20 + 1) < 18) && (abs(xSeedSC[1]) > 2) && (abs(ySeedSC[1]) < 24)";

        // objects
        auto clean_ee     = "abs(delta_t_ee) < 5";

        auto clean_e_0    = "abs(deltaT_e0_seeds) < 5";
        auto rel_ampl_0   = "abs(amplitudeSeedSC[0] - amplitudeSecondToSeedSC[0]) / (amplitudeSeedSC[0] + amplitudeSecondToSeedSC[0]) < 0.1)";

        auto clean_e_1    = "abs(deltaT_e1_seeds) < 5";
        auto rel_ampl_1   = "abs(amplitudeSeedSC[1] - amplitudeSecondToSeedSC[1]) / (amplitudeSeedSC[1] + amplitudeSecondToSeedSC[1]) < 0.1)";

        // physics
        auto z_mass       = "invMass > 85 && invMass < 95";
        auto high_r9      = "R9Ele[0] > 0.94 && R9Ele[1] > 0.94";

        // to debug columns
        //for (auto & el : df.GetColumnNames()) std::cout << el << "\n";

        // new quantities
        auto fn = df.Define("delta_t_ee", "timeSeedSC[0] - timeSeedSC[1]")
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
                    .Define("delta_t_ee_corr", "t_seed_corr[0] - t_seed_corr[1]");

        // reasonable quality selections and no gain switch
        auto comm = fn.Filter(z_mass).Filter(high_r9).Filter(clean_ee).Filter("gainSeedSC[0] == 0 && gainSeedSC[1] == 0");

        // histogram and graph collectors
        std::vector<ROOT::RDF::RResultPtr<TH1D> > hc_h1d;
        std::vector<ROOT::RDF::RResultPtr<TH2D> > hc_h2d;
        std::vector<ROOT::RDF::RResultPtr<TProfile> > hc_p;
        std::vector<const TGraph *> hc_g;

        // common selections
        auto eb_eb = comm.Filter(bb);
        auto eb_ee = comm.Filter(be);
        auto ee_ee = comm.Filter(ee);

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
        // N.B. the copy to set triggers lazy actions, so better to be run only
        // when necessary, and use the values cached in a file otherwise
        std::vector<unsigned int> run_list = retrieve_run_list(comm);
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
        hc_h1d.emplace_back(eb_eb.Histo1D({"eb_eb_entries_vs_run", "", 11000, 273100, 284100}, "runNumber"));
        hc_h1d.emplace_back(eb_eb.Filter("aeff_ee > 500").Histo1D({"eb_eb_aeff500_entries_vs_run", "", 11000, 273100, 284100}, "runNumber"));

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

        // this triggers the execution of all the lazy operations
        // by dereferencing one of the pointers
        auto g_dt_effsigma_aeff = new TGraph(); g_dt_effsigma_aeff->SetNameTitle("delta_t_effsigma_vs_aeff", "delta_t_effsigma_vs_aeff");
        auto g_dt_stddev_aeff   = new TGraph(); g_dt_stddev_aeff  ->SetNameTitle("delta_t_stddev_vs_aeff", "delta_t_stddev_vs_aeff");
        auto g_dt_mean_aeff     = new TGraph(); g_dt_mean_aeff    ->SetNameTitle("delta_t_mean_vs_aeff", "delta_t_mean_vs_aeff");
        for (size_t i = 0; i < t_corr.size(); ++i) {
                g_dt_effsigma_aeff ->SetPoint(i, *a_mean[i], eff_sigma(*t_corr[i]));
                g_dt_stddev_aeff   ->SetPoint(i, *a_mean[i], stddev(*t_corr[i]));
                g_dt_mean_aeff     ->SetPoint(i, *a_mean[i], mean(*t_corr[i]));
                std::cout << "--> " << *a_mean[i] << " " << mean(*t_corr[i]) << " " << stddev(*t_corr[i]) << " " << eff_sigma(*t_corr[i]) << "\n";
        }
        hc_g.emplace_back(g_dt_effsigma_aeff);
        hc_g.emplace_back(g_dt_stddev_aeff);

        auto g_dt_effsigma_run = new TGraph(); g_dt_effsigma_run->SetNameTitle("delta_t_effsigma_vs_run", "delta_t_effsigma_vs_run");
        auto g_dt_mean_run     = new TGraph(); g_dt_mean_run->SetNameTitle("delta_t_mean_vs_run", "delta_t_mean_vs_run");
        int cnt = 0;
        for (size_t i = 0; i < t_corr_run.size(); ++i) {
                // remove runs with less than 50 entries
                if ((*t_corr_run[i]).size() > 50) {
                        if (debug) std::cout << "--> taking run " << run_list[i] << ": " << (*t_corr_run[i]).size() << " entries.\n";
                        g_dt_effsigma_run->SetPoint(cnt, (float)run_list[i], eff_sigma(*t_corr_run[i]));
                        g_dt_mean_run    ->SetPoint(cnt, (float)run_list[i], mean(*t_corr_run[i]));
                        ++cnt;
                } else {
                        if (debug) std::cout << "--> skipping run " << run_list[i] << ": " << (*t_corr_run[i]).size() << " entries.\n";
                }
        }
        hc_g.emplace_back(g_dt_effsigma_run);
        hc_g.emplace_back(g_dt_mean_run);

        // save histograms
        auto fout = TFile::Open("out_plots.root", "recreate");
        for (auto h : hc_h1d) h->Write(); 
        for (auto h : hc_h2d) h->Write(); 
        for (auto p : hc_p)   p->Write(); 
        for (auto g : hc_g)   g->Write(); 
        fout->Close();

        return 0;
}
