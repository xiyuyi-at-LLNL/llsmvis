"""
Xiyu Yi @ LLNL, 2021.
"""
from matplotlib import pyplot as plt
from skimage import io
from scipy import ndimage
import numpy as np
import copy
from scipy.signal import argrelextrema

def find_threshold_saddle_point(k, pvrange=[50,1000], pvbin=5, show_plots=False):
    """
    find the mass center of an 3D volume
    :param k: 3D stack, np.ndarray
    :param pvrange: pixel value range, [minimum, maximum] value. this is the range to calculate the pixel histograms.
    :param pvbin: pixel value bin size
    :param show_plots: option to show the plots.
    :return:
    """
    # first, get histogram of pixel values
    [a, b]=np.histogram(k.ravel(), bins=list(np.arange(pvrange[0],pvrange[1],pvbin)))

    # transform the histogram counts into a profile that is shows more distinction between signal background region.
    l=(a+1)**0.1

    # find local minimum of this profile to be the cut-off value between background and signal.
    tp =argrelextrema(l, np.less)

    # increase the bin size until there is only one local minimum
    while len(tp[0])>1:
        pvbin += 5
        print('too many local minimum, increasing bin size to '+str(pvbin))
        [a,b]=np.histogram(k.ravel(), bins=list(np.arange(pvrange[0],pvrange[1],pvbin)));
        l=(a+1)**0.01
        tp = argrelextrema(l, np.less)

    # get the index of the local minimum.
    peaks = tp[0]
    threshold=b[peaks]  # this will be the voxel value of the local minimum
    threshold_ind=peaks  # this is the index of the voxel value
    bin_centers=(b[1:]+b[:-1])/2  # this are the centers of the bin
    phist_counts=a  # histogram counts
    if show_plots:
        plt.plot((b[1:]+b[:-1])/2,(a+1)**0.1)
        plt.plot(b[peaks],(a[peaks]+1)**0.1,'o')
        print('threshold is '+str(b[peaks]))
    return [threshold, threshold_ind,bin_centers,phist_counts]
