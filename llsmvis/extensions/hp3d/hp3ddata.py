"""
Xiyu Yi @ LLNL, 2021.
"""

# this is the hp3d data class for hp3d analysis and storing the results.
import h5py
import os
import time
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from llsmvis.extensions.hp3d import masscenter
from skimage import io
import numpy as np
import copy
import sys


class HP3Ddata:
    def __init__(self, fpath, dfnamehead, initialize=False, verbose=True):
        self.verbose=verbose
        self.fpath = fpath
        self.dfnamehead = dfnamehead
        # first initialize the datafile path
        if verbose:
            print('Try to create the following file path:')
            print(fpath)
        self.mcoop=False  # plot masss center trajectory output option
        self.mcop='./mass_center_trajectory.png'  # plot mass center trajectory output path
        self.vcoop=False  # plot masss center trajectory output option
        self.vcop='./volume_center_trajectory.png'  # plot mass center trajectory output path
        self.roop=False  # plot roughness trajectory output option
        self.rop='./roughness.png'  # plot roughness trajectory output path
        self.insptoop = False  # inspect thresholds output option
        self.insptop = './inspect_thresholds.png'  # inspect thresholds output path
        # check mass center on smip options
        self.mcsmipoop = False # output option
        self.mcsmipop = './check_mascenter_on_smip.png'  # output option
        # inspect rgbas save options
        self.inspect_rgbas_oop = False
        self.inspect_rgbas_op = './inspect_rgbas.png'
        self.inject_signature_points_vcount_profile = False
        self.signatures=[]
        self.signatures_to_inject=[]
        if os.path.isdir(fpath):
            if verbose:
                print('the file path exists')
        else:
            try:
                os.mkdir(fpath)
            except:
                if verbose:
                    print('make' + fpath + 'failed')
                pass

        if initialize is True:
            # Initialize the hdf5 file
            if os.path.isfile(os.path.join(fpath, dfnamehead + '.hdf5')):
                if verbose:
                    print('deleting existing hdf5 file')
                fname = os.path.join(fpath, dfnamehead + '.hdf5')
                print(fname)
                os.remove(fname)
                time.sleep(1)

            try:
                f = h5py.File(os.path.join(fpath, dfnamehead + '.hdf5'), 'w')
                self.h5f = f
            except:
                if verbose:
                    print('creating the file object for h5py file failed, file exists')
                pass

        if initialize is False:
            if os.path.isfile(os.path.join(fpath, dfnamehead + '.hdf5')):
                if verbose:
                    print('found the hdf5 file:')
                fname = os.path.join(fpath, dfnamehead + '.hdf5')
                if verbose:
                    print(fname)

            try:
                f = h5py.File(os.path.join(fpath, dfnamehead + '.hdf5'), 'a')
                self.h5f = f
                if verbose:
                    print('successfully opened the hp3d data object and the associated hdf5 file')
            except:
                if verbose:
                    print('opening the hp3d hdf5 file failed')
                pass

        if initialize is True:
            # create groups for different properties
            self.h5fhist_bc = self.h5f.create_group("[G01] voxel value bin centers")
            self.h5fhist_ct = self.h5f.create_group("[G02] voxel value histogram counts")

            # create groups for stack mip images in 3 different planes without cropping by the thres hold
            self.h5fkmip0 = self.h5f.create_group("[G03] stack XY mips before cropping")
            self.h5fkmip1 = self.h5f.create_group("[G04] stack YZ mips before cropping")
            self.h5fkmip2 = self.h5f.create_group("[G05] stack XZ mips before cropping")

            # create groups for stack mip images in 3 different planes with cropping by the thres hold
            self.h5fsmip0 = self.h5f.create_group("[G06] stack XY mips after cropping - saddle point to upper bound")
            self.h5fsmip1 = self.h5f.create_group("[G07] stack YZ mips after cropping - saddle point to upper bound")
            self.h5fsmip2 = self.h5f.create_group("[G08] stack XZ mips after cropping - saddle point to upper bound")

            # create groups for stack mip images in 3 different planes with cropping by the thres hold
            self.h5fdmip0 = self.h5f.create_group("[G09] stack XY mips after cropping - lower bound to saddle point")
            self.h5fdmip1 = self.h5f.create_group("[G10] stack YZ mips after cropping - lower bound to saddle point")
            self.h5fdmip2 = self.h5f.create_group("[G11] stack XZ mips after cropping - lower bound to saddle point")

            # create groups for stack mip images in 3 different planes with cropping by the thres hold
            self.h5fbmip0 = self.h5f.create_group("[G12] stack XY mips after cropping - zero to saddle point")
            self.h5fbmip1 = self.h5f.create_group("[G13] stack YZ mips after cropping - zero to saddle point")
            self.h5fbmip2 = self.h5f.create_group("[G14] stack XZ mips after cropping - zero to saddle point")

            # create groups for stack mip images in 3 different planes with cropping for the peripheral crust
            self.h5fcrmip0 = self.h5f.create_group("[G15] stack XY mips after cropping - peripheral lb to saddle point")
            self.h5fcrmip1 = self.h5f.create_group("[G16] stack YZ mips after cropping - peripheral lb to saddle point")
            self.h5fcrmip2 = self.h5f.create_group("[G17] stack XZ mips after cropping - peripheral lb to saddle point")

        return

    def process_all_time_points(self,
                                tlist,
                                pvbin=5,
                                pvrange=(50, 1500),
                                show_plots_saddle_point=False,
                                search_range=(150, 650),
                                debug=False,
                                minbins=5,
                                display_option_find_mcenter=False,
                                peripheral_ratio=1):
        # loop over all time point
        list_bc = []
        list_counts = []
        list_c = []

        # crmips, mips before cropping
        list_crmip0 = []
        list_crmip1 = []
        list_crmip2 = []

        # kmips, mips before cropping
        list_kmip0 = []
        list_kmip1 = []
        list_kmip2 = []

        # bmips, zero to saddle point
        list_bmip0 = []
        list_bmip1 = []
        list_bmip2 = []

        # smips, saddle point to upper bound
        list_smip0 = []
        list_smip1 = []
        list_smip2 = []

        # dmips, lower bound to saddle point.
        list_dmip0 = []
        list_dmip1 = []
        list_dmip2 = []

        list_thres = []
        list_thres_ub = []
        list_thres_ubind = []
        list_thres_lb = []
        list_thres_lbind = []
        list_thres_ind = []
        list_thres_cperilb = []
        if len(self.signatures) == 0:
            self.signatures = [np.nan] * 50

        for tindex, t in enumerate(tlist):
            print(t)
            # load in the time point
            k = io.imread(t)
            if self.inject_signature_points_vcount_profile is False:
                # find the intensity threshold
                [threshold, tind, bc, counts, upper_bound, upper_bound_ind, cell_peripheral_lb] = \
                    masscenter.find_threshold_saddle_point(k,
                                                           pvbin=pvbin,
                                                           pvrange=pvrange,
                                                           show_plots=show_plots_saddle_point,
                                                           search_range=search_range,
                                                           debug=debug,
                                                           minbins=minbins,
                                                           peripheral_ratio=peripheral_ratio)

                self.signatures[tindex]=[threshold, tind, bc, counts, upper_bound, upper_bound_ind, cell_peripheral_lb]

            if self.inject_signature_points_vcount_profile is True:
                print('injecting signature points for time point '+str(tindex))
                [threshold, tind, bc, counts, upper_bound, upper_bound_ind, cell_peripheral_lb]= \
                    self.signatures_to_inject[tindex]

            print('l0 - thres is' +str(threshold))
            list_thres.append(copy.deepcopy(threshold))
            list_thres_ind.append(copy.deepcopy(tind))
            list_thres_ub.append(upper_bound)
            list_thres_ubind.append(upper_bound_ind)
            lbind = np.where(counts == np.max(counts))[0][0]  # lower bound index appear at the highest peak in the
            # voxel value counts.
            list_thres_lbind.append(lbind)
            list_thres_lb.append(bc[lbind])
            list_thres_cperilb.append(cell_peripheral_lb)

            # find the mass center
            [c, smips, kmips, dmips, bmips, crmips] = masscenter.findmcenter(k,
                                                                     thres=threshold,
                                                                     thresmax=upper_bound,
                                                                     thresmin=bc[lbind],
                                                                     thres_perilb=cell_peripheral_lb,
                                                                     display_option=display_option_find_mcenter)
            list_bc.append(bc)
            list_counts.append(counts)
            list_c.append(c)
            list_smip0.append(smips[0])
            list_smip1.append(smips[1])
            list_smip2.append(smips[2])

            list_crmip0.append(crmips[0])
            list_crmip1.append(crmips[1])
            list_crmip2.append(crmips[2])

            list_kmip0.append(kmips[0])
            list_kmip1.append(kmips[1])
            list_kmip2.append(kmips[2])

            list_dmip0.append(dmips[0])
            list_dmip1.append(dmips[1])
            list_dmip2.append(dmips[2])

            list_bmip0.append(bmips[0])
            list_bmip1.append(bmips[1])
            list_bmip2.append(bmips[2])

        self.h5f.create_dataset("[D1] mass centers", data=list_c, dtype='float')
        self.h5f.create_dataset("[D2] threshold saddle point", data=list_thres, dtype='float')
        self.h5f.create_dataset("[D3] threshold saddle point index", data=list_thres_ind, dtype='float')
        self.h5f.create_dataset("[D4] threshold upper bound", data=list_thres_ub, dtype='float')
        self.h5f.create_dataset("[D5] threshold upper bound index", data=list_thres_ubind, dtype='float')
        self.h5f.create_dataset("[D6] threshold lower bound", data=list_thres_lb, dtype='float')
        self.h5f.create_dataset("[D7] threshold lower bound index", data=list_thres_lbind, dtype='float')
        self.h5f.create_dataset("[D8] threshold cell peripheral lower bound", data=list_thres_cperilb, dtype='float')

        for i, bc in enumerate(list_bc):
            self.h5fhist_bc.create_dataset('T' + str(i), data=bc, dtype='float')

        for i, c in enumerate(list_counts):
            self.h5fhist_ct.create_dataset('T' + str(i), data=c, dtype='float')

        # append smips
        for i, smip0 in enumerate(list_smip0):
            self.h5fsmip0.create_dataset('T' + str(i), data=smip0, dtype='float')

        for i, smip1 in enumerate(list_smip1):
            self.h5fsmip1.create_dataset('T' + str(i), data=smip1, dtype='float')

        for i, smip2 in enumerate(list_smip2):
            self.h5fsmip2.create_dataset('T' + str(i), data=smip2, dtype='float')

        # append crmips
        for i, crmip0 in enumerate(list_crmip0):
            self.h5fcrmip0.create_dataset('T' + str(i), data=crmip0, dtype='float')

        for i, crmip1 in enumerate(list_crmip1):
            self.h5fcrmip1.create_dataset('T' + str(i), data=crmip1, dtype='float')

        for i, crmip2 in enumerate(list_crmip2):
            self.h5fcrmip2.create_dataset('T' + str(i), data=crmip2, dtype='float')

        # append kmips
        for i, kmip0 in enumerate(list_kmip0):
            self.h5fkmip0.create_dataset('T' + str(i), data=kmip0, dtype='float')

        for i, kmip1 in enumerate(list_kmip1):
            self.h5fkmip1.create_dataset('T' + str(i), data=kmip1, dtype='float')

        for i, kmip2 in enumerate(list_kmip2):
            self.h5fkmip2.create_dataset('T' + str(i), data=kmip2, dtype='float')

        # append dmips, lower bound to saddle point.
        for i, dmip0 in enumerate(list_dmip0):
            self.h5fdmip0.create_dataset('T' + str(i), data=dmip0, dtype='float')

        for i, dmip1 in enumerate(list_dmip1):
            self.h5fdmip1.create_dataset('T' + str(i), data=dmip1, dtype='float')

        for i, dmip2 in enumerate(list_dmip2):
            self.h5fdmip2.create_dataset('T' + str(i), data=dmip2, dtype='float')

        # append bmips
        for i, bmip0 in enumerate(list_bmip0):
            self.h5fbmip0.create_dataset('T' + str(i), data=bmip0, dtype='float')

        for i, bmip1 in enumerate(list_bmip1):
            self.h5fbmip1.create_dataset('T' + str(i), data=bmip1, dtype='float')

        for i, bmip2 in enumerate(list_bmip2):
            self.h5fbmip2.create_dataset('T' + str(i), data=bmip2, dtype='float')

        return

    def show_data_structure(self):
        for name in self.h5f:
            print(name)
        return 0

    def plot_mass_center_trajectory(self):
        plot_mass_center_trajectory(hp3ddata_h=self, ttstr=self.dfnamehead, oop=self.mcoop, op=self.mcop)
        return 0

    def plot_volume_center_trajectory(self):
        plot_volume_center_trajectory(hp3ddata_h=self, ttstr=self.dfnamehead, oop=self.vcoop, op=self.vcop)
        return 0

    def plot_roughness_trajectory(self):
        plt_rv_rs_ratio(hp3ddata_h=self, ttstr=self.dfnamehead, oop=self.roop, op=self.rop)
        return 0

    def inspect_threshold(self):
        inspect_threshold(hp3ddata_h=self, oop=self.insptoop, op=self.insptop)
        return 0

    def check_mass_center_on_smip(self, projp='XY'):
        check_mass_center_on_smip(hp3ddata_h=self, projp=projp,oop=self.mcsmipoop, op=self.mcsmipop[:-4]+"_"+projp+'.png')
        return 0

    def inspect_rgbas(self, groupkey, cmap, show_50t_tiles=False):
        [rgbas, mip_rgbas, tiles_50t] = inspect_rgbas(hp3ddata_h=self, groupkey=groupkey, cmap=cmap,
                                                      show_50T_tiles=show_50t_tiles,
                                                      oop=self.inspect_rgbas_oop,
                                                      op=self.inspect_rgbas_op)
        return [rgbas, mip_rgbas, tiles_50t]

    def add_volume_centers_to_hdf5(self, tlist):
        # calculate the volume centers
        vcenters = []
        for ind, t in enumerate(tlist):
            sys.stdout.write('\r')
            sys.stdout.write('update volume centers, stack ' + str(ind) + '... ')
            sys.stdout.flush()
            k = io.imread(t)
            thres = self.h5f['[D2] threshold saddle point'][ind][0]
            vc = masscenter.findvcenter(k, thres)
            vcenters.append(vc)

        # add the name to the hdf5 file
        try:
            del self.h5f['[D9] volume centers']
        except:
            pass
        self.h5f.create_dataset("[D9] volume centers", data=vcenters, dtype='float')
        return vcenters


