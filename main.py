# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:09:02 2022

@author: berna
"""

import get_hydrus as gh
import hydrus_in_out_functions as hh

path = 'C:/Users/Public/Documents/PC-Progress/Hydrus-1D 4.xx/Examples/Direct/TEST2A/'

#hh.change_par_selectorin(path, 'Ks', 2.5)
hyd=gh.hydrus_handler(path)
hyd.run_hydrus()
# (df,text)=hh.get_atmosph_in(path)
# a=df['Prec']
A=hh.write_atmosph_in(path,par_change='Prec',col_multiple=1/4)

#print (a)



