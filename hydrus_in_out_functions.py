#!/home/theodor/anaconda3/bin/python
"""
Created on Sun Oct 30 22:18:05 2016
@author: theodor
"""

import os
import pandas as pd
import numpy as np

def get_profile_dat(run_path):
    '''
    read and write Profile.dat
    returns: df, textpd
    '''
    textpd = dict() # dictionary with text file data by row , textpd =text of profile.dat
    try:
        with open(os.path.join(run_path,'Profile.dat'),'r') as f:
            for i, line in enumerate(f):
                textpd[i] = line.split()
    #            if 'Mat' in textpd[i]:
    #               start_row = start_row + 1
    except:
        with open(os.path.join(run_path,'PROFILE.DAT'),'r') as f:
            for i, line in enumerate(f):
                textpd[i] = line.split()
    mypars = textpd[4][3:] # parameters for column names  of dataframe
    n_nodes = int(textpd[4][0]) # this can change.  if "Pcp_File_Version=4" not in first row
    num_pars = len(textpd[5])
    mypars = textpd[4][3:] # parameters for column names  of dataframe
    start_row  = 5
    if len(mypars) == len(textpd[start_row]) - 1: # in case of 2 solutes
        extention = ['Conc1', 'Conc2']
        mypars = mypars[:-1]
        textpd[4] = textpd[4][:-1]
        textpd[4].extend(extention)
        mypars.extend(extention)    
    end_row   = start_row + n_nodes
    dfarray = np.empty(shape=(end_row - start_row, num_pars))
    lines = list(range(start_row, end_row))
    for i,line in enumerate(lines):              # i are serial row numbers in the array
        dfarray[i,:] = [float(k) for k in textpd[line][:num_pars] ]
    df = pd.DataFrame(data=dfarray, columns=mypars[:num_pars])
    return df, textpd

# %%
# write back to Profile.dat
def write_profile_dat(run_path, df, textpd, **kwargs):
    '''
    df = df from original Profile_dat
    textpd    = dict of text from original profile_dat
    par_change = parameter you want to change
    values = values to place in changed parameter (same length)
    **kwargs = {par_change,col_values} - change one column in the dataframe

    example:
    write_profile_dat(run_path, df = new_pfor, textpd = hydrus_dict['profile_dat']['textpd'],
                  par_change='h',col_values=-40* np.ones(len(new_pfor)))
    '''
    df[['1','Mat', 'Lay']] = df[['1','Mat', 'Lay']].astype(int)
    df[['1','Mat', 'Lay']] = df[['1','Mat', 'Lay']].astype(str) # these columns should be integer strings
    if ('par_change' and 'col_values') in kwargs.keys():
        df[kwargs['par_change']] = kwargs['col_values']
    n_nodes = int(textpd[4][0]) # this can change.  if "Pcp_File_Version=4" not in first row
#    num_pars = len(textpd[5])
#    mypars = textpd[4][3:] # parameters for column names  of dataframe
    start_row  = 5
    end_row   = start_row + n_nodes
    lines = list(range(start_row, end_row))
    for i,line in enumerate(lines):              # i are serial row numbers in the array
        textpd[line] = map(str, df.loc[i,:].values.tolist())
    str_for_file = '\n'.join('  '.join(elem for elem in line) for i,line in textpd.items())
    with open(os.path.join(run_path,'PROFILE.DAT'),'w') as f:
#    with open(os.path.join(run_path,'Profile.dat'),'w') as f:       
        f.write(str_for_file)
    return  #rewrites profile in profile.dat