def check_histogram_thresholding(hp3ddata_h, Tind, zoffset, show_bounds=True):
    f = hp3ddata_h
    bin_centers = np.asarray(f.h5f["[G01] voxel value bin centers/T" + str(Tind)])
    counts = np.asarray(f.h5f["[G02] voxel value histogram counts/T" + str(Tind)])
    thres_sp = np.asarray(f.h5f["[D2] threshold saddle point"])[Tind]
    thres_spi = np.int(np.asarray(f.h5f["[D3] threshold saddle point index"])[Tind])
    thres_ub = np.asarray(f.h5f["[D4] threshold upper bound"])[Tind]
    thres_ubi = np.int(np.asarray(f.h5f["[D5] threshold upper bound index"])[Tind])
    thres_lb = np.asarray(f.h5f["[D6] threshold lower bound"])[Tind]
    thres_lbi = np.int(np.asarray(f.h5f["[D7] threshold lower bound index"])[Tind])
    plt.plot(bin_centers, (counts + 1) ** 0.1 + zoffset)
    if show_bounds:
        plt.plot(thres_lb, (counts[thres_lbi] + 1) ** 0.1 + zoffset, 'ro')
        plt.plot(thres_sp, (counts[thres_spi] + 1) ** 0.1 + zoffset, 'bo')
        plt.plot(thres_ub, (counts[thres_ubi] + 1) ** 0.1 + zoffset, 'go')


