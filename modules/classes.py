import matplotlib as mpl
import matplotlib.pyplot as plt

class histo1D:
	def __init__(self, var, config):
		self.var = var
		self.binning    = self.get_binning(config)
		self.selections = self.get_selections(config)
		self.options    = self.get_options(config)

	def get_binning(self, config):
		if not self.var in config.config['binning']: 
			print("### WARNING: no binning provided for ", self.var, ", using dummy")
		else:
			binning = [float(s) for s in config.config['binning'][self.var].split(",")]
			binning[0] = int(binning[0])
		return binning
	
	def get_selections(self, config):
		if self.var in config.config["hselections"]: 
			selections = config.readOption("hselections::"+self.var).split(",")
		else:
			selections = ["all"]
		return [sel.strip() for sel in selections]
	
	def get_options(self, config):
		if self.var in config.config['hoptions']:
			options = config.readOption("hoptions::"+self.var).split(",")
		return [opt.strip() for opt in options]
	
	def plot(self, df):
		if len(self.binning) > 0:
		    plot = plt.hist(df[self.var], self.binning[0], range = self.binning[-2:])
		else: 
		    plot = plt.hist(df[self.var])
		return plot
	
	def outlier_aware_hist(self, df):
		if len(self.binning) == 0: 
			print("### WARNING: no binning provided for ", self.var, ", skipping underflow/overflow histogram")
			return 0
	
		nbins = self.binning[0]
		lower , upper = self.binning[-2:]
		data = df[self.var]
		
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
	
		bincontent, edge, patches = plt.hist(data, bins = nbins,range=(lower, upper))
		
		if lower_outliers:
			n_lower_outliers = (data < lower).sum()
			bincontent[0] = (bincontent[0] + n_lower_outliers)
			patches[0].set_label('Lower outliers: ({:.2f}, {:.2f})'.format(data.min(), lower))
			print('Lower outliers: ({:.2f}, {:.2f}), n = {:.2f}'.format(data.min(), lower, n_lower_outliers))
		
		if upper_outliers:
			n_upper_outliers = (data > upper).sum()
			bincontent[-1] = (bincontent[-1] + n_upper_outliers)
			patches[-1].set_label('Upper outliers: ({:.2f}, {:.2f})'.format(upper, data.max()))
			print('Upper outliers: ({:.2f}, {:.2f}),  n = {:.2f}'.format(upper, data.max(), n_upper_outliers))
	
		return [bincontent,edge,patches]



class histo2D:
	def __init__(self, var, config):
		varx, vary, name = var.split(':')
		self.varx = varx.strip()
		self.vary = vary.strip()
		self.name = name.strip()
		self.xbinning, self.xcustom    = self.get_binning(config, "X")
		self.ybinning, self.ycustom    = self.get_binning(config, "Y")
		self.selections = self.get_selections(config)


	def get_binning(self,config,axis):
		if not axis+"@"+self.name in config.config['binning2D']: 
			print("### WARNING: no "+axis+" binning provided for ", self.name, ", skipping")
		binning = [float(s) for s in config.config['binning2D'][axis+"@"+self.name].split(",")]
		binning[0] = int(binning[0])
		custom = False
		if axis+"@"+self.name in config.config['custom_binning2D']: 
			custom = True
			binning = [float(s) for s in config.config['custom_binning2D'][axis+"@"+self.name].split(",")]
		return binning, custom
		
	def get_selections(self, config):
		if self.name in config.config["hselections2D"]: 
			selections = config.readOption("hselections2D::"+self.name).split(",")
		else:
			selections = ["all"]
		return [sel.strip() for sel in selections]

	def plot(self, df):
		if self.xcustom:
			if self.ycustom :
				plot = plt.hist2d(df[self.varx], df[self.vary], bins = [self.xbinning,self.ybinning])
			else:
				plot = plt.hist2d(df[self.varx], df[self.vary], bins = [self.xbinning,self.ybinning[0]], range = [[self.xbinning[0], self.xbinning[-1]], self.ybinning[-2:]])
		else:
			if self.ycustom:
				plot = plt.hist2d(df[self.varx], df[self.vary], bins = [self.xbinning[0],self.ybinning], range = [self.xbinning[-2:], [self.ybinning[0], self.ybinning[-1]]])
			else:
				plot = plt.hist2d(df[self.varx], df[self.vary], bins = [self.xbinning[0],self.ybinning[0]], range = [self.xbinning[-2:], self.ybinning[-2:]])
		return plot