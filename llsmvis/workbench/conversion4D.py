from os import listdir
from os.path import isfile, join, split
from skimage import io
import sys
from OpenVisus import *
import numpy as np

VERBOSE = True


def ASSERT(cond):
    if not cond: raise Exception("Assert failed")


def MSG(text):
    if VERBOSE:
        print(text)


def add_stack(idx_name, time_step, channel, tiff_file, offset=[0, 0, 0]):
    from skimage import io
    """Add a stack of images given as a tiff image to the 
    given idxfile"""

    # Make sure we are given a valid idx file and we can
    # create an access to it
    dataset = LoadDataset(idx_name)
    access = dataset.createAccess()
    field = dataset.getFieldByName(channel)
    ASSERT(dataset)
    # Now try to open the tiff file. We are using the skimage reader
    # as other implementations did not read the correct stack info
    img = io.imread(tiff_file)
    MSG("Adding %s to idx file %s" % (split(tiff_file)[-1], idx_name))
    # Now make sure that the dimensions match
    global_box = dataset.getLogicBox()
    local_box = np.flip(np.array(img.shape))

    # Remember that the local shape will change by the offset which
    # we expect to be applied in Z -direction
    extended_box = local_box + local_box[2] * offset

    if extended_box[0] != global_box.p2[0] or extended_box[1] != global_box.p2[1] or extended_box[2] != global_box.p2[
        2]:
        print("Dimensions in the idx file ", global_box.p2[0], global_box.p2[1], global_box.p2[2],
              " do not match the local dimensions in the tiff ", local_box)
        raise Exception("ASSERT")

    # Now we go through each slice and add them one by one since
    # we have to take care of the offset
    for Z in range(0, local_box[2]):

        if Z % 10 == 0:
            print("Processing slice %d" % Z)

        data = img[Z, :, :]

        # Now compute the target location
        bottom = PointNi(int(offset[0] * Z), int(offset[1] * Z), Z)
        top = PointNi(int(offset[0] * Z + local_box[0]), int(offset[1] * Z + local_box[1]), Z + 1)
        print(bottom[0], bottom[1], bottom[2], " -- ", top[0], top[1], top[2])

        target_box = BoxNi(bottom, top)
        # Get an internal descriptor for where we want the slice to go
        # target_box=dataset.getBox().getZSlab(Z,Z+1)

        # Create a write ('w') query for this part of the data
        query = BoxQuery(dataset, dataset.getDefaultField(), time_step, ord('w'))
        # We care about our target box
        query.logic_box = target_box
        # And the given field
        query.field = field

        dataset.beginQuery(query)
        if not query.isRunning():
            raise Exception("Begin query failed")

        # Assign the data. Note the shared memory piece
        query.buffer = Array.fromNumPy(data, bShareMem=True)

        # Execute the query to write the data to disk
        ASSERT(dataset.executeQuery(access, query))


def make_idx(tiff_channels, idx_name, offset=[0, 0, 0], timesteps=[0, 1, 1]):
    from skimage import io

    # Read all the channels
    channels = [io.imread(img) for img in tiff_channels]
    dimensions = [np.array(img.shape, dtype=np.int32) for img in channels]

    for i in range(0, len(dimensions) - 1):
        if (dimensions[i] != dimensions[i + 1]).any():
            raise Exception("Channel dimensions do not match ", dimensions[i], " ", dimensions[i + 1])

    # Get the global dimensions
    dim = dimensions[0]
    # and adjust for the offset. Note that the offset is [x,y,z] while the
    # shape is [z,y,x]
    dim[0] += offset[2] * dim[0]
    dim[1] += offset[1] * dim[0]
    dim[2] += offset[0] * dim[0]

    # Make the idx file
    idx_file = IdxFile()
    idx_file.logic_box = BoxNi(PointNi(0, 0, 0), PointNi(int(dim[2]), int(dim[1]), int(dim[0])))
    for i in range(len(channels)):
        idx_file.fields.push_back(Field('channel%d' % i, DType.fromString("uint16")))

    idx_file.timesteps.addTimesteps(*timesteps)
    idx_file.time_template = "time_%02d/"
    success = idx_file.save(idx_name)
    ASSERT(success)

    dataset = LoadDataset(idx_name)
    if not dataset: raise Exception("Cannot load idx")

    access = dataset.createAccess()
    if not access: raise Exception("Cannot create access")


if __name__ == '__main__':
    from skimage import io

    """ This file is used to demonstrated  an initial IDX conversion"""

    SetCommandLine("__main__")
    IdxModule.attach()

    # trick to speed up the conversion
    os.environ["VISUS_DISABLE_WRITE_LOCK"] = "1"

    raw_data_path = '/Users/yi10/Desktop/Research/Datasets/20191106'
    idx_path = '/Users/yi10/Desktop/Research/Datasets/20191106_idx'
    idx_name = idx_path + '/view3_4D_ch1_488_ch2_mcherry.idx'

    offset = np.array([0.6, 0, 0])
    single_T_tiffs = list()
    single_T_tiffs.append(raw_data_path + '/view3_ch0_487_ch1_561_ch0_stack0000_0nm_0000000msec_0002557530msecAbs.tif')
    single_T_tiffs.append(raw_data_path + '/view3_ch0_487_ch1_561_ch1_stack0000_3nm_0000000msec_0002557530msecAbs.tif')

    make_idx(single_T_tiffs, idx_name, offset, [0, 100, 1])

    print('make_idx done')
    tiffs_4D = [f for f in listdir(raw_data_path) if isfile(join(raw_data_path, f)) and f.endswith(".tif")]
    for time_id in np.arange(0, 99):  # loop through all time steps
        for channel_id in np.arange(0, 2):  # go through all the channels in this time step

            subs = '_ch' + str(channel_id) + '_stack' + str(time_id).zfill(4) + '_'
            f = [x for x in tiffs_4D if (subs in x) and ('view3' in x)]

            if len(f) > 1:
                sys.exit('Ambiguous file name!')
            if len(f) < 1:
                sys.exit('file missing')

            add_stack(idx_name, np.int(time_id), "channel%d" % channel_id, raw_data_path + '/' + f[0], offset)

    # IdxModule.detach()
    print("Done with conversion")
    dataset = LoadDataset(idx_name)