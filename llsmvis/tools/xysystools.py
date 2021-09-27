import os
import shutil


def syscopy(dest,source,fname_endstring):
    for file in os.listdir(source):
        if file.endswith(fname_endstring):
            shutil.copy2(dest,source)