def plot_mass_center_trajectory(hp3ddata_h, ttstr, oop=False, op='./mass_center_traj.png'):
    list_c = list(hp3ddata_h.h5f["[D1] mass centers"])
    x = []
    y = []
    z = []
    tt = np.arange(0, len(list_c))
    for c in list_c:
        x.append(c[0])
        y.append(c[1])
        z.append(c[2])
    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca(projection='3d')
    col = tt
    ax.plot(x, y, z, 'k')
    ax.scatter(x, y, z, marker='o', c=col, s=150, cmap='cool', edgecolors='k', alpha=0.8)
    plt.title('Mass center trajectory - ' + ttstr, fontsize=20)
    if oop is True:
        plt.savefig(op,transparent=True)
    plt.show()


def plot_volume_center_trajectory(hp3ddata_h, ttstr, oop=False, op='./volume_center_traj.png'):
    list_c = list(hp3ddata_h.h5f["[D9] volume centers"])
    x = []
    y = []
    z = []
    tt = np.arange(0, len(list_c))
    for c in list_c:
        x.append(c[0])
        y.append(c[1])
        z.append(c[2])
    fig = plt.figure(figsize=(8, 8))
    ax = fig.gca(projection='3d')
    col = tt
    ax.plot(x, y, z, 'k')
    ax.scatter(x, y, z, marker='o', c=col, s=150, cmap='cool', edgecolors='k', alpha=0.8)
    plt.title('Volume center trajectory - ' + ttstr, fontsize=20)
    if oop is True:
        plt.savefig(op,transparent=True)
    plt.show()


