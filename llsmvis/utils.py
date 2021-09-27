import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import six
from datetime import datetime, timedelta
import skvideo.io
from skimage import io
import numpy as np
import os
import skimage.external.tifffile
import sys
sys.path.append("/g/g92/yi10") # add more paths below when needed
from llsmvis import *
from llsmvis import utils
import skvideo.io
import warnings; warnings.simplefilter('ignore')


#import pandas as pd

def render_mpl_table(p, data, col_width=3.0, row_height=0.625, font_size=16,
                     header_color='#2b4360', row_colors=['#ecf0f5', '#c8d4e2'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])

    fig.savefig(p.fpath+'/results_dsk/'+p.fname_head + '_deskewed/MyRep_data_specifics.png')
    return [fig, ax]


def wpad2square(imraw):
    # pad the imraw images (1 channel) into squares
    m = np.max(imraw.shape)
    impad = np.ones((m, m)) * np.max(imraw.ravel())
    impad[0:imraw.shape[0], 0:imraw.shape[1]] = imraw
    return impad


def frameXYmip(im, imname, reldT, absdT, savepath, lower=0, upper=1, data_info='None'):
    # this function is to generate a single frame of the labeled MIP movie in the XY plane.

    fig = plt.figure(figsize=(15, 15), dpi=80)
    ax = plt.imshow(im, cmap=cm.Greys_r, vmin=lower, vmax=upper)
    pos1_f = 1 + 0.05 * np.max(im.shape) / im.shape[0]
    pos2_f = 1 + 0.1 * np.max(im.shape) / im.shape[0]
    pos3_f = 1 + 0.15 * np.max(im.shape) / im.shape[0]

    plt.text(im.shape[1] * 0.01, im.shape[0] * pos1_f, reldT + '(hh:mm:ss.ss)         scale bar: 8um', fontsize=24, color='k')
    plt.text(im.shape[1] * 0.01, im.shape[0] * pos2_f, absdT, fontsize=24, color='k')
    plt.text(im.shape[1] * 0.01, im.shape[0] * pos3_f, data_info, fontsize=24, color='k')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.spines['right'].set_visible(False)
    ax.axes.spines['top'].set_visible(False)
    ax.axes.spines['bottom'].set_visible(False)
    ax.axes.spines['left'].set_visible(False)
    fig.savefig(savepath+'/'+imname )
    plt.close()
    return None


def getLabeledXYmip_MP4(p, lb, ub, reference_frame_index = 0, channel_inds=None):
    # p is the parser
    # this function can only be used after deskew is finished and all the mip stacks are available.
    # take out the initial date time
    t0=datetime.strptime(p.acquisition_startT,'%m/%d/%Y %I:%M:%S %p')
    # loop over all t steps for all channels
    if channel_inds is None:
        channel_inds=np.arange(0,len(p.channel_names))

    for cind in channel_inds:
        c=p.channel_names[cind]
        # find the correct file name for the MIP project in XY of this channel.
        fname=p.fpath+'/results_dsk/'+p.fname_head + '_deskewed'+'/MIP_'+c+'_XY.tif'
        vidp=p.fpath+'/results_dsk/'+p.fname_head + '_deskewed'
        info=p.fname_head + '    channel: '+c
        writer = skvideo.io.FFmpegWriter(vidp+'/MyRep_MIP_'+c+'_wLabels.mp4',outputdict={"-pix_fmt":"yuv420p"})
        print(fname)
        try:
            imstack=skimage.external.tifffile.imread(fname).astype('float')
        except IOError:
            print('failed to open file: \n'+fname)
        peak=np.max(imstack[reference_frame_index,:,:].ravel());
        base=np.min(imstack[reference_frame_index,:,:].ravel());
        imstack=(imstack-base)/(peak-base)
        print('maximum is:' +str(np.max(imstack.ravel())))
        #imstack=(imstack*256).astype('uint8')
        # create a temp folder to hold all .png files as movie frames.
        f=p.fpath+'/results_dsk/'+p.fname_head + '_deskewed'+'/mp4s_'+c
        try:
            os.mkdir(f)
        except:
            pass
        print(imstack.shape)
        if len(imstack.shape)==2:
            stackN=1
        else:
            stackN=imstack.shape[0]
        for i in np.arange(0, stackN):  # loop over all tsteps
            # prepare the correct parameters
            for t in p.dict_tiffs:
                if t['channel index'] == cind:
                    if t['time step'] == i:
                        tc = t
                        dt=tc['time (datetime)']-t0
                        secondsstr='{:05.2f}'.format(np.float(str(dt).split(':')[2]))
                        reldTstr=':'.join(str(dt).split(':')[:2])+':'+secondsstr
                        absdTstr=tc['time (datetime)'].strftime('%m/%d/%Y %I:%M:%S %p')
            # frame this mip image with correct labels, save as png.
            if len(imstack.shape)==2:
                frameXYmip(im=imstack, imname=str(i)+'.png', reldT=reldTstr, absdT=absdTstr, savepath=f, lower=lb, upper=ub, data_info=info)
            else:
                frameXYmip(im=imstack[i,:,:], imname=str(i)+'.png', reldT=reldTstr, absdT=absdTstr, savepath=f, lower=lb, upper=ub, data_info=info)
        # loop over all frames again and export as .mp4
        for i in np.arange(0,stackN): # loop over all tsteps again
            im=skimage.io.imread(f+'/'+str(i)+'.png')
            writer.writeFrame(im)
        writer.close()
    return None


