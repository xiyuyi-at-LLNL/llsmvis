from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import DownloadSynchronizer
from time import time, sleep
import logging
import logging.handlers
from ftpsync.util import set_pyftpsync_logger
import os

path_local = r"C:\Users\miao1\Development\llsmvis\data_transfer_LLSM\ftp_client\sync_target"

# logging

custom_logger = logging.getLogger("pyftpsync")
log_path = os.path.join(path_local, "data_sync.log")
handler = logging.handlers.WatchedFileHandler(log_path)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
custom_logger.addHandler(handler)
set_pyftpsync_logger(custom_logger) 
custom_logger.setLevel(logging.DEBUG)

#ftp client setup
local = FsTarget(path_local)
user ="myuser"
passwd = "myuser"
remote = FtpTarget("", "192.168.0.123", username=user, password=passwd, tls=False, port=2121)
# opts={"verbose": 5, "force": True, "match": "file*.txt" }
opts={"verbose": 5, "force": True}
s = DownloadSynchronizer(local, remote, opts)

#run this and check if there are updates
while True:
    custom_logger.info("=========== download from ftp server ===========")
    s.run()
    custom_logger.info("*** sync stats ***")
    custom_logger.info(s.get_stats())

    u = "abc_äöü_¿ß"
    s = u.encode("utf-8")
    remote.write_text(log_path, s)

    custom_logger.info("=========== download finished ===========")
    sleep(5 - time() % 5)

s.close()