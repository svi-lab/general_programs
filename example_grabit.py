"""
Created by Pascal Raux, inspired by a matlab GUI by Jacopo Seiwert


grabit: this function extracts points coordinates (x,y) from a picture
        (typically from a screenshot of a figure),
        requires as input an image or a path for the image
        then various inputs from the user (for calibration and to set the points)

if xscale (or yscale)=='log', will expect the limit of the axis as power of ten
                              and will return the value in linear space

darkerred = True converts the red component of the image into a darker tone
(useful if the points are bright red, to allow visualisation of ginput dots...)

WARNING the ginput function requires to use QT windows
(call it with %matplotlib qt5 and use %matplotlib inline to return to inline display)
options:
        xscale/yscale allow to set
        nfig allows to set the figure number displaying the image
        redcontrast enhance the contrast for bright reds in order to see the ginput points
"""

import numpy as np
import matplotlib.pyplot as plt  # figure and graphs
import skimage.io


def grabit(img, xlinear='True', ylinear='True', nfig=1, redcontrast=True):
    if type(img) == str: # img is a path else img is directly an image
        img = skimage.io.imread(img)
    if redcontrast:
        # for bright red px, reduce brightness to see the ginput points
        if img.shape[2]==3: # RGB image
            img[:,:,0] = np.where(np.logical_and(img[:,:,0]>50, img[:,:,1]<200), # bright reds (but doesnot modify the whites)
                                    img[:,:,0]/2, img[:,:,0])
        if img.shape[2]==4: # CMYK image

             img[:,:,1] = np.where(np.logical_and(img[:,:,1]<100, img[:,:,0]>200),# bright reds (but doesnot modify the whites)
                                    img[:,:,1]*2, img[:,:,1])
    plt.close(nfig)
    # give the figure dimensions proportional to the image:
    fig = plt.figure(nfig, figsize=(.8*9*img.shape[1]/float(img.shape[0]),9))
    ax = fig.add_axes([0,0,1,1])
    ax.imshow(img) # displays the image
    plt.axis('off') # remove the axis of the figure for clarity

    # calibration: how to convert px in the units of the figure?
    print('\t'*2+'Calibration of the scale in figure '+str(nfig)+':')

    if xlinear:
        limitstr =['xmin','xmax','ymin','ymax']
    else:
        limitstr =['log(xmin)','log(xmax)','ymin','ymax']
    if not(ylinear):
        limitstr[2:] =['log(ymin)','log(ymax)']
    ax.set_title('Axis calibration: '+str(limitstr)+' (right click to cancel)')
    print('\t'*2+'Click on each boundary of the axis: '+str(limitstr)+' (right click to cancel)')
    fig.show()
    axlimits = plt.ginput(4, timeout=0) # wait for the input of the four points
    calibrationpx = [axlimits[0][0],axlimits[1][0], axlimits[2][1], axlimits[3][1]] # relevent values
    calibration = np.zeros(4)
    ax.set_title('Axis calibration: please give the limits corresponding in the console')
    for i in range(4):
        calibration[i] = input('\t'*2+'What is the value corresponding to '
                               +limitstr[i]+'? ')
    #display these limits on the graph:
    for i in range(2):
        plt.plot(axlimits[i][0],axlimits[i][1], 'xg', markersize=10)
        plt.text(axlimits[i][0] + 5, axlimits[i][1] + 10,
                 limitstr[i]+' = '+str(calibration[i]), color='g')
    for i in range(2,4):
        plt.plot(axlimits[i][0],axlimits[i][1], 'xr', markersize=10)
        plt.text(axlimits[i][0] + 5, axlimits[i][1] - 5,
                 limitstr[i]+' = '+str(calibration[i]), color='r')
    fig.show()
    # build convertion fonctions
    def convertx(px):
        return calibration[0]+(px-calibrationpx[0])*(calibration[1]-calibration[0])/(calibrationpx[1]-calibrationpx[0])
    def converty(px):
        return calibration[3]+(px-calibrationpx[3])*(calibration[2]-calibration[3])/(calibrationpx[2]-calibrationpx[3])

    nb = int(input('\t'*2+'How many data set(s) do you want to extract? '))
    if nb ==0: nb =1 # default is 1 set
    Data = [] # list of data sets
    for i in range(nb):
        ax.set_title('Data extraction: Click on the data for the set '+str(i+1)+' (right click to cancel, enter to exit)')
        fig.show()
        print('\t'*2+'Click on the data for the set '+str(i+1)+' (right click to cancel, enter to exit)')
        datapx = np.array(plt.ginput(-1, timeout=0))
        result = np.zeros(datapx.shape)
        if xlinear:
            result[:,0] = convertx(datapx[:,0])
        else:
            result[:,0] = 10**convertx(datapx[:,0])
        if ylinear:
            result[:,1] = converty(datapx[:,1])
        else:
            result[:,1] = 10**converty(datapx[:,1])
        # plot the former data sets
        colorplot = [1,0,0] + np.array([-.95,0,1])*i/float(nb)
        ax.plot(datapx[:,0],datapx[:,1],'x',
                color=colorplot, markersize =10)
        ax.plot(datapx[:,0],datapx[:,1],'o',
                color=colorplot, mfc='none', markersize =5)
        Data.append(result)

    # output:
    if nb == 1:  return result # only 1 data set
    else: return Data # list of data sets



#%% example: extract the data in the image testgrabit(.png/.jpg)
plt.close()
root = './' # use instead the file of the example
imgpath = root+'testgrabit.jpg'
#imgpath = root+'testgrabit.png'
img =  skimage.io.imread(imgpath) # loads the image

result = grabit(imgpath) # alternatively, one can call directly grabit(img)
# first click on the 4 boundary of the axes
# then give the value corresponding to these boundaries
# choose the number of data sets you want to extract
# then click on the data points you want to extract

# NB ginput function requires qt windows. If you are currently in inline mode,
# use the commande %matplotlib qt5 (%matplotlib inline to return to inline mode)


# build a double column figure:
fig = plt.figure(figsize=(12,5))
a1 = fig.add_subplot(121)
a2 = fig.add_subplot(122)

a1.imshow(img)
a1.set_title('Image')
a1.set_axis_off() # remove the axis for clarity
# reproduce the dash line on a2 for comparison:
a2.plot(np.linspace(0.1,10),2.8/np.linspace(0.1,10),':k')
try:
    _ = result.shape # is a test on the number of data set in results (*)
    a2.plot(result[:,0],result[:,1],'ok')
# (*)will work only for 1 data set as grabit returns (x,y) in an np.array
#    will fail if result is an array of np.array corresponding to each data set
except:
    for i in range(len(result)):
        data = result[i]
        colorplot = np.array([-.9,0,1])*i/float(len(result))+[1,0,0]
        a2.plot(data[:,0],data[:,1],'o', color= colorplot)



a2.set_title('Extracted data')
a2.set_xlim([0,6])
a2.set_ylim([0,4])