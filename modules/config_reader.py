import re
import sys

class cfg_reader:
    def __init__  (self, cfgInputFile) :
        self.cfgName = cfgInputFile
        self.lines = []
        self.config = {}
        self.parseInputFileList()
        self.makeConfig()
    
    def parseInputFileList (self) :
        """ removes all comments and return cleaned list of lines"""
        filelist = []
        try :
            with open (self.cfgName) as fIn:
                for line in fIn:
                    line = (line.split("#")[0]).strip()
                    if line:
                        self.lines.append(line)
        except IOError:
            print("*** WARNING: cfg file " , self.cfgName , " not found")
            return

    def processOption (self, line) :
        """ processes an option line and returns a pair (name, value) """
        ll = line.split ('=', 1)
        if len (ll) < 2:
            print("Cannot parse option " , line)
            sys.exit()
        result = (ll[0].strip() , ll[1].strip())
        return result

    def makeConfig (self) :
        """ creates the dictionary organized as section::option --> VALUE (all strings!) """
        section = None
        for line in self.lines:
            m = re.search ('\[(.*)\]', line)
            if m and not '=' in line: # declaration of a new section. If a '=' is also found, it is considered as an assignment
                section = m.group(1)
                #print("new section: " , section)
                self.config[section] = {}
            else: # is an option
                if not section: # protection
                    print("Cannot parse config: there are entries outside a [section]")
                    sys.exit()
                pair = self.processOption (line)
                if pair[0] in self.config[section]:
                    self.config[section][pair[0]+"_"] = pair[1] #allow for multiple options (readMultiOption)
                else:
                    self.config[section][pair[0]] = pair[1]

    def readOption (self, optName) :
        """ read the config with the c++ style section::option ; also removes any non-alphanumeric symbol in optName """
        name = optName.split ('::')
        if len (name) < 2:
            print("readOption(): please pass option as section::option")
            return None
        # name[1] = re.sub('[\W_]+', '', name[1]) # removes all non-alphanumeric characters, not needed for latest parser
        sec = name[0]
        opt = name[1]
        if not sec in self.config:
            print("NO SEC" , sec , "in CONFIG")
            return None
        if not opt in self.config[sec]:
            print("NO OPT" , opt , "in CONFIG at" , sec)
            return None
        return self.config[sec][opt]

    def readListOption (self, optName) :
        """ read the config with the c++ style section::option and return a list of arguments (string) """
        result = self.readOption (optName)
        if not result:
            return None
        line = result.split(',')
        for i in range (0, len(line)) : line[i] = line[i].strip()
        #print(line)
        return line
        
    def readMultiOption (self, optName) :
        """ read the config with the c++ style section::option and return a list of arguments for each option instance"""
        name = optName.split ('::')
        if len (name) < 2:
            print("readOption(): please pass option as section::option")
            return None
        # name[1] = re.sub('[\W_]+', '', name[1]) # removes all non-alphanumeric characters, not needed for latest parser
        sec = name[0]
        opt = name[1]
        if not sec in self.config:
            print("NO SEC" , sec , "in CONFIG")
            return None
        result = []
        for i in self.config[sec]:
            if opt in i:
                result.append(self.config[sec][i])
        if not opt in self.config[sec]:
            print("NO OPT" , opt , "in CONFIG at" , sec)
            return None
        if not result:
            return None
        return result



    def hasOption (self, optName) :
        opt = self.readOption (optName)
        if not opt:
            return False
        else:
            return True

    def hasSection (self, secName) :
        if not secName in self.config:
            return False
        else:
            return True

