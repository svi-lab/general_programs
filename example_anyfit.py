# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 18:27:24 2017

@author: P1230020
"""

import numpy as np  # calcul matriciel et scientifique

import matplotlib.pyplot as plt  # figure and graphs
import scipy.optimize


'''
from a function f(x,param), and initial guess, returns the parameters that
minimize (locally) the difference with the experimental data provided
need to define function as function(x, param): return yth=f_param(x) (param can be a vector)

log= True , the fmin search is done on a log scale

NB another option is to use the function scipy.optimize.curve_fit

update 12/01/2018:
    changing the function by optimize.minimize (instead of optimize.fmin)
    adding log option
'''
def anyfit(function, datat, datay, initial_guess, log=True):
    if log:
        def delta(param): return np.log(np.sum((function(datat, param)-datay)**2)/len(datat))
    else:
        def delta(param): return np.sum((function(datat, param)-datay)**2)/len(datat)

    result = scipy.optimize.minimize(delta, initial_guess) # args=(A[i],)

    return result.x # returns the solution array

#%% example 1:
#plt.close()
# data to be fitted:
t = np.linspace(0,25, num = 100)
y = 5*np.exp(-t/6.)*np.cos(3*t+1)

# define a custom fit function f(x,param)
# where x is the variable and param the parameters
def myfun(x,param):
    return param[0]*np.exp(-x/param[1])*np.cos(param[2]*x+param[3])

# fiting, returns the coefficients in param
paramfit = anyfit(myfun,t,y,[10,10,1,1])



plt.figure()
plt.plot(t,y,'ok')
plt.plot(np.linspace(0, 25, num=200),
         myfun(np.linspace(0, 25, num=200),paramfit),'-r')
plt.text(10,3, str(np.round(paramfit, decimals=3)))






#%% example 2:
#plt.close()

# build a double column figure:
fig = plt.figure(figsize=(12,5))
a1 = fig.add_subplot(121)
a2 = fig.add_subplot(122)

# data to be fitted:
t = np.linspace(0,25, num = 100)
y = 5*np.exp(-t/6.)*np.cos(3*t+1)
#NB it is a local minimum, the starting parameters must be chosen carefully:
paramfit2 = anyfit(myfun,t,y,[10,10,10,1], log=False) # here the frequency is too high

# using a logscale for searching the minimum helps exploring a larger range of parameters
paramfit3 = anyfit(myfun,t,y,[10,10,10,1], log=True)

a1.text(10,3, str(np.round(paramfit2, decimals=1)),color= 'b')
a1.text(10,2.5, str(np.round(paramfit3, decimals=1)),color= 'g')
a1.plot(t,y,'ok')
a1.plot(np.linspace(0, 25, num=200),
         myfun(np.linspace(0, 25, num=200),paramfit2),':b')
a1.plot(np.linspace(0, 25, num=200),
         myfun(np.linspace(0, 25, num=200),paramfit3),':g')

# adding some noise
y = 5*np.exp(-t/6.)*np.cos(3*t+1)+np.random.random_sample(100)-.5

paramfit=anyfit(myfun,t,y,[5,5,5,1], log=True)

a2.plot(t,y,'ok')
a2.plot(np.linspace(0, 25, num=200),
         myfun(np.linspace(0, 25, num=200),paramfit),'-r')
a2.text(10,3, str(np.round(paramfit, decimals=1)))


