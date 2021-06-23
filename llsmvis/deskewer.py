from skimage import io
import numpy as np
import os
import skimage.external.tifffile
from llsmvis.globals import *
import pickle
from scipy import interpolate

class Deskewer:
    def __init__(self, parser):
        # attach parser to the Deskewer
        self.p = parser
        #  create output path for deskewed tiffs
        self.path_o = parser.fpath + '/results_dsk/' + self.p.fname_head + '_deskewed'
        self.singleslices = False
        print("Deskewing dataset:\n    " + self.p.fpath + "/" + self.p.fname_head)
        try:
            if not os.path.exists(parser.fpath+'/results_dsk'):
                os.mkdir(parser.fpath+'/results_dsk')
                print("\n results_dsk folder for the collection of datasets created:")
                print(parser.fpath+'/results_dsk')
            else:
                print("\n results_dsk folder for the collection of datasets already exists:")
                print(parser.fpath + '/results_dsk')
        except OSError:
            print("\n  Failed to create the results_dsk folder for the datasets")

        try:
            if not os.path.exists(self.path_o):
                os.mkdir(self.path_o)
                print("\n  Output path for deskewed tiffs created:")
                print("    "+self.path_o)
            else:
                print("\n  Output path for deskewed tiffs already exists:")
                print("    "+self.path_o)
            # save the parser
            with open("{}/MyParser_{}.parser".format(self.path_o, self.p.fname_head), "wb") as f:
                pickle.dump(self.p, f, pickle.HIGHEST_PROTOCOL)
                print("Successfully saved the parser to directory.")
        except OSError:
            print("\n  Failed to create the output path for deskewed tiffs")

        #  define default definition of background component, can add different options in the future.
        self.bg_opt= 'mean of a tiff stack'
        self.threslist_tstep0 = ['']*self.p.channel_n  # prepare a list of thresholds of tstep=0 for each channel.
        image_name = self.p.dict_tiffs[0]['path of tiff']
        arr = io.imread(image_name)
        print(arr.shape)
        self.s = arr.shape  # stack size
        self.sample_z_shift = self.p.sample_z_shift  # this value comes from the paser
        self.angle = 58.5 * np.pi / 180.0
        self.xy_res = 0.100  # measured pixel size in xy
        self.z_res = self.sample_z_shift * np.cos(self.angle)
        self.x_shift = self.sample_z_shift * np.sin(self.angle)
        self.x_additional = np.int32(np.ceil(np.abs((self.x_shift * self.s[0] / self.xy_res))))
        if len(self.s) == 2:
            self.s = np.array([1,self.s[0],self.s[1]])
            self.nx_mod = self.s[2]
            self.singleslices = True
        else:
            self.singleslices = False
            self.nx_mod=self.s[2] + self.x_additional

        self.mip_TiffWriter_objs = list()
        self.label_MIPs=False

    def deskew_one_tiff(self, tif_dict):
        image_name = tif_dict['path of tiff']
        arr = io.imread(image_name)

        if self.bg_opt is 'mean of a tiff stack':
            thres = np.uint16(np.mean(arr[0, :, :]))
        elif self.bg_opt is 'mean of time step 0':
            thres = self.threslist_tstep0[tif_dict[0]['channel index']]
        else:
            thres = 0

        arr[arr < thres] = 0
        arr[arr >= thres] = arr[arr >= thres] - thres
        arr[arr <= 0] = 0
        arr_mod = np.zeros((self.s[0], self.s[1], self.nx_mod), dtype='uint16')

        print('    Deskewing time step ' + str(tif_dict['time step']) + '/' + str(self.p.tsteps_n-1)
                  + "; channel " + str(tif_dict['channel index']) + '/' + str(self.p.channel_n-1))
        if self.singleslices is False:
            for i in range(arr.shape[0]):
                x_start = np.int32(np.floor(i * self.x_shift / self.xy_res))
                # arr_mod[i, :, x_start:x_start + self.s[2]] = arr[i, :, :]
                arr_mod[i, :, x_start:x_start + self.s[2]] = self.deskew_a_slice(image_name, i)
        else:
            arr_mod = arr

        io.imsave(self.path_o + '/Deskewed_' + image_name.split('/')[-1], arr_mod)

        # write the XY-MIP to the corresponding MIP tiff file.
        if self.singleslices is False:
            mip0 = np.max(arr_mod, axis=0)
            mip0[30:35, 30:110] = np.max(mip0.ravel())
            mip1 = np.max(arr_mod, axis=1)
            mip2 = np.max(arr_mod, axis=2)

            self.mip_TiffWriter_objs[tif_dict['channel index']][0].save(mip0, compress=0)
            self.mip_TiffWriter_objs[tif_dict['channel index']][1].save(mip1, compress=0)
            self.mip_TiffWriter_objs[tif_dict['channel index']][2].save(mip2, compress=0)
        else:
            self.mip_TiffWriter_objs[tif_dict['channel index']][0].save(arr_mod, compress=0)

    def deskew_all_tiffs(self):
        # go through all tiffs, and deskew one after another
        self.threslist_tstep0 = ['']*self.p.channel_n
        if self.bg_opt is 'mean of time step 0':
            for d in self.p.dict_tstep0_tiffs:
                arr = io.imread(d['path of tiff'])
                self.threslist_tstep0[d['channel index']] = np.uint16(np.mean(arr[0, :, :]))

        # prepare TiffFile writers for the maximum intensity projection (MIP) time lapse of each channel
        for chi in np.arange(self.p.channel_n):
            f1 = skimage.external.tifffile.TiffWriter(self.path_o + '/MIP_'+self.p.channel_names[chi]+'_XY.tif')
            f2 = skimage.external.tifffile.TiffWriter(self.path_o + '/MIP_'+self.p.channel_names[chi]+'_XZ.tif')
            f3 = skimage.external.tifffile.TiffWriter(self.path_o + '/MIP_'+self.p.channel_names[chi]+'_YZ.tif')
            self.mip_TiffWriter_objs.append([f1, f2, f3])

        for d in sorted(self.p.dict_tiffs, key=lambda i: (i['channel index'], i['time step'])):
            self.deskew_one_tiff(d)

        # close MIP TiffFile writers
        for f in self.mip_TiffWriter_objs:
            for subf in f:
                subf.close()

        print("    DONE\n")

    def deskew_a_slice(self, stackname, zi):
        #  return the deskewed slice without saving it, to feed into idx_converter.
        #  use it for idx converter
        # read out a slice
        arr = skimage.external.tifffile.imread(stackname, pages=[zi])
        # prepare an empty slice to store the modified slice
        deskewed = np.zeros((self.s[1], self.s[2]), dtype='uint16')
        # find out the x_start
        x_start_real = zi * self.x_shift / self.xy_res
        x_start = np.int32(np.floor(x_start_real))
        dx = x_start_real - x_start
        # print(dx)
        locs1 = np.arange(0, arr.shape[0])
        locs2 = np.arange(0, arr.shape[1])
        # find interpolation coordinates based on the sub-pixel shifts
        locs1new = locs1[1:locs1.size - 1]
        locs2new = locs2[1:locs2.size - 1] - dx

        # define interpolation function
        f = interpolate.interp2d(locs2, locs1, arr, kind='cubic')
        arr_sps = f(locs2new, locs1new)
        # now interpolate the arr to match the grid precisly.
        deskewed[1:self.s[1]-1, 1:self.s[2]-1] = arr_sps
        return deskewed

