# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 17:27:30 2017

@author: B7044343
"""
import numpy as np

#Built a structured array
#U7 = characters length max 7 
#f4 = float length max 4
#i5 = integer length max 2
data_save = np.zeros(6, dtype=[('var1','U8'),('var2','f4'),('var3','i2')]) 
data_save['var1'] = ["sample1", "sample2", "sample3","sample4","sample5","sample6"]
data_save['var2'] = [10.15, 11.5, 19.85, 15.3, 12.6, 17.65]
data_save['var3'] = [0, 1, 0, 1, 0, 1]


#Save data 
#for nomenclature see https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.savetxt.html#r285
np.savetxt('save_data_test.txt', data_save, fmt="%s %.2f %i") 

#/!\don't use np.loadtxt
data_loaded = np.genfromtxt('save_data_test.txt', dtype=None)

print(data_loaded[0])       #a tuple
print(data_loaded[1][1])    #a value
print(data_loaded['f1'])    #a variable (named f0, f1, etc by default)
