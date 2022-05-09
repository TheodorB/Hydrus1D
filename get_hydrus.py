#!/home/theodor/anaconda3/bin/python
"""
Created on Tue Jan 26 09:35:03 2016

@author: theodor
"""
import numpy as np
import pandas as pd
import os
import re
import subprocess

#import time

class hydrus_handler:
    '''
    A bunch of hydrus inpu/output/run functions
    '''
    def __init__(self, run_path, exe_folder='default', change_dir=True, suppress_printing=True):
        self.run_path = run_path
        if exe_folder == 'default':
            self.exe_folder = '/home/theodor/Documents/hydrus/'
        else:
            self.exe_folder = exe_folder
        self.change_dir = change_dir
        self.suppress_printing = suppress_printing
    def run_hydrus(self):
        '''
        running h1d_calc like from terminal
        '''
        run_path = os.path.join(self.run_path)
#        with open('/home/theodor/hydrus/build/LEVEL_01.DIR','w') as f: # for compiled fortran codes
        # if self.exe_folder == 'default':
        #     with open('/home/theodor/Documents/hydrus/LEVEL_01.DIR','w') as f:
        #         f.write(run_path)

        # elif self.exe_folder != 'default' and self.change_dir:
        with open('{}/LEVEL_01.DIR'.format(self.exe_folder),'w') as f:
            f.write(run_path)
        # else:
        #     pass

#        for (path,dirs,files) in os.walk(run_path): # this is sometimes needed and sometimes not. dependent on hydrus1D, I guess
#            for fi in files:
#                if fi=='PROFILE.DAT':
#                    os.rename(os.path.join(run_path,fi),os.path.join(run_path,'Profile.dat'))
#                elif fi=='HYDRUS1D.DAT':
#                    os.rename(os.path.join(run_path,fi),os.path.join(run_path,'Hydrus1d.dat'))
#                elif fi=='SELECTOR.IN':
#                    os.rename(os.path.join(run_path,fi),os.path.join(run_path,'Selector.in'))
#                else:
#                    pass
#        tic = time.time()

        #### added >/dev/null 2>&1 & for supressing the printing of the run1
        # if self.exe_folder == 'default':
        #     # cmd = os.system("cd  /home/theodor/Documents/hydrus ;wine H1D_CALC.EXE  >/dev/null 2>&1 &")
        #     cmd = "cd  /home/theodor/Documents/hydrus ;wine H1D_CALC.EXE"
        # else:
        #     # cmd = os.system("cd  {} ;wine H1D_CALC.EXE  >/dev/null 2>&1 &".format(self.exe_folder))
        cmd = "cd  {} ;wine H1D_CALC.EXE".format(self.exe_folder)
        # os.system("cd '/home/theodor/hydrus/build';./h1d_calc") # for compiled fortran codes
