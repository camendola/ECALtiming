import matplotlib as mpl
import matplotlib.pyplot as plt
import modules.compute_variables as compute
import pandas as pd
import numpy as np


class histo1d:
    def __init__(self, var, config):
        self.var = var
        self.binning = self.get_binning(config)
        self.selections = self.get_selections(config)
        self.options = self.get_options(config)

    def get_binning(self, config):
        if not self.var in config.config["binning"]:
            print("### WARNING: no binning provided for ", self.var, ", using dummy")
        else:
            binning = [float(s) for s in config.config["binning"][self.var].split(",")]
            binning[0] = int(binning[0])
        return binning

    def get_selections(self, config):
        if self.var in config.config["hselections"]:
            selections = config.readOption("hselections::" + self.var).split(",")
        else:
            selections = ["all"]
        return [sel.strip() for sel in selections]

    def get_options(self, config):
        options = []
        if self.var in config.config["hoptions"]:
            options = config.readOption("hoptions::" + self.var).split(",")
        return [opt.strip() for opt in options]

    def plot(self, df):
        if len(self.binning) > 0:
            plot = plt.hist(df, self.binning[0], range=self.binning[-2:])
        else:
            plot = plt.hist(df)
        return plot

    def outlier_aware_hist(self, df):
        if len(self.binning) == 0:
            print(
                "### WARNING: no binning provided for ",
                self.var,
                ", skipping underflow/overflow histogram",
            )
            return 0

        nbins = self.binning[0]
        lower, upper = self.binning[-2:]
        data = df

        if not lower or (lower < (data.min())):
            lower = data.min()
            lower_outliers = False
        else:
            lower_outliers = True

        if not upper or upper > data.max():
            upper = data.max()
            upper_outliers = False
        else:
            upper_outliers = True

        bincontent, edge, patches = plt.hist(data, bins=nbins, range=(lower, upper))

        if lower_outliers:
            n_lower_outliers = (data < lower).sum()
            bincontent[0] = bincontent[0] + n_lower_outliers
            patches[0].set_label(
                "Lower outliers: ({:.2f}, {:.2f})".format(data.min(), lower)
            )
            print(
                "Lower outliers: ({:.2f}, {:.2f}), n = {:.2f}".format(
                    data.min(), lower, n_lower_outliers
                )
            )

        if upper_outliers:
            n_upper_outliers = (data > upper).sum()
            bincontent[-1] = bincontent[-1] + n_upper_outliers
            patches[-1].set_label(
                "Upper outliers: ({:.2f}, {:.2f})".format(upper, data.max())
            )
            print(
                "Upper outliers: ({:.2f}, {:.2f}),  n = {:.2f}".format(
                    upper, data.max(), n_upper_outliers
                )
            )

        return [bincontent, edge, patches]


class histo2d:
    def __init__(self, var, config):
        varx, vary, name = var.split(":")
        self.varx = varx.strip()
        self.vary = vary.strip()
        self.name = name.strip()
        self.xbinning, self.xcustom = self.get_binning(config, "X")
        self.ybinning, self.ycustom = self.get_binning(config, "Y")
        self.selections = self.get_selections(config)
        self.options = self.get_options(config)

    def get_binning(self, config, axis):
        if not axis + "@" + self.name in config.config["binning2D"]:
            print(
                "### WARNING: no " + axis + " binning provided for ",
                self.name,
                ", skipping",
            )
        binning = [
            float(s)
            for s in config.config["binning2D"][axis + "@" + self.name].split(",")
        ]
        binning[0] = int(binning[0])
        custom = False
        if axis + "@" + self.name in config.config["custom_binning2D"]:
            custom = True
            binning = [
                float(s)
                for s in config.config["custom_binning2D"][
                    axis + "@" + self.name
                ].split(",")
            ]
        return binning, custom

    def get_selections(self, config):
        if self.name in config.config["hselections2D"]:
            selections = config.readOption("hselections2D::" + self.name).split(",")
        else:
            selections = ["all"]
        return [sel.strip() for sel in selections]

    def get_options(self, config):
        options = []
        if self.name in config.config["hoptions2D"]:
            options = config.readOption("hoptions2D::" + self.name).split(",")
        return [opt.strip() for opt in options]

    def plot(self, df, do_density):
        if self.xcustom:
            if self.ycustom:
                plot = plt.hist2d(
                    df[self.varx],
                    df[self.vary],
                    bins=[self.xbinning, self.ybinning],
                    density=True,
                )
            else:
                plot = plt.hist2d(
                    df[self.varx],
                    df[self.vary],
                    bins=[self.xbinning, self.ybinning[0]],
                    range=[[self.xbinning[0], self.xbinning[-1]], self.ybinning[-2:]],
                    density=do_density,
                )
        else:
            if self.ycustom:
                plot = plt.hist2d(
                    df[self.varx],
                    df[self.vary],
                    bins=[self.xbinning[0], self.ybinning],
                    range=[self.xbinning[-2:], [self.ybinning[0], self.ybinning[-1]]],
                    density=True,
                )
            else:
                plot = plt.hist2d(
                    df[self.varx],
                    df[self.vary],
                    bins=[self.xbinning[0], self.ybinning[0]],
                    range=[self.xbinning[-2:], self.ybinning[-2:]],
                    density=do_density,
                )
        return plot