def getLabeledXYmip_MP4_fromGparser(g, lb, ub, reference_frame_index=0, channel_inds=None):
    # p is the group parser
    # this function can only be used after deskew is finished and all the mip stacks are available.
    ptlist = gp.time_sorted_indiv_parsers  # a list of parsers with time order
    # take out the initial date time from the first parser
    t0 = datetime.strptime(ptlist[0].acquisition_startT, '%m/%d/%Y %I:%M:%S %p')

    # loop over all t steps for all channels
    if channel_inds is None:
        channel_inds = np.arange(0, len(ptlist[0].channel_names))

    for cind in channel_inds:  # loop over all the channels
        c = ptlist[0].channel_names[cind]
        # find the correct file name for the MIP project in XY of this channel.
        fname0 = ptlist[0].fpath + '/results_dsk/' + ptlist[0].fname_head + '_deskewed' + '/MIP_' + c + '_XY.tif'

        # Create a folder for the mp4 video
        try:
            os.mkdir(ptlist[0].fpath + '/mp4s')
        except:
            pass
        vidp = ptlist[0].fpath + '/mp4s/' + ptlist[0].fname_head + '_deskewed'

        try:
            os.mkdir(vidp)
        except:
            pass

        info = ptlist[0].fname_head + ',    channel: ' + c

        # Initiate an mp4 file.
        writer = skvideo.io.FFmpegWriter(vidp + '/MyRep_MIP_' + c + '_wLabels.mp4', outputdict={"-pix_fmt": "yuv420p"})
        print(fname0)

        # Read in the image of the first time point.
        try:
            imstack = skimage.external.tifffile.imread(fname0).astype('float')
        except IOError:
            print('failed to open file: \n' + fname)

        # Find the peak and the base of the image at the first time point.
        peak = np.max(imstack.ravel());
        base = np.min(imstack.ravel());
        imstack = (imstack - base) / (peak - base)
        print('maximum is:' + str(np.max(imstack.ravel())))

        # Create a temp folder to hold all .png files as movie frames.
        f = vidp + '/mp4s_' + c
        try:
            os.mkdir(f)
        except:
            pass

        # Print the image shape
        print(imstack.shape)
        stackN = len(ptlist)
        for i in np.arange(0, stackN):  # Loop over all tsteps
            # Prepare the correct parameters
            for t in ptlist[i].dict_tiffs:
                if t['channel index'] == cind:
                    tc = t
                    dt = tc['time (datetime)'] - t0
                    secondsstr = '{:05.2f}'.format(np.float(str(dt).split(':')[2]))
                    reldTstr = ':'.join(str(dt).split(':')[:2]) + ':' + secondsstr
                    absdTstr = tc['time (datetime)'].strftime('%m/%d/%Y %I:%M:%S %p')

            # Find the correct file name for the MIP project in XY of this channel.
            fnamei = ptlist[i].fpath + '/results_dsk/' + ptlist[i].fname_head + '_deskewed' + '/MIP_' + c + '_XY.tif'

            # Load this image
            try:
                imstack = skimage.external.tifffile.imread(fnamei).astype('float')
            except IOError:
                print('failed to open file: \n' + fname)

            # Find the peak and the base of the image at the first time point.
            peak = np.max(imstack.ravel());
            base = np.min(imstack.ravel());
            imstack = (imstack - base) / (peak - base)

            # Frame this mip image with correct labels, save as png.
            frameXYmip(im=imstack, imname=str(i) + '.png', reldT=reldTstr, \
                       absdT=absdTstr, savepath=f, lower=lb, upper=ub, data_info=info)

        # Loop over all frames again and export as .mp4
        for i in np.arange(0, stackN):  # Loop over all tsteps again
            im = skimage.io.imread(f + '/' + str(i) + '.png')
            writer.writeFrame(im)

        writer.close()
    return None


def deskew_a_tiff_stack(fpath, fname_head):
    """

    :param fpath: the path string to the tiff stack
    :param fname_head: the fname_head of the tiff stack
    :return: none. The deskewd tiff will be stored at the designated results folder.
    """
    # get a parser:
    p = LLSMParser(fpath, fname_head)
    # define the deskewer
    d = Deskewer(p)
    # deskew all the tiffs
    d.deskew_all_tiffs()
    [fig, ax] = utils.render_mpl_table(p, p.data_properties, header_columns=0, col_width=7.0)


def datetime_to_integer(t):
    return np.int(1e10*t.year + 1e8*t.month + t.day + 1e6*t.hour + 1e4*t.minute + 1e2*t.second)

