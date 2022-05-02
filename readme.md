### setup the conda environment for llsmvis

## This repository is under development.

1. Install anaconda:
   on LC:
   After login onto LC, go to the path of anaconda installers:
   >> cd /collab/usr/gapps/python/$SYS_TYPE/conda
   install anaconda3: 
   >> bash ./Anaconda3-2019.10-Linux-x86_64.sh
   Follow the prompted instructions to activate anaconda, and initialize conda.

   reference: https://hpc.llnl.gov/software/development-environment-software/python
 
2. Create a virtual environment for llsmvis under folder llsmvis:	
   >> bash llsmvis-setup

## Dataset
The dataset is being uploaded to figshare (find it [here](https://figshare.com/articles/journal_contribution/Datasets_for_the_manuscript_titled_A_Tailored_Approach_to_Study_Legionella_Infection_Using_Lattice_Light_Sheet_Microscope_LLSM_/19694809?file=34982371)).

### Processing
To process all the raw ata after an imaging session with multiple stacks and various imaging conditions.
1. activate the llsmv conda environment 
    >> conda activate llsmvis 
2. copy ./tools/getdsk into the data file folder and run it.
    >> ./getdsk  

answer the prompted questions accordingly, and you'll find the results under folder 'results_dsk'

Find developing notes [here](./documents/docs_main.md).

This work was produced under the auspices of the U.S. Department of Energy by
Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. Release number: LLNL-CODE-834237