#        toc = time.time()
#        os.system("echo 'HYDRUS SIMULATION IS DONE (in {} [sec])'".format((toc-tic)))
  # EXECUTE AND WAIT
        
          
        if self.suppress_printing:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            #This makes the wait possible
            p_status = p.wait()
        else:
            os.system("cd  {} ;wine H1D_CALC.EXE".format(self.exe_folder))
        
        return  

    def  get_hydrus_dat(self):
        '''
        Hydrus1d.dat
        return a dict with keys = parameters
        '''
        htext = dict() # dictionary with text file data by row
        try:
            with open(os.path.join(self.run_path,'Hydrus1d.dat'),'r') as f:
                for i, line in enumerate(f):
                    htext[i] = line.split()
        except:
            with open(os.path.join(self.run_path,'HYDRUS1D.DAT'),'r') as f:
                for i, line in enumerate(f):
                    htext[i] = line.split()            
        hdict = dict() # hydrus_dat dict
        for l in htext.items():
            a =  l[1][0].split('=')
            if len(a) == 2:
                hdict[a[0]] = (a[1])
                if a[0] not in ['SpaceUnit','TimeUnit']:
                    hdict[a[0]] = float(hdict[a[0]])
        return hdict

    def get_node_out(self):
        '''
        create a dict time:df
        '''
        run_path = os.path.join(self.run_path)
        for (path,dirs,files) in os.walk(run_path):
            for fi in files:
                if fi=='Nod_Inf.out':
                    os.rename(os.path.join(run_path,fi),os.path.join(run_path,'NOD_INF.OUT'))

        text = dict() # dictionary with text file data by row
        with open(os.path.join(self.run_path, 'NOD_INF.OUT'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
        start_row  =   10
        mypars      = text[start_row][1:] # parameters for column names  of dataframe
        if len(text[start_row]) == len(text[start_row+3]) - 2: # in case of 2 solutes
            extention = [mypars[-2], mypars[-2].replace('1', '2'), mypars[-1], mypars[-1].replace('1', '2')]
            mypars = mypars[:-2]
            mypars.extend(extention)
#        print(text.items())
#        print([val[1][1] for val in text.items() if (('Time:' in val[1]) and('Date' not in val[1]))])
        print_times = [val[1][1] for val in text.items() if 'Time:' in val[1]][1:]
        print_times = [float(var) for var in print_times]
        start_rows  = [val[0]+6 for val in text.items() if 'Time:' in val[1]][1:] # drop first 'Time' (the header one)
        end_rows    = [val[0] for val in text.items() if 'end' in val[1] ]

        mydata = dict() # dict of keys=time, values=dataframes
        for n,t in enumerate(print_times):            # n is the number of the data frame created
            dfarray = np.empty((end_rows[n] - start_rows[n], len(mypars)))
            lines = list(range(start_rows[n],end_rows[n]))
            for i in range(len(lines)):              # i are serial row numbers in the array
                dfarray[i,:] = [float(k) for k in text[lines[i]][1:]]
            mydata[t] = pd.DataFrame(data=dfarray, columns=mypars)
        return mydata

    def get_t_level_out(self):
        '''
        returns dataframe
        '''
        run_path = os.path.join(self.run_path)
        for (path,dirs,files) in os.walk(run_path):
            for fi in files:
                if fi=='T_Level.out':
                    os.rename(os.path.join(run_path,fi),os.path.join(run_path,'T_LEVEL.OUT'))
        text = dict() # dictionary with text file data by row
        with open(os.path.join(self.run_path, 'T_LEVEL.OUT'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
        par_row, start_row = 6, 9 # 5,8 on linux compiled fortran codes
        mypars = text[par_row] # parameters for column names  of dataframe
        end_row   = [val[0] for val in text.items() if 'end' in val[1]][0]

        dfarray = np.empty(shape=(end_row - start_row, len(mypars)))
        lines = list(range(start_row, end_row))

        for i,line in enumerate(lines):              # i are serial row numbers in the array
            dfarray[i,:] = [float(k) for k in text[line]]
        levdf = pd.DataFrame(data=dfarray, columns=mypars)
        return levdf

    def get_obs_node_out(self):
        try:
            # maybe no obs nodes?
            run_path = os.path.join(self.run_path)
            for (path,dirs,files) in os.walk(run_path):
                for fi in files:
                    if fi=='Obs_Node.out':
                        os.rename(os.path.join(run_path,fi),os.path.join(run_path,'OBS_NODE.OUT'))
            #TODO - run  'get_node_out' before to get mydata dictionary
            mydata = self.get_node_out()
            text = dict() # dictionary with text file data by row
            with open(os.path.join(self.run_path, 'OBS_NODE.OUT'),'r') as f:
                for i, line in enumerate(f):
                    text[i] = line.split()
            node_list =  [p.split() for p in text[8]]
        #     get node numbers and depths!
            while ['Node('] in node_list:
                node_list.remove(['Node('])
    
            node_list = [int(re.findall('\d+',l[0])[0]) for l in node_list]
    #        print (mydata)
            depths = [list(mydata.values())[0].iloc[node-1]['Depth'] for node in node_list]
            start_row  =   11 #10  on linux compiled fortran codes
            mypars = text[start_row - 1] # parameters for column names  of dataframe
            end_row   = [val[0] for val in text.items() if 'end' in val[1]][0]
    
            dfarray = np.empty(shape=(end_row - start_row, len(mypars)))
            lines = list(range(start_row, end_row))
    
            for i,line in enumerate(lines):              # i are serial row numbers in the array
                dfarray[i,:] = [float(k) for k in text[line]]
            obsdf = pd.DataFrame(data=dfarray, columns=mypars)
            # split to node dataframes in dict
            obsdict = dict()
            length = len(obsdf.columns)
            Lcolumns = list(obsdf.columns) # list of column names
            try:
                ind = Lcolumns.index('Conc')
                if Lcolumns[ind + 1:].index('Conc') == 0: # if two solutes
                    while 'Conc' in Lcolumns:
                        ind = Lcolumns.index('Conc')
                        Lcolumns[ind] = 'Conc1'
                        Lcolumns[ind+1] = 'Conc2'
                    obsdf.columns = Lcolumns
            except:
                print('no solute')
            params_len = len(set(obsdf.columns[1:])) # how many parameters
            for i, n in enumerate(range(1,length,len(set(obsdf.columns[1:])))):
                obsdict[depths[i]] = obsdf.iloc[:,np.concatenate((np.array([0]), np.array(  list(range(n,n+params_len))  )))]
            return obsdict
        except:
            print('no obs nodes or something!')
            return {}

    def get_profile_out(self):
        '''
        get PROFILE.OUT DataFrame
        '''
        text = dict() # dictionary with text file data by row
        with open(os.path.join(self.run_path, 'PROFILE.OUT'),'r') as f:
            for i, line in enumerate(f):
                text[i] = line.split()
        # text
        mypars = text[6] # parameters for column names  of dataframe
        start_row  = 8
        end_row   = [val[0] for val in text.items() if 'end' in val[1]][0]
        dfarray = np.empty(shape=(end_row - start_row, len(mypars)))
        lines = list(range(start_row, end_row))

        for i,line in enumerate(lines):              # i are serial row numbers in the array
            dfarray[i,:] = [float(k) for k in text[line]]
        profoutdf = pd.DataFrame(data=dfarray, columns=mypars)
        return profoutdf

    def get_profile_dat(self):
        '''
        get text dict and DataFrame of profile
        '''
        textpd = dict() # dictionary with text file data by row , textpd =text of profile.dat
        try:
            with open(os.path.join(self.run_path, 'Profile.dat'),'r') as f:
                for i, line in enumerate(f):
                    textpd[i] = line.split()
        except:
            with open(os.path.join(self.run_path, 'PROFILE.DAT'),'r') as f:
                for i, line in enumerate(f):
                    textpd[i] = line.split()            
        myint = 4 # integer of line number   # this can change. 4 if "Pcp_File_Version=4" in first row
        n_nodes = int(textpd[myint][0])
        start_row  = 5    # this can change. 5 if "Pcp_File_Version=4" in first row
        end_row   = start_row + n_nodes
        num_pars = len(textpd[start_row+1])
        mypars = textpd[myint][3:] # parameters for column names  of dataframe
        if len(mypars) == len(textpd[start_row]) - 1: # in case of 2 solutes
            extention = ['Conc1', 'Conc2']
            mypars = mypars[:-1]
            textpd[myint] = textpd[myint][:-1]
            mypars.extend(extention)
            textpd[myint].extend(extention)
        dfarray = np.empty(shape=(end_row - start_row, num_pars))
        lines = list(range(start_row, end_row))
        for i,line in enumerate(lines):              # i are serial row numbers in the array
#            print textpd[line]
            dfarray[i,:] = [float(k) for k in textpd[line][:num_pars] ]
        df = pd.DataFrame(data=dfarray, columns=mypars[:num_pars])
        return df, textpd