def plt_rv_rs_ratio(hp3ddata_h, ttstr='test', oop=False, op='./roughness.png'):
    rv=np.asarray(hp3ddata_h.h5f['[D12] sphere radius with equi volume'])
    rs=np.asarray(hp3ddata_h.h5f['[D13] sphere radius with equi surface area'])
    tt = np.arange(0, len(rv))
    plt.figure(figsize=(8, 8))
    col = tt
    plt.plot(np.arange(0,len(rv)), rv/rs, 'k')
    plt.scatter(np.arange(0,len(rv)), rv/rs, marker='o', c=col, s=50, cmap='cool', edgecolors='w', alpha=1)
    plt.title('Surface roughness (Rv/Rs) - ' + ttstr, fontsize=20)
    plt.xlim(0, len(rv))
    plt.ylim(0, 1)
    if oop is True:
        plt.savefig(op, transparent=True)
    plt.show()


def check_mass_center_on_smip(hp3ddata_h, projp='XY', oop=False, op='./check_mass_center_test.png'):
    # first, determin the group name for this smip
    if projp is 'XY':
        groupkey = "[G06] stack XY mips after cropping - saddle point to upper bound"

    if projp is 'YZ':
        groupkey = "[G07] stack YZ mips after cropping - saddle point to upper bound"

    if projp is 'XZ':
        groupkey = "[G08] stack XZ mips after cropping - saddle point to upper bound"

    # find out total time point for the dataset at current
    TimeN = len(list(hp3ddata_h.h5f["[G02] voxel value histogram counts"].__iter__()))

    s1 = list(hp3ddata_h.h5f[groupkey + "/T0"].shape)
    s1 = np.asarray(s1, dtype='float32') / np.max(s1) * 5
    tag = 0
    plt.figure(figsize=(s1[1] * 2, s1[0]))

    # findout colume n
    column_n = np.int(TimeN / 5)
    for timei in np.arange(TimeN):
        tag += 1
        smip0 = np.asarray(hp3ddata_h.h5f[groupkey + "/T" + str(timei)])
        c = hp3ddata_h.h5f["[D1] mass centers"][timei]
        ax1 = plt.subplot(5, column_n, tag)
        if timei == 0:
            smip0[20:40, 10:90] = np.max(smip0)
        fig = plt.imshow(smip0)
        if projp is "XY":
            plt.plot(c[2], c[1], 'ro', markersize=4)
        if projp is "XZ":
            plt.plot(c[1], c[0], 'ro', markersize=4)
        if projp is "YZ":
            plt.plot(c[2], c[0], 'ro', markersize=4)

        plt.axis('off')
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        ax1.set_xticklabels([])
        ax1.set_yticklabels([])
        plt.subplots_adjust(wspace=0.1, hspace=0.1)
    if oop is True:
        plt.savefig(op, transparent=True)
    plt.show()
    print('scale bars are 8 um')