# %%
def change_par_selectorin(run_path,par,par_new_value, row_under=1):
    '''
    change parameter value in Selector.in file. tested for Ks so far
    row_under - for multiple materials. for material. Ex: =2 for material no.2
    '''
    text = dict()
    try:
        with open(os.path.join(run_path,'Selector.in'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
        capital = False
    except:
        with open(os.path.join(run_path,'SELECTOR.IN'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()  
        capital = True
    # find variable('Ks')
#    print(capital)
    row =  [key for key, value in text.items() if par in value][0]
    text[row+row_under][text[row].index(par)] = str(par_new_value)
    str_for_file = '\n'.join('  '.join(elem for elem in line) for i,line in text.items())
    if capital == True:
        filename = 'SELECTOR.IN'
    else:
        filename = 'Selector.in'
    with open(os.path.join(run_path, filename),'w') as f:
        f.write(str_for_file)
    return  text # changes parameter in Selector in file
#%%
def get_par_selectorin(run_path,par, row_under=1):
    '''
    get parameter value in Selector.in file. tested for Ks so far
    '''
#     run_path = os.path.join(path,example)
    text = dict()
    try:
        with open(os.path.join(run_path,'Selector.in'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
    except:
        with open(os.path.join(run_path,'SELECTOR.IN'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()        
    # find variable
    row =  [key for key, value in text.items() if par in value][0]
    return  text[row + row_under][text[row].index(par)] # return desired parameter in Selector in file

#%%
def get_par_selectorin_from_text(text,par, row_under=1):
    '''
    get parameter value in Selector.in text. tested for Ks so far
    '''
    # find variable
    row =  [key for key, value in text.items() if par in value][0]
    return  text[row + row_under][text[row].index(par)] # return desired parameter in Selector in file

#%%

def get_munit_selectorin(run_path, par='LUnit'):
    '''
    get mass unit value in Selector.in file. it is 3 rows under 'Lunit'
    '''
#     run_path = os.path.join(path,example)
    text = dict()
    try:
        with open(os.path.join(run_path,'Selector.in'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
    except:
        with open(os.path.join(run_path,'SELECTOR.IN'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()        
    # find variable
    row =  [key for key, value in text.items() if par in value][0]
    return  text[row+3][text[row].index(par)] # return desired mass unit in Selector in file
# %%
def get_selectorin(run_path):
    text = dict()
    try:
        with open(os.path.join(run_path,'Selector.in'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
    except:
        with open(os.path.join(run_path,'SELECTOR.IN'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()        
    return text
# %%
def change_print_times(run_path, tMax, times, how='linespaced',tInit=0.0):
    '''
    times - times of print
    tInit -first print time
    tMax  - max print time
    how - {'logspaced', 'linespaced'}
    TPrint1
    '''
    dtMin = float(get_par_selectorin(run_path, 'dtMin'))
    dt    = float(get_par_selectorin(run_path, 'dt'))

    if  how=='linespaced':
        print_times = np.linspace(tInit, tMax, num=times)
        if tInit == 0.0:
            print_times = np.linspace(tInit, tMax, num=times)
        else:
            raise ValueError('tInit must be zero')
    elif how=='logspaced':
        if tInit == 0.0:
            print_times = np.logspace(np.log10(tInit+0.00024), np.log10(tMax), num=times)
        else:
            raise ValueError('tInit must be zero')
    else:
        raise ValueError('specify print spaces method')

    if print_times[0] < (dtMin + dt):
        print_times[0] =  dtMin + dt

    mytext = change_par_selectorin(run_path,'MPL',len(print_times))
    mytext = change_par_selectorin(run_path,'tInit',tInit)
    mytext = change_par_selectorin(run_path,'tMax',tMax)
    my_keys = list(mytext.keys())
    # write print times
    if len(print_times)%6 != 0:
        print_times = np.concatenate([print_times, np.empty((6-len(print_times)%6))*np.nan])
    print_times = print_times.reshape((-1,6))
    # change parameters
    start_print_times_line = [k for k,v in mytext.items() if 'TPrint' in v[0]][0] + 1
    rows = print_times.shape[0] # number of rows of the print times
    # write first part of text dict up to print times
    range_first_part = range(start_print_times_line)
    first_part = dict(zip(range_first_part, [mytext[i] for i in range_first_part]))

    # write print times part of text dict
    range_print_part = range(start_print_times_line, start_print_times_line + rows) # keys of print time part
    print_part = dict()
    for iii, row in enumerate(range_print_part):
        print_part[row] = [str(i) for i in list(print_times[iii,:])]

    last_part = dict()
    range_of_keys = my_keys[start_print_times_line:] # range of middle keys to find start of last part
    start_of_last_part = min([i for i in range_of_keys if '***' in mytext[i]])
    last_part_keys = range(start_of_last_part, len(mytext))

    first_key_of_last_part = len(first_part) + len(print_part)
    for i, k in enumerate(last_part_keys):
        last_part[first_key_of_last_part+i] = mytext[k]

    first_part.update(print_part)
    first_part.update(last_part)
    new_text = first_part.copy()

    str_for_file = '\n'.join('  '.join(elem for elem in line) for i,line in new_text.items())
    try:
        with open(os.path.join(run_path,'SELECTOR.IN'),'w') as f:
            f.write(str_for_file)
    except:
        with open(os.path.join(run_path,'Selector.in'),'w') as f:
            f.write(str_for_file)        
    return print_times

# %%
def get_atmosph_in(run_path):
    '''
    get text dict and DataFrame of profile
    '''
    text = dict() # dictionary with text file data by row , textpd =text of profile.dat
    with open(os.path.join(run_path, 'ATMOSPH.IN'),'r') as f:
        for i, line in enumerate(f):
            text[i] = line.split()

    start_row  = 9   # this can change  if "Pcp_File_Version=4" not first row
    myint = 3 # integer of line number   # this can change  if "Pcp_File_Version=4" not first row
    n_times = int(text[myint][0])
    end_row   = start_row + n_times # - 1
    num_pars = len(text[start_row])
    mypars = text[start_row-1][:] # parameters for column names  of dataframe
    dfarray = np.empty(shape=(end_row - start_row, num_pars))
    lines = list(range(start_row, end_row))
    for i,line in enumerate(lines):              # i are serial row numbers in the array
        dfarray[i,:] = [float(k) for k in text[line][:num_pars] ]
    df = pd.DataFrame(data=dfarray, columns=mypars[:num_pars])
    return df, text
# %%
def write_atmosph_in(run_path, df, mytext, **kwargs):
    '''
    df = df from original Profile_dat
    textpd    = dict of text from original profile_dat
    par_change = parameter you want to change
    values = values to place in changed parameter (same length)
    **kwargs = {par_change,col_values} - change one column in the dataframe

    example:
    write_profile_dat(run_path, df = new_pfor, textpd = hydrus_dict['profile_dat']['textpd'],
                  par_change='h',col_values=-40* np.ones(len(new_pfor)))
    '''
#     df[['1','Mat', 'Lay']] = df[['1','Mat', 'Lay']].astype(int)
#     df[['1','Mat', 'Lay']] = df[['1','Mat', 'Lay']].astype(str) # these columns should be integer strings
    my_keys = list(mytext.keys())
    if ('par_change' and 'col_values') in kwargs.keys():
        df[kwargs['par_change']] = kwargs['col_values']

    start_row  = 9   # this can change  if "Pcp_File_Version=4" not first row
    n_times = len(df)
    mytext[3][0] = str(n_times) # change number of temporal data points (3  if "Pcp_File_Version=4" not first row )
    end_row   = start_row + n_times - 1
    lines = list(range(start_row, end_row+1))

    range_of_keys = my_keys[start_row:] # range of last keys df
    start_of_last_part = min([i for i in range_of_keys if 'END' in mytext[i]])

    last_part_dict = dict()
    for new_key, key in enumerate(list(mytext.keys())[start_of_last_part:]):
        last_part_dict[new_key] = mytext[key]
#     delete last part
    for k in list(mytext):
        if k>=start_row:
            del mytext[k]
#     write df to text dict
    for i,line in enumerate(lines):              # i are serial row numbers in the array
        mytext[line] = map(str, df.loc[i,:].values.tolist())
        
#    write last part after df
#    for i, key in enumerate(range(my_keys[-1]+1, my_keys[-1]+1 + len(last_part_dict))):
#        mytext[key] = last_part_dict[i]
    mytext[list(mytext.keys())[-1]+1] = last_part_dict[0]
    
    str_for_file = '\n'.join('  '.join(elem for elem in line) for i,line in mytext.items())
    with open(os.path.join(run_path,'ATMOSPH.IN'),'w') as f:
        f.write(str_for_file)
    return  #rewrites profile in profile.dat
#%%
def get_solute1_out(run_path):
    text = dict() # dictionary with text file data by row
    with open(os.path.join(run_path, 'solute1.out'),'r') as f:
        for i, line in enumerate(f):
            text[i] = line.split()

    mypars = text[2] # parameters for column names  of dataframe
    data_width = len(text[5]) # 5th line is arbitrary
    NObs = int((data_width - (len(mypars) - 3))/2) # number of observation points

    mypars = mypars[:-3]
    mypars.extend(['cv({})'.format(i) for i in range(1,NObs+1)])
    mypars.extend(['Sum(cv({}))'.format(i) for i in range(1,NObs+1)])

    start_row  = 4
    end_row   = [val[0] for val in text.items() if 'end' in val[1]][0]
    dfarray = np.empty(shape=(end_row - start_row, len(mypars)))
    lines = list(range(start_row, end_row))

    for i,line in enumerate(lines):              # i are serial row numbers in the array
        dfarray[i,:] = [float(k) for k in text[line]]
    soluteoutdf = pd.DataFrame(data=dfarray, columns=mypars)
    return soluteoutdf
#%%

def get_solute_out(run_path, SoluteNum=1):
    SoluteNum = int(SoluteNum)
    text = dict() # dictionary with text file data by row
    with open(os.path.join(run_path, 'solute{}.out'.format(SoluteNum)),'r') as f:
        for i, line in enumerate(f):
            text[i] = line.split()

    mypars = text[2] # parameters for column names  of dataframe
    data_width = len(text[5]) # 5th line is arbitrary
    NObs = int((data_width - (len(mypars) - 3))/2) # number of observation points

    mypars = mypars[:-3]
    mypars.extend(['cv({})'.format(i) for i in range(1,NObs+1)])
    mypars.extend(['Sum(cv({}))'.format(i) for i in range(1,NObs+1)])

    start_row  = 4
    end_row   = [val[0] for val in text.items() if 'end' in val[1]][0]
    dfarray = np.empty(shape=(end_row - start_row, len(mypars)))
    lines = list(range(start_row, end_row))

    for i,line in enumerate(lines):              # i are serial row numbers in the array
        dfarray[i,:] = [float(k) for k in text[line]]
    soluteoutdf = pd.DataFrame(data=dfarray, columns=mypars)
    return soluteoutdf