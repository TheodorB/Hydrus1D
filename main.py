# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:09:02 2022

@author: berna
"""
import matplotlib.pyplot as plt
import get_hydrus as gh
import hydrus_in_out_functions as hh

path = 'C:/Users/Public/Documents/PC-Progress/Hydrus-1D 4.xx/Examples/Direct/TEST2C/'

#hh.change_par_selectorin(path, 'Ks', 2.5)
hyd=gh.hydrus_handler(path)

X=[]
Y=[]
(df,text)=hh.get_atmosph_in(path)
prec_ini=df['Prec']


for k in range (5,6):
    i=k/10
    prec_modif=prec_ini*i
    print(prec_modif[1])
    
    A=hh.write_atmosph_in(path,par_change='Prec',col_values=prec_modif)
    
    hyd.run_hydrus()
    t_level=hyd.get_t_level_out()
#     print(t_level)
#     TA=t_level['sum(vRoot)']
#     TP=t_level['sum(rRoot)']

#     ta=TA[len(TA)-1]
#     tp=TP[len(TP)-1]
#     X+=[i]
#     Y+=[ta/tp]
    
A=hh.write_atmosph_in(path,par_change='Prec',col_values=prec_ini)
    
# plt.plot(X,Y)
    
    
    
    




