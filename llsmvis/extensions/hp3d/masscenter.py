"""
Xiyu Yi @ LLNL, 2021.
"""
from skimage import io
from scipy import ndimage
import copy
from scipy.signal import argrelextrema
import plotly.graph_objects as go
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def find_threshold_saddle_point(k, pvrange=[50,1000], pvbin=5, show_plots=False, search_range=[200,700], debug=False, minbins=5, peripheral_ratio=0.5):
    """
    find the mass center of an 3D volume
    :param k: 3D stack, np.ndarray
    :param pvrange: pixel value range, [minimum, maximum] value. this is the range to calculate the pixel histograms.
    :param pvbin: pixel value bin size
    :param show_plots: option to show the plots.
    :return:
    """
    # first, get histogram of pixel values
    [a, b] = np.histogram(k.ravel(), bins=list(np.arange(pvrange[0], pvrange[1], pvbin)))

    # find the indexes of the search range for local minimua
    pvbins = np.arange(pvrange[0], pvrange[1], pvbin)
    search_range_ind0 = np.where(pvbins > search_range[0])[0][0]
    search_range_ind1 = np.where(pvbins < search_range[1])[0][-1]
    search_range_inds = [search_range_ind0, search_range_ind1]

    # transform the histogram counts into a profile that is shows more distinction between signal background region.
    l = (a + 1) ** 0.1  # transform counts into a profile that highlights the signature feature of the distribution
    # - I just tried out a bunch intuitively and you can think about this as a magic funtion - Xiyu 2021.10.12

    # find local minimum of this profile to be the cut-off value between background and signal.
    tp0 = argrelextrema(l, np.less)
    # find local minimal within the defined search range
    tp1 = tp0[0][np.where(tp0[0] > search_range_inds[0] - 1)]
    tp = tp1[np.where(tp1 < search_range_inds[1] + 1)]

    # increase the bin size until there is only one local minimum
    while len(tp) > 1:
        pvbin += 5
        if debug:
            print('too many local minimum, increasing bin size to ' + str(pvbin))

        pvbins = np.arange(pvrange[0], pvrange[1], pvbin)  # update the bins with the updated pvbin value.
        search_range_ind0 = np.where(pvbins > search_range[0])[0][0]
        search_range_ind1 = np.where(pvbins < search_range[1])[0][-1]
        search_range_inds = [search_range_ind0, search_range_ind1]
        [a, b] = np.histogram(k.ravel(), bins=list(pvbins))  # udpate the histogram
        l = (a + 1) ** 0.01  # transform counts into a profile that highlights the signature feature of the distribution
        # - I just tried out a bunch intuitively and you can think about this as a magic funtion - Xiyu 2021.10.12
        # find local minimal in the full range
        tp0 = argrelextrema(l, np.less)
        # find local minimal within the defined search range
        tp1 = tp0[0][np.where(tp0[0] >= search_range_inds[0])]  # crop out the ones that are too small
        tp = tp1[np.where(tp1 <= search_range_inds[1])]  # crop out the ones that are too large
        if debug:
            print('len tp is' + str(len(tp)))
            print(tp)
        if len(tp)==0:
            tp = [(np.int(np.mean(np.asarray(tppre))))]
            a = copy.deepcopy(apre)
            b = copy.deepcopy(bpre)

        # store the current a, b, tp values for next round.
        apre = copy.deepcopy(a)
        bpre = copy.deepcopy(b)
        tppre = copy.deepcopy(tp)


    # get the index of the local minimum.
    peaks = tp
    threshold = b[peaks]  # this will be the voxel value of the local minimum
    threshold_ind = peaks  # this is the index of the voxel value
    bin_centers = (b[1:] + b[:-1]) / 2  # this are the centers of the bin
    phist_counts = a  # histogram counts

    # now find the upper_bound - the first bin that has counts lower than minbins, and after the threshold bin.
    upper_bound_inds = np.where(phist_counts < minbins)[0]
    if debug:
        print('low count inds:')
        print(upper_bound_inds)

    upper_bound_inds = upper_bound_inds[np.where(upper_bound_inds > threshold_ind)]
    upper_bound_ind = upper_bound_inds[0]
    upper_bound = b[upper_bound_ind]

    # find cell peripheral lower bound and its index.
    # this is the cell body
    k1 = copy.deepcopy(k)
    k1[np.where(k1 < threshold)] = 0
    k1[np.where(k1 > upper_bound)] = 0
    vbody = len(np.where(k1 > 0)[0])

    # now based on the cell body, identify the peripheral region
    k2 = copy.deepcopy(k)
    k2[np.where(k2 > upper_bound)] = 0
    sorted_voxels = np.sort(k2.ravel())
    cell_peripheral_lb = sorted_voxels[-np.int(vbody * (1 + peripheral_ratio))]


    if show_plots:
        plt.figure(figsize=(3, 3))
        plt.plot((b[1:] + b[:-1]) / 2, (a + 1) ** 0.1)
        plt.plot(b[peaks], (a[peaks] + 1) ** 0.1, 'o')
        plt.plot([b[search_range_inds[0]], b[search_range_inds[1]]], [(a[search_range_inds[0]] + 1) ** 0.1] * 2, '-*')
        plt.plot(b[upper_bound_ind], (a[upper_bound_ind] + 1) ** 0.1, 'o')
        if debug:
            print('threshold is ' + str(b[peaks]))

    return [threshold, threshold_ind, bin_centers, phist_counts, upper_bound, upper_bound_ind, cell_peripheral_lb]


