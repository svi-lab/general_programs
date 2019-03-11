# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 2018 @author: Pascal Raux

This function creates another axis to show some values given by an arbitray function
 - the transform must be given as convert(new_coordinates) = parent_coordinates
 - by default creates another xaxis, otherwise will create a yaxis
 - the range of the new axis is given by newrange (will automatically rescale the parent ax to match)
 - ticks= "array of values" allows to define the values to display
 - minor= 10 allows to create minor ticks with a specified division scale (e.g. here 10 minor ticks/ tick)

NB: - Note that convert gives the former coordinates from the new ones
        (you will need to reverse your function if you have the opposite)
    - the function only generates the ticks:
      To plot data, you still need to use convert(yourdata)
      only use the returned ID to modify the appearance of the ax, not to plot..
      (values does not correspond to values displayed, but to the parent axis)
    - you may need to extend the space around the figure or use plt.tight_layout()
    - minor displays linearly spaced minorticks (unless minlog=True, in this case geometrical scale (as in log scale))
"""

import numpy as np
import matplotlib.pyplot as plt


def doubleaxis(parentID, convert, newrange, xaxis=True, ticks= False, minor=0, minlog=False, label= ' '):
    # to make sure we are able to convert arrays, modify the convert function:
    def npconvert(x): return convert(np.array(x))
    newrange, ticks = np.array(newrange), np.array(ticks)

    if xaxis: # duplicates the x axis
        # creates a fake axis to show the correct ticks:
        axisID = parentID.twiny()

        # make sure the two axes are matched to get auto ticks
        parentID.set_xlim(npconvert(newrange))
        axisID.set_xlim(newrange)
        if ticks.any():
            MajTicks=ticks
        else:
            # get the needed ticks automatically from the generated figure
            MajTicks = axisID.get_xticks()
    else:
#NB: This is the same script but on y axis. There must be a more elegant way to
#  switch between the two. Let me know if you know how to avoid this repetition
         # creates a fake axis to show the correct ticks:
        axisID = parentID.twinx()
        # make sure the two axes are matched
        parentID.set_ylim(npconvert(newrange))
        axisID.set_ylim(newrange)
        if ticks.any():
            MajTicks=ticks
        else:
            # get the needed ticks automatically from the generated axis
            MajTicks = axisID.get_yticks()

    # creating minor ticks if needed:
    MinTicks = np.array([])
    if minor: # builds minor tick as a division of major ticks:
        for t in range(len(MajTicks)-1):# creates "minor" divisions in each interval
            if minlog:  # log-space ticks
                MinTicks=np.append(MinTicks, MajTicks[t]*np.arange(1,minor)*\
                               (MajTicks[t+1]/MajTicks[t])/float(minor))
            else: # linearly spaced ticks
                MinTicks=np.append(MinTicks, MajTicks[t] + np.arange(1,minor)* \
                               (MajTicks[t+1]-MajTicks[t])/float(minor))
    # restrain the ticks to the used ranged
    MajTicks=MajTicks[np.logical_and(MajTicks>=np.min(newrange), MajTicks<=np.max(newrange))]
    MinTicks=MinTicks[np.logical_and(MinTicks>=np.min(newrange), MinTicks<=np.max(newrange))]

    # converting ticks coordinates in parent axis units:
    newTicks = npconvert(MajTicks)
    newMinTicks = npconvert(MinTicks)
    if xaxis: # adjust the values of ticks in the new axis:
        # the new ax is then reversed as the parent one,
        # link the two axis to make sure they always stay connected
        axisID.set_xlim(npconvert(newrange))# parent ax values
        axisID.get_shared_x_axes().join(axisID,parentID)

        # and ticks are fixed to their new value
        axisID.set_xticks(newTicks)
        axisID.set_xticks(newMinTicks, minor=True)
         # labels from the former range are kept:
        axisID.set_xticklabels(MajTicks.astype(str))
        # label the axis
        axisID.set_xlabel(label)
        axisID.xaxis.set_label_coords(.5,1.125) # adjust position
    else: # adjust the values of ticks in the new axis:
        # the new ax is then reversed as the parent one,
        # link the two axis to make sure they stay connected
        axisID.set_ylim(npconvert(newrange))# parent ax values
        axisID.get_shared_y_axes().join(axisID,parentID)
#
        # and ticks are fixed to their new value
        axisID.set_yticks(newTicks)
        axisID.set_yticks(newMinTicks, minor=True)
        # labels from the former range are kept:
        axisID.set_yticklabels(MajTicks.astype(str))
        # label the axis
        axisID.set_ylabel(label)
        axisID.yaxis.set_label_coords(1.1,.5) # adjust position
    return axisID

#%% example 1: normalized scale
plt.close()
f=plt.figure()
ax= f.add_subplot(111)

ax.plot(np.linspace(0,10),np.linspace(0,10)**2,'-k')

ax.set_xlabel('$x$ (regular axis)')
ax.set_ylabel('$y$')
# we want to display an axis with y normalized by lambda = 2
# the former coordinates are given by multiplying new coordinates by lambda
def inversefun(x): return np.array(x)*5

doubleaxis(ax,inversefun, [0,2], label='$x/\lambda$ (created axis)')

#%% example 2: non-linear scale
plt.close()
f=plt.figure()
ax = f.add_subplot(111)

# we want to display an axis with z, given as a function of y
def convertz(y): return np.exp(y)

# we need to define the inverse function of convertz to reverse z to y
def converty(z): return np.log(z) # ln(z)

ax.plot(np.linspace(0,3),np.exp(np.linspace(0,3)),'-k')
ax.set_xlabel('$x$')
ax.set_ylabel('$y$ (regular linear axis)')
ax.set_xlim([0,2.5])
newID=doubleaxis(ax,convertz, [.0,2.5], xaxis=False,ticks= np.arange(0,5.5,.5), # "ticks" to display part of the ticks only
                 label='manual log scale (new)')

yvect = np.arange(2,20,2)
ax.plot(converty(yvect),yvect,'sb')
for y in yvect: ax.plot([.05,converty(y)],y*np.ones(2),':b')
ax.set_yticks(np.arange(0,20,2))

xvect = np.arange(0,3.5,.5)
ax.plot(xvect,convertz(xvect),'or')
for x in xvect: ax.plot([x, 2.45],convertz(x)*np.ones(2),'-r')

# NB: the axis are matched even if limits of the parent ax are changed.
ax.set_ylim([0,12.5])
#newID.set_ylim([0,12.5]) #is equivalent to the previous line: it will set the PARENT axis limits
# (the values in newID do NOT correspond to its own ticks but to the parent axis)


#%% example 3: non-linear scale, minorticks
plt.close()
f = plt.figure(figsize=(12,5))
a1 = f.add_subplot(121)
a2 = f.add_subplot(122)

# we want to display an axis with z, given as a function of y
def convertz(y): return 101-np.sqrt(100*y)


# we need to define the inverse function of convertz to reverse z to y
def converty(z): return 1/100.*(101-np.array(z))**(2)

a1.plot(np.linspace(0,100),converty(np.linspace(0,100)),':k')
a2.plot(np.linspace(0,100),converty(np.linspace(0,100)),':k')
a1.set_xlim([0,100])
a2.set_xlim([0,100])
a1.set_xlabel('$x$')
a2.set_xlabel('$x$')
a1.set_ylabel('$y$ (regular linear axis)')

a1.set_title('standard')
a2.set_title("'MinorTicks' option")

# determine the limits of the new axis:
newlimits=convertz(np.array([0,100])) # if we want to keep y from 0 to 13
# creates the second axis
a1bis=doubleaxis(a1,converty, newlimits, xaxis=False, ticks=np.arange(10,101,10)) # "ticks" to display part of the ticks only
a2bis=doubleaxis(a2,converty, newlimits, xaxis=False, minor=5, ticks=np.arange(0,101,20))
a2bis.set_ylabel('$z = 11 - \sqrt{10 y}$ (new)', fontsize=14)
# NB : only use the returned ID to modify the appearance of the ax, not to plot..

yvect = np.arange(0,103,20)
a1.plot(convertz(yvect),yvect,'sb')
for y in yvect: a2.plot([5,convertz(y)],y*np.ones(2),':b')

xvect = np.arange(0,101,10)
a1.plot(xvect,converty(xvect),'or')
for x in np.arange(0,101,20): a2.plot([x, 95],converty(x)*np.ones(2),'-r', linewidth=1)
for x in np.arange(0,101,20/5.): a2.plot([x, 95],converty(x)*np.ones(2),'-r', linewidth=.3)


#%% example 4: viscosity of a suspension, "log-like" scale
plt.close()
f=plt.figure()
ax = f.add_subplot(111)

# we want to display an axis with the viscosity,
# given as a function of the concentration phi
def visc_Zarraga(phi, eta0=1, phim=.59): # Zarraga model for suspensions
             phi = np.array(phi)
             return eta0*np.exp(-2.34*phi)/(1-phi/phim)**3
# build a function that deduces the concentration from the viscosity
# this function is a bit complicated to reverse directly,
# so I used dichotomy to deduce it from viscosity(phi)
def inverse(eta, eta0=1, phim=.59, tolerance=1e-8):
    eta = np.array(eta)
    if eta.shape == (): # check if it is only a number
        eta = np.array([eta])# creates an array in this case (in order to apply the same code to single values and vectors)

    if any(eta<eta0):
        print('Viscosity cannot be lower that solvent viscosity')
        eta[np.where(eta<eta0)] = eta0

    # calculate the fraction by dichotomy:
    # initialize
    xmin = np.zeros(len(eta))
    xmax = np.ones(len(eta))*phim # max concentration
    # calculate the properties of the mixture in the middle:
    guess = visc_Zarraga((xmin+xmax)/2., eta0=eta0, phim=phim)
    while any(np.abs(guess-eta) > tolerance * eta): # dichotomy loop
        xmax[guess > eta] = (xmin[guess > eta] + xmax[guess > eta])/2.
        xmin[guess < eta] = (xmin[guess < eta] + xmax[guess < eta])/2.
        # calculate the properties of the mixture in the middle:
        guess = visc_Zarraga((xmin+xmax)/2., eta0=eta0, phim=phim)

    return (xmin+xmax)/2.

maxphi = .55
ax.plot(np.linspace(0,maxphi), visc_Zarraga(np.linspace(0,maxphi)),'-k') # dependency of the viscosity to the concentration
ax.set_xlabel('volumic fraction')
ax.set_ylabel('viscosity')

newlimits= visc_Zarraga([0,maxphi])
ax2 = doubleaxis(ax, inverse, newlimits, ticks=[1,10,100,1000], minor=10, minlog=True, label='relative viscosity')


# some physical law that depends on the viscosity we may want to plot, measured from the concentration
ax.plot(np.linspace(0,maxphi),
        800/(1+np.sqrt(visc_Zarraga(np.linspace(0,maxphi)))), ':r')
def bidon(y): return y # new y axis for this law
ay2= doubleaxis(ax, bidon, [.8,1e3],xaxis=False)


# log scale for y axis:
ax.set_yscale('log')
# to keep the two axes connected, it is necessary to also adjust the scale of ay2
ay2.set_yscale('log')

 # modify the appearance of the new axis using the returned ID
ay2.set_ylabel('duplicated yaxis in log', color='r')
ay2.yaxis.set_label_coords(1.08,.5)

# paint it red
ay2.tick_params(axis='y', colors='r', which='both')
ay2.spines['right'].set_color('r')


# verification of the values:
ay2.grid(axis='y')
ax2.grid(axis='x')

