# write a python version of the getdsk that was in bash
# -Xiyu 2021.Aug.10.

# This python script checks, organizes, generates and submits slurm jobs to deskew and calcualte the MIPs for all the
# tiff files under the current directory.
#
# To be specific, it checks the *_Setting.txt files generate by the LLSM instrument, and prepares
# the corresponding executable python scripts for deskew and MIP calculations.
# Each *_Setting.txt file describes the specifics on one dataset containing the volumetric acquisition
# of all the channels and time steps.
#
# The resultant python and slurm scripts are placed in the '' folder under the current directory.
import datetime
import os
import shutil
from pathlib import Path
import sys

print('startig time')
now = datetime.datetime.now()
print ("Current date and time : ")
print (now.strftime("%Y-%m-%d %H:%M:%S"))

current_directory = os.getcwd()

jobs_dsk_path = os.path.join(current_directory, 'jobs_dsk')
if not os.path.exists(jobs_dsk_path):
    os.makedirs(jobs_dsk_path)

results_dsk_path = os.path.join(current_directory, 'results_dsk')
if not os.path.exists(results_dsk_path):
    os.makedirs(results_dsk_path)


def syscopy(source, dest, fname_ends):
    for file in os.listdir(source):
        print(file)
        if file.endswith(fname_ends):
            sourcefile=os.path.join(source,file)
            destfile=os.path.join(dest,file)
            shutil.copyfile(sourcefile, destfile)


syscopy(current_directory, results_dsk_path, ".txt")  # move all .txt files to the results_dsk folder.
homepath = str(Path.home())
pythonpath = os.path.join(sys.prefix, 'bin', 'python')


print("echo generate .mp4 files for mip movies? \(y/[n]\)")
v=input()
if v is 'y':
    mp4flag="yes"
else:
    mp4flag="no"

##### identify and prepare single node jobs using sbatch for each file head
slurms=[]


# for i in $(ls *.txt) # check all txt files
for file in os.listdir(os.getcwd()): # check all txt files
# do
#     if [[ $i == *_Settings.txt ]] # consider only the Setting.txt files, each corresponds to one 4D dataset.
    if file.endswith('Settings.txt'):
#     then
#
     # get the file head of the 4D datasete
        print('prep for ' + file)
#     echo prep for $i
#
     # define filehead string
        filehead=file[:-13]
#     filehead=${i:0:${#i}-13}
#
     # define path string, handle the special characters "/" in the path.
        fpath=os.getcwd()
#     fpath=$(echo $(pwd) | sed 's/\//\\\//g')
#
     # define seed file path for the executabllse python script and the slurm (shell)
#     seedpy=$(echo ~/llsmvis/tools/deskew4D.seed)
        seedpy = os.path.join(homepath, 'llsmvis', 'tools', 'deskew4D.seed')
#     if [ -f $seedpy ]; then :; else echo $seedpy not found; fi
        if os.path.exists(seedpy):
            pass
        else:
            print(seedpy+' not found')
#
#     seedsl=$(echo ~/llsmvis/tools/slurm.seed)
        seedsl = os.path.join(homepath, 'llsmvis', 'tools', 'slurm.seed')
#     if [ -f $seedsl ]; then :; else echo $seedsl not found; fi
        if os.path.exists(seedsl):
            pass
        else:
            print(seedsl + ' not found')
#     # define output file path for the executable python script and the slurm (shell)
#     foutpy="./jobs_dsk/deskew4D_"$filehead".py"
        foutpy = os.path.join(current_directory,'jobs_dsk','deskew4D_'+filehead+'.py')
#
#     foutsl="./jobs_dsk/slurm_"$filehead
        foutsl = os.path.join(current_directory,'jobs_dsk','slurm_'+filehead)
#
#     # prepare the corresponding executable python script
#     sed -e "s/FPATH/\"$fpath\"/g" -e "s/FHEAD/\"$filehead\"/g" \
#     -e "s/\[WHICHPYTHON\]/$pythonpath/g" -e "s/\[HOME\]/\"$homepath\"/g" $seedpy > $foutpy
        with open(seedpy, "rt") as fin:
            with open(foutpy, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('FPATH', "\""+fpath+"\""
                                            ).replace('FHEAD',"\""+filehead+"\""
                                            ).replace('[WHICHPYTHON]',pythonpath
                                            ).replace('[HOME]',"\""+homepath+"\""))

        fin.close()
        fout.close()


#     if [[ $mp4flag == "yes" ]]
        if mp4flag is "yes":
#     then
#       echo "[fig, ax] = utils.render_mpl_table(p, p.data_properties, header_columns=0, col_width=7.0)" >> $foutpy
            with open(foutpy, "a") as fout:
                fout.write("[fig, ax] = utils.render_mpl_table(p, p.data_properties, header_columns=0, col_width=7.0)\n")
#       echo "utils.getLabeledXYmip_MP4(p, 0, 1, channel_inds=None)" >> $foutpy
                fout.write("utils.getLabeledXYmip_MP4(p, 0, 1, channel_inds=None)\n")
#       fi
#

# prepare the corresponding slurm
#     sed "s/\[EXECUTABLE\]/$fpath\/jobs_dsk\/deskew4D_"$filehead".py/g" $seedsl > $foutsl
        with open(seedsl, "rt") as fin:
            with open(foutsl, "wt") as fout:
                for line in fin:
                    fout.write(line.replace('[EXECUTABLE]', os.path.join(fpath,'jobs_dsk','deskew4D_'+filehead+'.py')))

        fin.close()
        fout.close()

#     chmod u+rwx $foutpy
#     chmod u+rwx $foutsl
#     slurms+=(slurm_$filehead)
#     fi
# done
#
if sys.platform.startswith('linux'):
    os.system('chmod u+rwx ' + foutpy)
    os.system('chmod u+rwx ' + foutsl)
    slurms.append('slurm_' + filehead)
    # #### Launch single node jobs using sbatch for each
    # echo submit all jobs? \(y/[n]\)
    print('submit all jobs? \(y/[n]\)')
    # read v
    v = input()
    # if [[ $v == "y" ]]
    if v is "y":
        # then
        #   cd jobs_dsk
        os.system('cd jobs_dsk')
        #   for s in ${slurms[@]}
        for s in os.listdir(os.getcwd()):
            if s.startswith('slurm'):
                print('submitting ' + s)
                os.system('sbatch ' + s)
        #   do
        #     echo submitting $s
        #     sbatch $s
        #   done
        #   cd ..

        os.system('cd ..')
        print('all job submitted.')
    #   echo all job submitted.
    # else
    else:
        print('all jobs are prepared in ./jobs_dsk')
    #   echo all job are prepared in ./jobs_dsk
    #   echo
    # fi
else:
    print('Not on cluster, skip preparing the slurm scripts.')