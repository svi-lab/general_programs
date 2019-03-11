# -*- coding: utf-8 -*-
import numpy as np
"""
Created on Thu Feb 08 09:59:53 2018

@author: Pascal Raux

quicksave generates a formated str array from a list of variables and
        saves this array inside a txt file (one column for each variable)
each variable in the array must be a one dimensional vector, of the same size
    variables = [var1,var2,var3,var4,etc...] is an array of variables (each one is a list)
    header=str, or list of str allow to add custom headers to the file
    nosave allow to skip the saving in order to recover only the str array generated
    column = False allow to create line arranged variable instead of column arranged variables
    colwidth is the width of each column (without the delimiter)
    floatfmt sets precision and format for float numbers as collength+fmt (default='16.5g')
    alignment define how to aligne the variables ('<' left, '>' right or '^' center)

for format details see https://pyformat.info/ or https://docs.python.org/3/library/string.html#string-formatting
"""
def quicksave(variables, name='quicksave_TEMP', root='./', header=[], nosave=False, column=True,
             colwidth=16, alignment='<', floatfmt='.5g', signed=' ', # format options
             delimiter='\t'): # np.savetxt options
    # define saving path:
    if name[-4:]=='.txt': name=root+name
    else: name=root+name+'.txt'

    # determine data type:
    datatype=[]
    for variable in variables:
        datatype.append(type(variable[0]))
#    # initialize format for each variable
    formatstr = []
    for k, dtype in enumerate(datatype):
        if np.issubdtype(dtype,str):
            formatstr.append('{:'+alignment+str(colwidth)+'}')
        elif np.issubdtype(dtype, int):
            formatstr.append('{:'+alignment+signed+str(colwidth)+'d}') # ' ' signed, ie: ' ' for positive, '-' for negative
        elif np.issubdtype(dtype, float):
            formatstr.append('{:'+alignment+signed+str(colwidth)+floatfmt+'}')
        else:
            print("data type unsuported in quicksave: "+str(dtype)+
            " in variable nb "+str(k)+"... -> replaced by float")
            datatype[k] = float
            formatstr.append('{:'+alignment+str(colwidth)+'}')

    # define header if not given by user:
    if not header:
        headerstr=''
        for k, dtype in enumerate(datatype):
            headerfmt = '{:'+alignment+str(colwidth)+'}'
            headerstr=headerstr+headerfmt.format(str(dtype)[6:-1]+' #'+str(k))+delimiter+' '
#    elif type(header)==str: # if str, header is kept as defined by the user

    elif type(header)==list: # expecting an array of str
        headerstr=''
        for string in header:
            headerfmt = '{:'+alignment+str(colwidth)+'}'
            headerstr=headerstr+headerfmt.format(string)+delimiter+' '
    else:
        headerstr=header

    # initialize data array
    savedata=np.empty((len(variables[0]),len(variables)), dtype='S'+str(colwidth))
    for i, var in enumerate(variables):# assign each variable
           for k in range(len(var)):
               savedata[k,i] = formatstr[i].format(var[k])

    if not column:
        savedata = savedata.swapaxes(0,1) #linewise array

    # save as string:
    if not nosave:
        np.savetxt(name, savedata, fmt='%s', delimiter=delimiter,
                header= headerstr)
    else:
        return savedata


#%% example 1: basics
#data:
a,b,c,d = np.arange(1,4), np.arange(11,14), np.arange(21,24), np.arange(31,34)
#save it:
quicksave([a,b,c,d])
#returns the following table: (default is in ./quicksave_TEMP.txt)
# 'numpy.int32' #0	 'numpy.int32' #1	 'numpy.int32' #2	 'numpy.int32' #3
# 1               	 11             	 21             	 31
# 2                 	 12             	 22             	 32
# 3                 	 13             	 23             	 33


# NB : for this simple task (always the same type of data), a simpler method is to use swapaxes:
#a,b,c,d = np.arange(1,4), np.arange(11,14), np.arange(21,24), np.arange(31,34)
#savedata=[a,b,c,d] # in lines
#savedata= np.swapaxes(savedata,0,1) # swap to columns
#np.savetxt(root+name,savedata, fmt='%-16s', delimiter='\t')
#%% example 2: various types
#data:
a= ['pommes', 'bananes', 'oranges']
b= [10, 20, 30]
c = [4.5, 2.5e2, 42]
#save it:
quicksave([a,b,c], header=['fruit','number (%)','price ($)'])
#returns the following table in ./quicksave_TEMP.txt:
## fruit name      	 number (%)      	 price ($)
#pommes             	 10             	 4.5
#bananes          	 20             	 250
#oranges          	 30             	 42
#%% example 3: change format
#save it:
quicksave([a,b,c], header=['fruit','nb (%)','price ($)'], alignment='^', colwidth=9)
# returns a centered table:
##   fruit  	  nb (%)  	 price ($)
#  pommes  	    1    	   4.5
#  bananes 	    2    	   250
#  oranges 	    3    	   -42
#

# recover the corresponding str array:
abc = quicksave([a,b,c], nosave=True, alignment='^', colwidth=9)
abc

#%% example 4: line display
a= ['pommes', 'bananes', 'oranges']
b= [1, 2, 3]
c = [4.5, 2.5e2, -42]


abc = quicksave([a,b,c], name='quicksave_myfavoritename', column=False, nosave = True, header='in lines: a then b and c')
#returns the following table in ./quicksave_myfavoritename.txt, with a line display:
## in line: a then b and c
#pommes          	 1              	 4.5
#bananes         	 2              	 250
#oranges         	 3              	-42


