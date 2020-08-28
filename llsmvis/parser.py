import numpy as np
import glob
import pprint
from llsmvis.globals import *

class LLSMParser:
    def __init__(self, fpath, fname_head):
        """
        initialize the LLSMParser.
        :param fpath: path to the set of datafile
        :param fname_head: name head of the set of datafiles.
        """
        self.channel_n = np.nan
        self.tsteps_n = np.nan
        self.fpath = fpath
        self.fname_head = fname_head
        self.all_tiffs = glob.glob(self.fpath + "/" + self.fname_head + "*.tif")
        self.dict_tiffs = list()
        with open(fpath + "/" + fname_head + "_Settings.txt", "r") as f:
            self.configs = f.readlines()
        self.count_channel()
        self.count_tsteps()
        self.channel_names = ['channel'+str(x) for x in np.arange(self.channel_n)]  # default channel  names
        self.sample_z_shift = np.nan
        self.dict_tstep0_tiffs = list()
        self.get_sample_z_shift()
        self.idx_offset = np.array([0, 0, 0])
        self.sort_tiff_dict()

    def count_channel(self):
        """
        count total number of channels
        :return: channel_n: the total number of channels.
        """
        subs = "X Galvo Offset, Interval (um), # of Pixels for Excitation"
        self.channel_n = sum(subs in s for s in self.configs)
        return self.channel_n

    def count_tsteps(self):
        """
        count total number of time steps
        :return: tsteps_n: the total number of time steps.
        """
        subs = self.fname_head + "_ch0_stack"
        self.tsteps_n = sum(subs in s for s in self.all_tiffs)
        return self.tsteps_n

    def sort_tiff_dict(self):
        """
        set the list of full-path of the tiff files corresponding to each channel and time steps.
        :return:
        """
        ssec = self.all_tiffs[0].split(self.fname_head + "_")[1].split("_")[1]
        zfilln = len(ssec) - 5  # number of digits with zero-fill for the stack numbers.
        self.dict_tiffs = list()
        for chi in np.arange(0,self.channel_n):
            for ti in np.arange(0, self.tsteps_n):
                subs = self.fname_head + "_ch" + str(chi) + "_stack" + str(ti).zfill(zfilln) + "_"
                f = [s for s in self.all_tiffs if subs in s]
                if len(f) == 1:
                    d = {
                      "channel name": self.channel_names[chi],
                      "channel index": chi,
                      "time step": ti,
                      "path of tiff": f[0]
                    }
                    self.dict_tiffs.append(d)
                else:
                    print("ambiguous file names: ")
                    print(f)
        self.dict_tstep0_tiffs = [s for s in self.dict_tiffs if s['time step'] == 0]

    def set_channel_names(self, names):
        if len(names) == self.channel_n:
            self.channel_names = names
            self.sort_tiff_dict()  # resort the tiff list dictionary
        else:
            print(" total channel number is " + str(self.channel_n) +", but " + str(len(names)) + " names are provided.")

    def get_sample_z_shift(self):
        # get sample_z_shift from the txt file.

        self.sample_z_shift = np.float([s for s in self.configs
                                          if "S PZT Offset, Interval (um), # of Pixels for Excitation (0) :"
                                          in s][0].split('\t')[2])  # this will pick up the Interval (um) value.
        return None

    def info(self):
        """
        print out some basic information about this object
        :return: none
        """
        print("\n\n")
        print("          file name prefix: \"" + self.fname_head+"\"")
        print("          file path: " + self.fpath)
        print("          channel number: " + str(self.channel_n))
        print("          number of time steps: " + str(self.tsteps_n))
        print("")
        print("example tiffs dictionary item:\n")
        pprint.pprint(self.dict_tiffs[0])
        print('\n============================================\n')
        print("ATTRIBUTES:")
        for key, value in self.__dict__.items():
            if key is "dict_tiffs":
                print("self." + key + ":  [hidden], a list of all the tiffs, with one element being a dictionary containing info"
                            " of one tiff")
                print('Example:')
                pprint.pprint(self.dict_tiffs[0])
                print('\n')
            elif key is "all_tiffs":
                print("self." + key + ":  [hidden], a list of all the tiffs, with one element being the string of the path of one"
                            "tiff")
                print('Example:')
                print(self.all_tiffs[0])
                print('\n')
            elif key is "configs":
                print("self." + key + ":  [hidden], a list of configurations, str lines from the txt file")
                print('Example:')
                print(self.configs[0])
                print('\n')
            else:
                print("self." + key + ":  " + str(value))
                print('\n')

