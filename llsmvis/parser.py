import numpy as np
import glob
import pprint
from datetime import datetime, timedelta
from llsmvis.globals import *
import pandas as pd


class LLSMParser:
    def __init__(self, fpath, fname_head, prefer_deskewed=True):
        """
        initialize the LLSMParser.
        :param fpath: path to the set of datafile
        :param fname_head: name head of the set of datafiles.
        """
        self.prefer_deskewed=prefer_deskewed
        self.channel_n = np.nan
        self.tsteps_n = np.nan
        self.fpath = fpath
        self.fname_head = fname_head
        try:
            self.all_tiffs = glob.glob(self.fpath + "/" + self.fname_head + "_ch*.tif")
        except OSError:
            pass

        try:
            self.deskewed_tiffs = glob.glob(self.fpath + "/results_dsk/" + self.fname_head + "_deskewed/Deskewed_"+self.fname_head+"*.tif")
            if VERBOSE:
                print(self.deskewed_tiffs)
        except OSError:
            pass

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

        # add some data specific information.
        self.pausing_time_between_stacks = None  # this should be the pausing time chose on LabView
        self.slice_number_per_stack = None
        self.estimated_acqT_per_stack = None
        self.estimated_stack_cycle_seconds = None
        self.estimated_stack_cycle_Hz = None
        self.laser_power = None
        self.acquisition_startT = None
        self.datetime_acq_start = None
        self.acquisition_endT = None
        self.camera_cycle_Hz = None
        self.camera_cycle_seconds = None
        self.camera_expo_ms = None
        self.stage_settle = None
        self.stage_settle_time_ms = None
        self.data_properties = None
        self.sort_tiff_dict()

    def what(self):
        """
        To display what methods are included in this class
        """
        print('LLSMParser contains the following methods:')
        print('LLSMParser.count_channel: \n \
            Count how many channels are there associated with the  \n \
            given fname_head, and return the channel number.  \n \
            It also set .channel_n attribute to the LLSMParser object. \n \
            ')
        print('LLSMParser.count_tsteps: \n \
            Count how many time steps are there associated with the  \n \
            given fname_head, and return the time steps number.  \n \
            It also set .tsteps_n attribute to the LLSMParser object. \n \
            ')

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
        if self.prefer_deskewed:
            if len(self.all_tiffs) > len(self.deskewed_tiffs):
                self.tsteps_n = sum(subs in s for s in self.all_tiffs)
            else:
                self.tsteps_n = sum(subs in s for s in self.deskewed_tiffs)
        else:
            self.tsteps_n = sum(subs in s for s in self.all_tiffs)
        return self.tsteps_n

    def sort_tiff_dict(self):
        """
        set the list of full-path of the tiff files corresponding to each channel and time steps.
        always give the deskewed tiffs a higher priority
        :return:
        """
        # prepare for time stamps
        self.parse_specs()
        if VERBOSE:
            print('length of all tiffs is ' + str(len(self.all_tiffs)))

        try:
            if self.prefer_deskewed:
                if len(self.all_tiffs) > 0:
                    ssec = self.all_tiffs[0].split(self.fname_head + "_")[1].split("_")[1]
                elif len(self.deskewed_tiffs) > 0:
                    # use deskewed tiffs instead to parse the information.
                    ssec = self.deskewed_tiffs[0].split("Deskewed_"+self.fname_head + "_")[1].split("_")[1]
            else:
                ssec = self.all_tiffs[0].split(self.fname_head + "_")[1].split("_")[1]
        except OSError:
            pass
        zfilln = len(ssec) - 5  # number of digits with zero-fill for the stack numbers.
        self.dict_tiffs = list()
        for chi in np.arange(0,self.channel_n):
            for ti in np.arange(0, self.tsteps_n):
                subs = self.fname_head + "_ch" + str(chi) + "_stack" + str(ti).zfill(zfilln) + "_"
                if self.prefer_deskewed:
                    if len(self.deskewed_tiffs) < len(self.all_tiffs):
                        f = [s for s in self.all_tiffs if subs in s]
                    else:
                        f = [s for s in self.deskewed_tiffs if subs in s]
                else:
                    f = [s for s in self.all_tiffs if subs in s]

                if len(f) == 1:
                    t_stamp=np.float(f[0].split('_')[-2].split('msec')[0]) # time stamp of the tiff file (ms)
                    curr_time = self.datetime_acq_start + timedelta(seconds=t_stamp/1000)
                    d = {
                      "fname_head":self.fname_head,
                      "channel name": self.channel_names[chi],
                      "channel index": chi,
                      "time step": ti,
                      "path of tiff": f[0],
                      "time stamp (ms)": t_stamp,
                      "time (datetime)":  curr_time,
                    }
                    self.dict_tiffs.append(d)
                else:
                    print("ambiguous file names: ")
                    print(f)

        self.dict_tstep0_tiffs = [s for s in self.dict_tiffs if s['time step'] == 0]
        self.get_data_properties()

    def set_channel_names(self, names):
        if len(names) == self.channel_n:
            self.channel_names = names
            self.sort_tiff_dict()
        else:
            print(" total channel number is " + str(self.channel_n) +", but " + str(len(names)) + " names are provided.")

    def get_sample_z_shift(self):
        # get sample_z_shift from the txt file.

        self.sample_z_shift = np.float([s for s in self.configs
                                          if "S PZT Offset, Interval (um), # of Pixels for Excitation (0) :"
                                          in s][0].split('\t')[2])  # this will pick up the Interval (um) value.
        return None

    def parse_specs(self):
        '''
        parse out the specs information of a dataset
        :return: None
        '''
        self.pausing_time_between_stacks = np.nan  # this number is not available from the .txt file.

        # self.time_delay_between_stacks =  # get time delay between stacks by parsing the file names.

        self.slice_number_per_stack = np.float([s for s in self.configs
                                          if "S PZT Offset, Interval (um), # of Pixels for Excitation (0) :"
                                          in s][0].split('\t')[3])  # this will pick up the Interval (um) value.

        self.laser_power = np.float([s for s in self.configs
                                          if "Excitation Filter, Laser, Power (%), Exp(ms) (0) :"
                                          in s][0].split('\t')[3])  # this will pick up the Interval (um) value.

        self.acquisition_startT = [s for s in self.configs  # this will pick up the Interval (um) value.
                                          if "Date :"
                                          in s][0].split('\t')[1].split('\n')[0]

        self.datetime_acq_start = datetime.strptime(self.acquisition_startT, '%m/%d/%Y %I:%M:%S %p')

        # self.acquisition_endT = np.float([s for s in self.configs
        #                                   if "S PZT Offset, Interval (um), # of Pixels for Excitation (0) :"
        #                                   in s][0].split('\t')[2])  # this will pick up the Interval (um) value.
        #
        self.camera_cycle_Hz = [s for s in self.configs
                                          if "Cycle(Hz) :"
                                          in s][0].split('\t')[1].split('\n')[0]

        self.camera_cycle_seconds = np.float([s for s in self.configs
                                          if "Cycle(s) :"
                                          in s][0].split('\t')[1])  # this will pick up the Interval (um) value.

        self.camera_expo_ms = np.float([s for s in self.configs
                                          if "Excitation Filter, Laser, Power (%), Exp(ms) (0) :"
                                          in s][0].split('\t')[4])  # this will pick up the Interval (um) value.

        self.stage_settle = [s for s in self.configs  # this will pick up the Interval (um) value.
                                          if "Add extra time = "
                                          in s][0].split(' ')[4].split('\n')[0]

        self.stage_settle_time_ms = np.float([s for s in self.configs  # this will pick up the Interval (um) value.
                                          if "Added time (ms) = "
                                          in s][0].split(' ')[4].split('\n')[0])

        self.estimated_acqT_per_stack = self.slice_number_per_stack * self.camera_cycle_seconds

        self.estimated_stack_cycle_seconds = self.estimated_acqT_per_stack * self.channel_n

        self.estimated_stack_cycle_Hz = 1 / self.estimated_stack_cycle_seconds

        return None

    def get_data_properties(self):
        exp = str(self.camera_expo_ms) + ' ms'
        acqT_per_stack = str(self.estimated_acqT_per_stack) + ' s/V/C'
        # find the average time interval between time steps. use the first channel to estimate.
        for t in self.dict_tiffs:
            if t['time step'] == 0:
                if t['channel index'] == 0:
                    if VERBOSE: print('setting t1')
                    t1 = t['time stamp (ms)']
                    totaldt = 0
            elif t['time step'] == self.tsteps_n - 1:
                if t['channel index'] == 0:
                    if VERBOSE: print('setting t2')
                    t2 = t['time stamp (ms)']
                    totaldt = t2 - t1

        interval = totaldt / 1000 / self.tsteps_n
        tint='{:.2f} s'.format(interval)
        if interval > 0:
            cycle_hz = '{:02.3f}'.format(1/interval) + ' Hz'
        else:
            cycle_hz = 'nan'
        cycle_s = '{:.3f}'.format(self.estimated_stack_cycle_seconds) + ' s/V'
        df = pd.DataFrame()
        df['data properties'] = ['file name',
                                 'start time',
                                 'channels',
                                 'slice number per V',
                                 'slice interval (z-piezo step)',
                                 'laser power(%)',
                                 'exposure time per slice',
                                 'acquisition time per volume/channel',
                                 'average all-channel acquisition T (s)',
                                 'average time per V \n(acq-T + pausing/settling-T)',
                                 'average time resolution (Hz)',
                                 ]
        df['values'] = [self.fname_head,  # file name
                        self.acquisition_startT,  # start time
                        self.channel_names,  # channels
                        str(self.slice_number_per_stack),
                        str(self.sample_z_shift) + ' microns',
                        self.laser_power,  # laser power(%)
                        exp,  # exposure time per slice
                        acqT_per_stack,  # acquisition time per V per C
                        cycle_s,  # all-channel cycle (s)
                        tint,  # average time interval per V
                        cycle_hz,  # all-channel cycle (Hz)
                        ]
        self.data_properties = df
        return None

    def info(self):
        """
        print out some basic information about this object
        :return: none
        """
        print("\n\n")
        print("file name prefix: \"" + self.fname_head + "\"")
        print("file path: " + self.fpath)
        print("channel number: " + str(self.channel_n))
        print("number of time steps: " + str(self.tsteps_n))
        print("")
        print("example tiffs dictionary item:\n")
        pprint.pprint(self.dict_tiffs[0])
        print('\n============================================\n')
        print("ATTRIBUTES:")
        for key, value in self.__dict__.items():
            if key is "dict_tiffs":
                print(
                    "self." + key + ":  [hidden], a list of all the tiffs, with one element being a dictionary containing info"
                                    " of one tiff")
                print('Example:')
                pprint.pprint(self.dict_tiffs[0])
                print('\n')
            elif key is "all_tiffs":
                print(
                    "self." + key + ":  [hidden], a list of all the tiffs, with one element being the string of the path of one"
                                    "tiff")
                if len(self.all_tiffs) > len(self.deskewed_tiffs):
                    print('Example:')
                    print(self.all_tiffs[0])
                    print('\n')
                else:
                    print('\n raw data was partially or completely deleted, look at self.deskewed_tiffs instead\n')
            elif key is "deskewed_tiffs":
                print(
                    "self." + key + ":  [hidden], a list of all the deskewed tiffs, with one element being the string of the path of one"
                                    "tiff")
                if len(self.deskewed_tiffs) > 0:
                    print('Example:')
                    print(self.deskewed_tiffs[0])
                    print('\n')
                else:
                    print('\n no data is deskewed as of yet\n')
            elif key is "configs":
                print("self." + key + ":  [hidden], a list of configurations, str lines from the txt file")
                print('Example:')
                print(self.configs[3])
                print('\n')
            elif key is "data_properties":
                print("self." + key + ":  [hidden], pandas.DataFrame, a small table with data properties")
            else:
                print("self." + key + ":  " + str(value))