class graph:
    def __init__(self, var, config):
        varx, vary = var.split(":")
        self.var = var
        self.varx = varx.strip()
        self.vary = vary.strip()
        self.name = self.vary + "_vs_" + self.varx
        self.binning = self.get_binning(config)
        self.selections = self.get_selections(config)
        self.options = self.get_options(config)

    def get_binning(self, config):
        binning = []
        if self.var in config.config["grmarkerwidth"]:
            cfg_binning = config.readOption("grmarkerwidth::" + self.var).split(",")
            if len(cfg_binning) == 3:
                bins, xmin, xmax = cfg_binning
                xmin = float(xmin.strip())
                xmax = float(xmax.strip())
                bins = float(bins.strip())
                width = (xmax - xmin) / bins
                binning = np.arange(xmin, xmax + float(width), float(width))
            else:
                binning = np.asarray(cfg_binning, dtype=np.float32)
        return binning

    def get_selections(self, config):
        if self.var in config.config["grselections"]:
            selections = config.readOption("grselections::" + self.var).split(",")
        else:
            selections = ["all"]
        return [sel.strip() for sel in selections]

    def get_options(self, config):
        if self.var in config.config["groptions"]:
            options = config.readOption("groptions::" + self.var).split(",")
        return [opt.strip() for opt in options]

    def plot_simple(self, df, aggr_var):
        if len(self.binning) > 0:
            graph = df.groupby(pd.cut(df[self.varx], self.binning))[self.vary]
        else:
            graph = df.groupby(self.varx)[self.vary]
        if hasattr(compute, aggr_var):
            aggr_graph = graph.agg(getattr(compute, aggr_var))
        elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var):
            aggr_graph = getattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var)(
                graph
            )
        else:
            print("### WARNING: ", aggr_var, " not defined, skipping")
        plot = aggr_graph.plot()
        return plot

    def plot(self, df, aggr_var, args, size):
        if args.byrun:
            return self.plot_byrun(df, aggr_var)
        elif args.byrunsize:
            return self.plot_byrunsize(df, aggr_var, size)
        elif args.bysize:
            return self.plot_bysize(df, aggr_var, size)
        else:
            return self.plot_simple(df, aggr_var)

    def plot_byrun(self, df, aggr_var):
        graph = df.groupby("runNumber")[self.vary]
        if hasattr(compute, aggr_var):
            aggr_graph = graph.agg(getattr(compute, aggr_var))
        elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var):
            aggr_graph = getattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var)(
                graph
            )
        plot = aggr_graph.plot()
        return plot

    def plot_byrunsize(self, df, aggr_var, size):
        graph = df.groupby(["runNumber", df.groupby("runNumber").cumcount() // size])[
            self.varx, self.vary
        ]
        if hasattr(compute, aggr_var):
            aggr_graph = graph.agg(
                {self.varx: "mean", self.vary: getattr(compute, aggr_var)}
            )
        elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var):
            aggr_graph = graph.agg({self.vary: aggr_var})
            aggr_graph = aggr_graph.droplevel(0, axis=1)
        plot = aggr_graph.plot(x=self.varx, y=self.vary)
        return plot

    def plot_bysize(self, df, aggr_var, size):
        graph = df.groupby(np.arange(len(df)) // size)[self.varx, self.vary]
        if hasattr(compute, aggr_var):
            aggr_graph = graph.agg(
                {self.varx: "mean", self.vary: getattr(compute, aggr_var)}
            )
        elif hasattr(pd.core.groupby.generic.DataFrameGroupBy, aggr_var):
            aggr_graph = graph.agg({self.vary: aggr_var})
            aggr_graph = aggr_graph.droplevel(0, axis=1)
        plot = aggr_graph.plot(x=self.varx, y=self.vary)
        return plot


class map2d:
    def __init__(self, var, config):
        varx, vary, varz = var.split(":")
        self.var = var
        self.varx = varx.strip()
        self.vary = vary.strip()
        self.varz = varz.strip()
        self.name = self.varz + "_" + self.vary + "_vs_" + self.varx
        self.selections = self.get_selections(config)
        self.options = self.get_options(config)

    def get_selections(self, config):
        if self.var in config.config["mselections"]:
            selections = config.readOption("mselections::" + self.var).split(",")
        else:
            selections = ["all"]
        return [sel.strip() for sel in selections]

    def get_options(self, config):
        if self.var in config.config["moptions"]:
            options = config.readOption("moptions::" + self.var).split(",")
        return [opt.strip() for opt in options]

    def plot(self, df, aggr_var):
        if hasattr(compute, aggr_var):
            table = pd.pivot_table(
                df,
                index=self.vary,
                columns=self.varx,
                values=self.varz,
                aggfunc=getattr(compute, aggr_var),
            )
        elif hasattr(np, aggr_var):
            table = pd.pivot_table(
                df,
                index=self.vary,
                columns=self.varx,
                values=self.varz,
                aggfunc=getattr(np, aggr_var),
            )
        table.dropna()
        table.dropna(axis=1)
        return plot
