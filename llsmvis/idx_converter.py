# This script is developed from a script from Timo (bremer5) with very minor modifications on format only.
from os import listdir
from os.path import isfile, join, split
from skimage import io
import sys
from OpenVisus import *
from llsmvis import globals
import numpy as np
from llsmvis.globals import *

class IDXConverter:
    def __init__(self, p):
        # define basic attributes from the parser object
        if VERBOSE:
            self.VERBOSE = True
        else:
            self.VERBOSE = False

        self.p = p
        self.offset = p.idx_offset  # offset defined in parser, based on file information. should be integers
        self.convert_from_deskewed = False
        print("Idx conversion of dataset:\n    " + self.p.fpath + "/" + self.p.fname_head + "\n\n")

        # trick to speed up the conversion
        os.environ["VISUS_DISABLE_WRITE_LOCK"] = "1"

    def ASSERT(self,cond):
        if not cond: raise Exception("Assert failed")

    def MSG(self,text):
        if self.VERBOSE:
            print(text)

    def add_stack(self, idx_name, time_step, channel, tiff_file, offset=[0, 0, 0]):
        from skimage import io
        """Add a stack of images given as a tiff image to the 
        given idxfile"""
        # Make sure we are given a valid idx file and we can
        # create an access to it
        dataset = LoadDataset(idx_name)
        access = dataset.createAccess()
        field = dataset.getFieldByName(channel)
        self.ASSERT(dataset)
        # Now try to open the tiff file. We are using the skimage reader
        # as other implementations did not read the correct stack info
        img = io.imread(tiff_file)
        self.MSG("Adding %s to idx file %s" % (split(tiff_file)[-1], idx_name))
        # Now make sure that the dimensions match
        global_box = dataset.getLogicBox()
        local_box = np.flip(np.array(img.shape))

        # Remember that the local shape will change by the offset which
        # we expect to be applied in Z -direction
        extended_box = local_box + local_box[2] * offset

        if extended_box[0] != global_box.p2[0] or extended_box[1] != global_box.p2[1] or extended_box[2] != global_box.p2[
            2]:
            print("Dimensions in the idx file ", global_box.p2[0], global_box.p2[1], global_box.p2[2],
                  " do not match the local dimensions in the tiff, padding zeros ", local_box)
            # padd zeros to match the box
            target_local_box = extended_box - extended_box[2]*offset
            imgpad = np.zeros(np.flip(target_local_box))
            # index flip
            imgpad[0:target_local_box[2], 0:target_local_box[1], 0:target_local_box[0]] = img
            img = imgpad

        # Now we go through each slice and add them one by one since
        # we have to take care of the offset
        for Z in range(0, local_box[2]):

            if Z % 50 == 0:
                self.MSG("    Processing slice %d" % Z)

            data = img[Z, :, :]

            # Now compute the target location
            bottom = PointNi(int(offset[0] * Z), int(offset[1] * Z), Z)
            top = PointNi(int(offset[0] * Z + local_box[0]), int(offset[1] * Z + local_box[1]), Z + 1)
            #print(bottom[0], bottom[1], bottom[2], " -- ", top[0], top[1], top[2])

            target_box = BoxNi(bottom, top)

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
            self.ASSERT(dataset.executeQuery(access, query))

    def make_idx(self, tiff_channels, tiff_channels_dict, idx_name, offset=[0, 0, 0], timesteps = [0, 1, 1]):
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

        # now give reasonable channel names:
        for i in tiff_channels_dict:
            idx_file.fields.push_back(Field(i['channel name'], DType.fromString("uint16")))

        idx_file.timesteps.addTimesteps(*timesteps)
        idx_file.time_template = "time_%02d/"
        success = idx_file.save(idx_name)
        self.ASSERT(success)

        dataset = LoadDataset(idx_name)
        if not dataset: raise Exception("Cannot load idx")

        access = dataset.createAccess()
        if not access: raise Exception("Cannot create access")

    def convert_all(self):
        # define idx name (full path)
        IdxModule.attach()
        idx_name = self.p.fpath + '/results_idx/IDX_' + self.p.fname_head + '.idx'
        if self.convert_from_deskewed:
            ### need to change this for deskewed to the correct path ###
            single_tstep_tiffs = [self.p.fpath + '/' + self.p.fname_head + '_deskewed'
                                  + '/Deskewed_' + s['path of tiff'].split('/')[-1] for s in self.p.dict_tstep0_tiffs]
        else:
            single_tstep_tiffs = [s['path of tiff'] for s in self.p.dict_tstep0_tiffs]

        self.make_idx(single_tstep_tiffs, self.p.dict_tstep0_tiffs, idx_name, self.offset, [0, self.p.tsteps_n, 1])
        print('make_idx done')
        tif_dict = sorted(self.p.dict_tiffs, key=lambda i: (i['time step'], i['channel index']))
        for f in tif_dict:
            if self.convert_from_deskewed:
                ### need to change this for deskewed to the correct path t###
                tiff_file = self.p.fpath + '/' + self.p.fname_head + '_deskewed' \
                            + '/Deskewed_' + f['path of tiff'].split('/')[-1]
                print('now adding ' + tiff_file)
                self.add_stack(idx_name,  # idx_name
                               np.int(f['time step']),  # time_step
                               f['channel name'],  # channel
                               tiff_file,  # tiff_file
                               np.array([0, 0, 0]))
            else:
                print('    Adding time step ' + str(f['time step']) + '/' + str(self.p.tsteps_n - 1)
                      + "; channel index " + str(f['channel index']) + '/' + str(self.p.channel_n - 1))
                self.add_stack(idx_name,  # idx_name
                               np.int(f['time step']),  # time_step
                               f['channel name'],  # channel
                               f['path of tiff'],  # tiff_file
                               self.offset)

        IdxModule.detach()
        print("    DONE with idx conversion\n")

    def convert_stacks(self, fnames, stack, despath):
        # convert an input block (stack), and save the converted data into the destination path (despath).
        # define idx name (full path)
        # IdxModule.attach()
        # idx_name = despath + '/IDX_' + self.p.fname_head + '.idx'
        #
        # self.make_idx([fname], self.p.dict_tstep0_tiffs, idx_name, self.offset, [0, self.p.tsteps_n, 1])
        # print('make_idx done')
        # tif_dict = sorted(self.p.dict_tiffs, key=lambda i: (i['time step'], i['channel index']))
        # for f in tif_dict:
        #     if self.convert_from_deskewed:
        #         ### need to change this for deskewed to the correct path t###
        #         tiff_file = self.p.fpath + '/' + self.p.fname_head + '_deskewed' \
        #                     + '/Deskewed_' + f['path of tiff'].split('/')[-1]
        #         print('now adding ' + tiff_file)
        #         self.add_stack(idx_name,  # idx_name
        #                        np.int(f['time step']),  # time_step
        #                        f['channel name'],  # channel
        #                        tiff_file,  # tiff_file
        #                        np.array([0, 0, 0]))
        #     else:
        #         print('    Adding time step ' + str(f['time step']) + '/' + str(self.p.tsteps_n - 1)
        #               + "; channel index " + str(f['channel index']) + '/' + str(self.p.channel_n - 1))
        #         self.add_stack(idx_name,  # idx_name
        #                        np.int(f['time step']),  # time_step
        #                        f['channel name'],  # channel
        #                        f['path of tiff'],  # tiff_file
        #                        self.offset)
        #
        # IdxModule.detach()
        # print("    DONE with idx conversion\n")