def inspect_threshold(hp3ddata_h, oop=False, op='./inspect_threasholds.png'):
    # find out total time point for the dataset at current
    TimeN = len(list(hp3ddata_h.h5f["[G02] voxel value histogram counts"].__iter__()))

    plt.figure(figsize=(15, 5))
    ax = plt.subplot(1, 3, 1)
    for i in np.arange(TimeN):
        check_histogram_thresholding(hp3ddata_h=hp3ddata_h, Tind=i, zoffset=-0.5 * i, show_bounds=False)
    # plt.axis('off')
    ax.set_yticklabels([])
    ax = plt.subplot(1, 3, 2)
    for i in np.arange(TimeN):
        check_histogram_thresholding(hp3ddata_h=hp3ddata_h, Tind=i, zoffset=-0.5 * i, show_bounds=True)
    # plt.axis('off')
    ax.set_yticklabels([])
    ax = plt.subplot(1, 3, 3)
    for i in np.arange(1):
        check_histogram_thresholding(hp3ddata_h=hp3ddata_h, Tind=i, zoffset=-0.5 * i, show_bounds=True)
        #     ax.set_xticklabels([])
        ax.set_yticklabels([])
        plt.legend(['transformed counts', 'Lower bound', 'Saddle point', 'Upper bound'],
                   bbox_to_anchor=(0.3, 1), loc="upper left")
    if oop is True:
        plt.savefig(op,transparent=True)
    plt.show()