class LLSMGroupParser1s1t:
    """
    when a time series belong to the same feature, but each stack has its own _Settings.txt file.
    Use this group parser and use the parsers for the individual stacks as input (organized as a list)
    1s1t: this means 1 *_Settings.txt file per one time step, but may contain multiple channels
    """

    def __init__(self, fpath, fname_head):
        self.fname_head = fname_head
        # 1. get all the _Settings.txt file with the csubs
        self.all_settings_fname = [x for x in os.listdir(fpath) if x.endswith('.txt') and x.startswith(fname_head)]
        # 2. a regular parser for all these stacks
        # 2.1 get fname_head for each specific *Settings.txt file
        self.indiv_fname_heads = [];  # indiviudal fname_heads for each *_Setting.txt
        for n in self.all_settings_fname:
            self.indiv_fname_heads.append(n[:-13])
        return

    def get_indiv_parsers(self):
        """
        get individual parsers for all the _Setting.txt file.
        """
        self.indiv_parsers = []
        for n in self.indiv_fname_heads:
            p = LLSMParser(fpath, n, prefer_deskewed=False)
            self.indiv_parsers.append(p)
        return

    def valid_check(self):
        # go through all the parsers and makes ure there is only one .tiff stack involved.
        self.valid = True
        for p in self.indiv_parsers:
            if len(p.dict_tiffs) != len(p.channel_names):
                self.valid = False
        return self.valid

    def get_parser_time_indexes(self):
        # group all the parsers based on time for the first channel_indx
        # first, go through all parsers and take out the time and index as a np.ndarray
        time_n_inds = np.ndarray([len(self.indiv_parsers), 2], dtype='int')
        for ind, p in enumerate(self.indiv_parsers):
            time_n_inds[ind, 0] = self.datetime_to_integer(p.datetime_acq_start);
            time_n_inds[ind, 1] = ind;
        self.time_n_inds = time_n_inds;
        a = time_n_inds;
        self.sorted_time_n_inds = a[a[:, 0].argsort(), :]
        return self.sorted_time_n_inds

    def sort_parsers_by_time(self):
        self.time_sorted_indiv_parsers = []
        for ind in self.sorted_time_n_inds[:, 1]:
            self.time_sorted_indiv_parsers.append(gp.indiv_parsers[ind])

    def datetime_to_integer(self, t):
        return np.int(1e12 * t.year + 1e10 * t.month + 1e8 * t.day + 1e6 * t.hour + 1e4 * t.minute + 1e2 * t.second)