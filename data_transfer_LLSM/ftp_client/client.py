from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import DownloadSynchronizer
from time import time, sleep

local = FsTarget(r"C:\Users\miao1\Development\data_transfer_LLSM\ftp_client\sync_target")
user ="myuser"
passwd = "myuser"
remote = FtpTarget("", "127.0.0.2", username=user, password=passwd, tls=False, port=2121)
#opts = {"resolve": "skip", "verbose": 1}
opts={}
s = DownloadSynchronizer(local, remote, opts)
while True:
    s.run()
    sleep(5 - time() % 5)