def findmcenter(k, thres, thresmax=800, thresmin=100, thres_perilb=100, display_option=False):
    s=copy.deepcopy(k)
    s[np.where(s<thres)]=0
    s[np.where(s>thresmax)]=thresmax

    # for crmips, crust mips. peripheral crust lb to saddle point.
    cr=copy.deepcopy(k)
    cr[np.where(cr<thres_perilb)]=thres_perilb
    cr[np.where(s>thres)]=thres_perilb

    # for dmips, lower bound to saddle point.
    d=copy.deepcopy(k)
    d[np.where(d>thres)]=0
    d[np.where(d<thresmin)]=0

    b=copy.deepcopy(k)
    b[np.where(b>thres)]=0

    c=ndimage.measurements.center_of_mass(s)

    # for crmips, mips of pheripheral crust
    crmip_ax0 = np.sum(cr, axis=0)
    crmip_ax1 = np.sum(cr, axis=1)
    crmip_ax2 = np.sum(cr, axis=2)
    crmips = [crmip_ax0, crmip_ax1, crmip_ax2]

    # for kmips, mips before cropping
    kmip_ax0 = np.max(k, axis=0)
    kmip_ax1 = np.max(k, axis=1)
    kmip_ax2 = np.max(k, axis=2)
    kmips = [kmip_ax0, kmip_ax1, kmip_ax2]

    # for smips, saddle point to upper bound
    smip_ax0 = np.max(s, axis=0) # thres is saddle point, thresmax is upper bound; thresmin was set to be the lower bound.
    smip_ax1 = np.max(s, axis=1)
    smip_ax2 = np.max(s, axis=2)
    smips=[smip_ax0, smip_ax1, smip_ax2]

    # for dmips, lower bound to saddle point.
    dmip_ax0 = np.max(d, axis=0)
    dmip_ax1 = np.max(d, axis=1)
    dmip_ax2 = np.max(d, axis=2)
    dmips = [dmip_ax0, dmip_ax1, dmip_ax2]

    # for bmips, zero to saddle point
    bmip_ax0 = np.max(b, axis=0)
    bmip_ax1 = np.max(b, axis=1)
    bmip_ax2 = np.max(b, axis=2)
    bmips = [bmip_ax0, bmip_ax1, bmip_ax2]

    if display_option:
        plt.figure(figsize=(3,3))
        plt.imshow(smip_ax0)
        plt.plot(c[2], c[1], 'bo')
    return [c, smips, kmips, dmips, bmips, crmips]


def plotly_scat_3d(x,y,z):
    # this script is copied over from here: https://plotly.com/python/3d-scatter-plots/ -Xiyu.
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=12,
            color=z,                # set color to an array/list of desired values
            colorscale='Viridis',   # choose a colorscale
            opacity=0.8
        )
    )])

    # tight layout
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()


def plot_mass_centers(x,y,z,t):
    fig = plt.figure(figsize=(10,10))
    ax = fig.gca(projection='3d')
    col = t
    ax.plot(x, y, z, label='mass center positions')
    ax.legend()
    ax.scatter(x,y,z, marker='o', c=col, s=200, cmap='cool')
    plt.show()