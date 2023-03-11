# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:09:02 2022

@author: berna
"""
import os
import matplotlib.pyplot as plt
import get_hydrus as gh
import hydrus_in_out_functions as hh

path = 'C:/Users/Public/Documents/PC-Progress/Hydrus-1D 4.xx/Examples/Direct/TEST2g/'

#hh.change_par_selectorin(path, 'Ks', 2.5)
hyd=gh.hydrus_handler(path)

X=[]
Y=[]
(df,text)=hh.get_atmosph_in(path)
prec_ini=df['Prec']

##copied from gh.run_hydrus because there is permission problem when opening LEVEL_01 too many times
path_exe='C:/Program Files (x86)/PC-Progress/Hydrus-1D 4.xx/'
with open('{}LEVEL_01.DIR'.format(path_exe),'w') as f:
    f.write(path)

    
os.chdir("{}".format(path_exe))


for k in range (5,10):
     i=k/10
     prec_modif=prec_ini*i
     
     
    
     A=hh.write_atmosph_in(path,par_change='Prec',col_values=prec_modif.round(3))
    
     #runs hydrus
     os.startfile("H1D_CALC.EXE")   
     
     
     t_level=hyd.get_t_level_out()

     TA=t_level['sum(vRoot)']
     TP=t_level['sum(rRoot)']

     ta=TA[len(TA)-1]
     tp=TP[len(TP)-1]
     X+=[i]
     Y+=[ta/tp]
plt.plot(X,Y)     
A=hh.write_atmosph_in(path,par_change='Prec',col_values=prec_ini)
     

    