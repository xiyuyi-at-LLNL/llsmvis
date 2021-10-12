"""
Xiyu Yi @ LLNL, 2021.
"""
from matplotlib import pyplot as plt
from skimage import io
from scipy import ndimage
import numpy as np
import copy
from scipy.signal import argrelextrema

def find_threshold_saddle_point(k, pvrange=[50,1000], pvbin=5, show_plots=False, search_range=[200,700], debug=False):
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
    if show_plots:
        plt.figure(figsize=(3, 3))
        plt.plot((b[1:] + b[:-1]) / 2, (a + 1) ** 0.1)
        plt.plot(b[peaks], (a[peaks] + 1) ** 0.1, 'o')
        plt.plot([b[search_range_inds[0]], b[search_range_inds[1]]], [(a[search_range_inds[0]] + 1) ** 0.1] * 2, '-*')
        if debug:
            print('threshold is ' + str(b[peaks]))
    return [threshold, threshold_ind, bin_centers, phist_counts]


def findmcenter(k, thres, display_option=False):
    s=copy.deepcopy(k)
    s[np.where(s<thres)]=0
    c=ndimage.measurements.center_of_mass(s)
    smip = np.max(s, axis=0)
    kmip_ax0 = np.max(k, axis=0)
    kmip_ax1 = np.max(k, axis=1)
    kmip_ax2 = np.max(k, axis=2)
    if display_option:
        plt.figure(figsize=(3,3))
        plt.imshow(smip)
        plt.plot(c[2], c[1], 'bo')
    return [c, smip, kmip_ax0, kmip_ax1, kmip_ax2]