def get_rgba_one_stack(hp3ddata_h, groupkey, timetag, cmap, total_time_N):
    # get rgba of a single stack
    # first, get the stack c based on the miptag
    k = cmap(np.linspace(0, 1, total_time_N))
    c = np.asarray(hp3ddata_h.h5f[groupkey + "/T" + str(timetag)])
    cnonzero = c[np.where(c > 0)].ravel()
    lb = np.min(cnonzero.ravel())
    ub = np.max(cnonzero.ravel())
    c[np.where(c < lb)] = lb
    c[np.where(c > ub)] = ub
    c = (c - lb) / (ub - lb)
    c_r = c * k[timetag][0]
    c_g = c * k[timetag][1]
    c_b = c * k[timetag][2]
    c_a = np.ones(c.shape)
    c_rgba = np.stack([c_r, c_g, c_b, c_a], axis=2)
    c_rgba[np.where(c_rgba > 1)] = 1
    c_rgba[np.where(c_rgba < 0)] = 0
    return c_rgba


def get_rgba_all_stacks(hp3ddata_h, groupkey, cmap):
    total_time_N = \
        len(list(hp3ddata_h.h5f["[G06] stack XY mips after cropping - saddle point to upper bound"].__iter__()))
    rgbas = []
    for tind in np.arange(total_time_N):
        c_rgba = \
            get_rgba_one_stack(hp3ddata_h=hp3ddata_h, groupkey=groupkey, \
                               timetag=tind, cmap=cmap, total_time_N=total_time_N)
        rgbas.append(c_rgba)

    return rgbas


def inspect_rgbas(hp3ddata_h, groupkey, cmap, show_50T_tiles=False, oop=False, op='./inspect_rgbas.png'):
    total_time_N = \
        len(list(hp3ddata_h.h5f["[G06] stack XY mips after cropping - saddle point to upper bound"].__iter__()))
    rgbas = get_rgba_all_stacks(hp3ddata_h=hp3ddata_h, groupkey=groupkey, cmap=cmap)
    s1 = rgbas[0].shape
    s1 = s1 / np.max(s1) * 10
    tag = 0
    if show_50T_tiles is False:
        plt.figure(figsize=(s1[1] * 2, s1[0]))
        column_n = np.int(total_time_N / 5)
        for timei in np.arange(total_time_N):
            tag += 1
            ax1 = plt.subplot(5, column_n, tag)
            if timei == 0:
                im2show = copy.deepcopy(rgbas[timei])
                im2show[20:40, 10:90, :] = np.max(im2show)
            else:
                im2show = rgbas[timei]
            fig = plt.imshow(im2show)
            plt.axis('off')
            fig.axes.get_xaxis().set_visible(False)
            fig.axes.get_yaxis().set_visible(False)
            ax1.set_xticklabels([])
            ax1.set_yticklabels([])
            plt.subplots_adjust(wspace=0, hspace=0)
        if oop is True:
            plt.savefig(op, transparent=True)
        plt.show()

    tiles_50T = []
    if show_50T_tiles is True:
        plt.figure(figsize=(12, 12))
        r1 = np.concatenate(rgbas[0:10], axis=1)
        r2 = np.concatenate(rgbas[10:20], axis=1)
        r3 = np.concatenate(rgbas[20:30], axis=1)
        r4 = np.concatenate(rgbas[30:40], axis=1)
        r5 = np.concatenate(rgbas[40:50], axis=1)
        im2show = np.concatenate([r1, r2, r3, r4, r5], axis=0)
        im2show[20:40, 10:90, :] = np.max(im2show)
        fig = plt.imshow(im2show)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        tiles_50T = im2show
        if oop is True:
            plt.savefig(op, transparent=True)

    mip_rgbas = np.max(np.asarray(rgbas), axis=0)
    plt.figure(figsize=(5, 5))
    im2show = copy.deepcopy(mip_rgbas)
    im2show[10:15, 10:90, :] = np.max(im2show)
    fig = plt.imshow(im2show)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    if oop is True:
        plt.savefig(op[:-4]+"_overlay.png", transparent=True)

    print("scale bars are 8 um")
    return [rgbas, mip_rgbas, tiles_50T]

