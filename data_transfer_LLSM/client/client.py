from ftpsync.targets import FsTarget
from ftpsync.ftp_target import FtpTarget
from ftpsync.synchronizers import DownloadSynchronizer
from time import time, sleep
import logging
import logging.handlers
from ftpsync.util import set_pyftpsync_logger
import os
import yaml
import sys

def read_config():
    config_path = os.path.join(os.getcwd(), "config.yaml")
    print(config_path)
    with open(config_path, "r") as f: 
        return yaml.safe_load(f)

def main(dataset_name = ""):
    #FTP Configuration
    config_ftp = read_config().get("FTP")
    TARGET_DIRECTORY = config_ftp.get("TARGET_DIRECTORY")
    PORT = config_ftp.get("PORT")
    IP = config_ftp.get("IP")
    FTP_USER = config_ftp.get("FTP_USER")
    FTP_PASSWORD = config_ftp.get("FTP_PASSWORD")

    #SYNC Configuration
    config_sync = read_config().get("SYNC")
    WAIT_SECONDS = config_sync.get("WAIT")

    custom_logger = logging.getLogger("pyftpsync")
    log_path = os.path.join(TARGET_DIRECTORY, "data_sync.log")
    handler = logging.handlers.WatchedFileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    set_pyftpsync_logger(custom_logger) 
    custom_logger.setLevel(logging.DEBUG)

    #ftp client setup
    local = FsTarget(TARGET_DIRECTORY)
    remote = FtpTarget("", IP, username=FTP_USER, password=FTP_PASSWORD, tls=False, port=PORT)
    # opts={"verbose": 5, "force": True, "match": "file*.txt" }
    opts={"verbose": 5, "force": True, "match": dataset_name}
    s = DownloadSynchronizer(local, remote, opts)

    #run this and check if there are updates
    c = 1
    while True:
        custom_logger.info("=========== Sync Started ===========")
        custom_logger.info("sync iteration: " + str(c))
        s.run()
        custom_logger.info("*** sync stats ***")
        custom_logger.info(s.get_stats())

        custom_logger.info("=========== Sync Finished ===========")
        sleep(WAIT_SECONDS - time() % WAIT_SECONDS)
        
        c+=1

    s.close()

def prompt_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    while True:
        sys.stdout.write(question + "\n[yes/no]")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

if __name__ == '__main__':

    if(len(sys.argv) > 1): 
        dataset_name = sys.argv[1] + "*" #TODO the issue with this is that if there are datasets that contain part of the name of another dataset
        main(dataset_name)

    else: 
        copy_all = prompt_yes_no("You didn't specify a dataset name. Without specifying one, every file will be copied. Go ahead? ")
        if(copy_all):
            main()
        else:
            print("Abort. Nothing will be copied. Good bye!")
