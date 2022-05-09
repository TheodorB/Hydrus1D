# Hydrus1D
Running hydrus in batch mode using Python 3. Written for Linux but can be accomodated to Windows OS

Works on Linux but nothing should be different in the get_hydrus.py functions except the way the directories are written (\ seperators  instead of /) and the "wine" command that is used for running windows software in linux (you can delete it when running Windows).

You basically need to write your hydrus project directory to Level_01.dir file and execute H1D_CALC.EXE


### Example1:
import pandas as pd

import get_hydrus as gh # MY HYDRUS IMPORT FUNCTIONS

import hydrus_in_out_functions as hh # MY HYDRUS CHANGE DATA FUNCTIONS

calc_path = '/home/theodor/Documents/hyd_calc01' # path to calc.exe file
run_path = '/home/theodor/Documents/hydrus/WRF_RAIN01' # path to hydrus project folder

### run hydrus
hyd = gh.hydrus_handler(run_path, exe_folder=calc_path)
hyd.run_hydrus()

### If you want to change parameters and input data the hydrus_in_out_functions.py has a lot of functions
#### example for changing Ks:
hh.change_par_selectorin(run_path, 'Ks', 2.5);
#### example for changin atmospheric data:
atmdf, atmtxt  = hh.get_atmosph_in(run_path) # atmdf is a pandas dataframe 
atmdf['rRoot'] = 2.0*atmdf['rRoot'] # you just doubled the transpiration
hh.write_atmosph_in(run_path, atmdf, atmtxt) # write data back to the hydrus input file

#### you can now run hydrus again after the changes
