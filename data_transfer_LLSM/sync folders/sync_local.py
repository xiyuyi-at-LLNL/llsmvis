from dirsync import sync

source_dir = r"C:\Users\miao1\Development\data_transfer_LLSM\sync folders\test_dirs\source"
target_dir = r"C:\Users\miao1\Development\data_transfer_LLSM\sync folders\test_dirs\target2"
log_file=r"C:\Users\miao1\Development\data_transfer_LLSM\sync folders\test_dirs\log.txt"


sync(source_dir, target_dir, action="diff", verbose=True, create=True)
