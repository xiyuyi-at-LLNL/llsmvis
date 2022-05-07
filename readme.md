## llsmvis
llsmvis is a collection of codes that we used to analyze the datasets acquired in the following study:

Yi, X., Miao, H., Lo, J.K.Y., Elsheikh, M., Lee, T.H., Jiang, C., Segelke, B.W., Overton, K.W., Bremer, P.T. and Laurence, T.A., 2022. A Tailored Approach To Study Legionella Infection Using Lattice Light Sheet Microscope (LLSM). bioRxiv.
doi: https://doi.org/10.1101/2022.03.20.485032 

#### Prerequisits: Python, Conda, Git, Jupyter notebook.

## Relevant datasets.
The dataset is being uploaded to figshare (find it [here](https://figshare.com/articles/journal_contribution/Datasets_for_the_manuscript_titled_A_Tailored_Approach_to_Study_Legionella_Infection_Using_Lattice_Light_Sheet_Microscope_LLSM_/19694809?file=34982371)).


## 1. Getting started.
### 1.1. Install [Anaconda](https://docs.anaconda.com/anaconda/install/).

### 1.2. Clone the repository.
`git clone https://github.com/xiyuyi-at-LLNL/llsmvis.git`

### 1.3. Configure the conda virtual environment.
`conda env create -f mac_env.yml` (tested for MacOS Majave 10.14.3)`



## for LC users:
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



### Data processing for LC users (to deskew acquired datasetes).
To process all the raw ata after an imaging session with multiple stacks and various imaging conditions.
1. activate the llsmv conda environment 
    >> conda activate llsmvis 
2. copy ./tools/getdsk into the data file folder and run it.
    >> ./getdsk  

answer the prompted questions accordingly, and you'll find the results under folder 'results_dsk'


## Note.
This work was produced under the auspices of the U.S. Department of Energy by
Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344. Release number: LLNL-CODE-834237
