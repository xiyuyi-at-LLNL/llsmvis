import numpy as np
from tifffile import imsave
import os
from time import time, sleep

target=r"C:\Users\miao1\Development\llsmvis\data_transfer_LLSM\ftp_server\public"

channels = 10
acquisition_name = "image"
for channel in range(channels):
    sx = 600
    sy = 600
    sz = 600

    seed = [int(sx / 2), int(sy / 2), int(sz / 2)]

    a = 10 * channel
    b = 5 * channel
    c = 10 * channel

    arr = np.zeros((sx, sy, sz), 'uint16')

    for z in range(-a, a):
        for y in range(-b, b):
            for x in range(-c, c):
                res = pow(x, 2) / pow(a, 2) + pow(y, 2) / pow(b, 2) + pow(z, 2) / pow(c, 2)
                if(res < 1):
                    i = x + a + seed[0]
                    j = y + b + seed[1]
                    k = z + c + seed[2]
                    if((i < sx) & (j < sy) & (k < sz)):
                        arr[i, j, k] = channel

    file_name = acquisition_name + "__ch" + str(channel) + "_stack0000_0nm_0000000msec_0019825262msecAbs.tif"
    tiff_path = os.path.join(target, file_name)

    imsave(tiff_path, arr)
    print("saved " + file_name)
    sleep(15 - time() % 15)


