"""
Xiyu Yi @ LLNL, 2021.
"""
import skimage
import os
import numpy as np
import copy
from skimage import io
import pickle
from scipy import signal


def get_locs(tpath, thead, mipstr):
    with open(os.path.join(tpath, thead) + '_' + mipstr + '.txt') as f:
        lines = f.readlines()
    locs_xy = []
    for l in lines[1:]:
        x = np.int(l.split(',')[0])
        y = np.int(l.split(',')[1].split('\n')[0])
        locs_xy.append(copy.deepcopy([x, y]))

    return locs_xy


def get_fpath(tpath, thead):
    with open(os.path.join(tpath, thead) + '_fpath.txt') as f:
        fp = f.readlines()
    return fp[0].split(' ')[1]


def get_parser(tpath, thead):
    fpath = get_fpath(tpath, thead)  # get the file path that is stored in the cropping output files.
    pname = [i for i in os.listdir(fpath) if i.endswith('.parser')][0]  # get the file name of the parser.
    with open(os.path.join(fpath, pname), 'rb') as f:
        p = pickle.load(f)
    return p


def get_deskewed_tiff_list(tpath, thead):
    tlist = []
    fpath = get_fpath(tpath, thead)  # get the file path that is stored in the cropping output files.
    p = get_parser(tpath, thead)
    for d in p.dict_tiffs:
        t = 'Deskewed_' + d['path of tiff'].split('/')[-1]
        tlist.append(os.path.join(fpath, t))

    time_stamps = []
    for t in np.arange(0, 50):
        time_stamps.append(np.int(tlist[t].split('trimmed_stacks')[1].split('stack')[1][0:4]))
    sorted_tlist = [t for _, t in sorted(zip(time_stamps, tlist))]
    return sorted_tlist


def get_trimmed_tiff_list(tpath, thead):
    tlist = []
    fpath = get_fpath(tpath, thead)  # get the file path that is stored in the cropping output files.
    p = get_parser(tpath, thead)
    for d in p.dict_tiffs:
        t = 'Trimmed_' + d['path of tiff'].split('/')[-1]
        tlist.append(os.path.join(fpath, 'trimmed_stacks', t))
    return tlist


def get_cell_stl_list(hp3dpath, thead):
    cellstlspath=os.path.join(hp3dpath, thead, 'surface_extraction')
    stlpaths = []
    for i in np.arange(50):
        stlfname = [x for x in os.listdir(cellstlspath) if 'stack' + str(i).zfill(4) in x and x.endswith('.stl')]
        stlpaths.append(os.path.join(cellstlspath, stlfname[0]))
    return stlpaths


def get_2d_mask(m, locs):
    for i in locs:
        m[i[1], i[0]] = 1
    m = signal.convolve2d(m, np.ones([20, 20]), boundary='symm', mode='same')
    m[np.where(m > 1)] = 1
    return m


def set_3d_mask_n_trim_stack(stack, locs0, locs1, locs2):
    # input is a single stack
    m0 = np.zeros(stack.shape[1:3])
    m0 = get_2d_mask(m0, locs0)
    m1 = np.zeros(stack.shape[0:3:2])
    m1 = get_2d_mask(m1, locs1)
    m2 = np.zeros(stack.shape[0:2])
    m2 = get_2d_mask(m2, locs2)
    m = np.ones(stack.shape)
    for i in np.arange(m.shape[0]):
        m[i, :, :] = m[i, :, :] * m0
    for i in np.arange(m.shape[1]):
        m[:, i, :] = m[:, i, :] * m1
    for i in np.arange(m.shape[2]):
        m[:, :, i] = m[:, :, i] * m2
    # find the bounds
    inds = np.where(m == 1)
    b = [[np.min(inds[i]), np.max(inds[i])] for i in np.arange(0, 3)]
    # trim the stack
    trimmed_s = stack * m
    trimmed_s = np.uint16(trimmed_s[b[0][0]:b[0][1], b[1][0]:b[1][1], b[2][0]:b[2][1]])
    return [m, b, trimmed_s]


def export_trimmed_stacks_for_all(tpath, thead):
    locs_xy = get_locs(tpath, thead, 'XY')
    locs_xz = get_locs(tpath, thead, 'XZ')
    locs_yz = get_locs(tpath, thead, 'YZ')
    tlist = get_deskewed_tiff_list(tpath, thead)
    fpath = get_fpath(tpath, thead)
    # create a folder to store the trimmed tiff stacks
    trimmed_folder = os.path.join(fpath, 'trimmed_stacks')
    try:
        if not os.path.exists(trimmed_folder):
            os.mkdir(trimmed_folder)
            print("\nCreated folder for trimmed tiff stacks: \n" + trimmed_folder)
        else:
            print("\nFolder for trimmed tiff stacks exists: \n" + trimmed_folder)
    except OSError:
        print("\nFailed to create the folder for trimmed tiff stacks: \n" + trimmed_folder)
    # go through each deskewed stack, and create the trimmed stack
    for t in tlist:
        trimmed_fname = 'Trimmed_' + t.split('/')[-1].split('Deskewed_')[1]
        print('Trimming stack for ' + trimmed_fname)
        stack = io.imread(t)
        [mask, bs, ts] = set_3d_mask_n_trim_stack(stack, locs_xy, locs_xz, locs_yz)
        skimage.external.tifffile.imsave(os.path.join(trimmed_folder, trimmed_fname), ts)
