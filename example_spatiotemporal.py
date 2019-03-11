# -*- coding: utf-8 -*-
"""
@author: Pascal Raux
Various functions for spatio-temporal diagrams ("reslice")
"""
import numpy as np  # calcul matriciel et scientifique
import matplotlib.pyplot as plt  # figure and graphs
import skimage
from math import pi
import skimage.io, skimage.draw


#%% Movie spatio-temporal diagrams ("reslice")
"""
# reslice takes an image sequence and 2 coordinates to return a reslice
# i.e. an image showing the time-evolution of the line [x[0],y[0]],[x[1],y[1]]
dilatet = int (default= 1) sets the number of px displayed for each frame
"""
def reslice(imgseq,xslice,yslice, dilatet=1):
    # rounds and converts to an integer
    xslice, yslice = np.rint(xslice).astype(int), np.rint(yslice).astype(int)
    # determines the px to extract from each image: indline=(iy,ix)
    indline = skimage.draw.line(yslice[0], xslice[0], yslice[1], xslice[1])
    if len(imgseq[0].shape) ==2: #B&W img
        resliceimg = np.zeros((len(imgseq)*dilatet, len(indline[0])), dtype='uint8')
    else: # color img
        resliceimg = np.zeros((len(imgseq)*dilatet, len(indline[0]),
                               imgseq[0].shape[2]), dtype='uint8')
    for kimg in range(len(imgseq)):
        # extracts the line in each image of imgseq
        resliceimg[kimg*dilatet:(kimg+1)*dilatet, :] = imgseq[kimg][indline]

    return resliceimg

"""
display some images of the sequence then calls for "reslice" after defining x/yslice with ginput

- display to define a list of the img to average to generate the image displayed
        by default displays [0, len(imgseq)/2 , len(imgseq)] in an RGB img
        will display an RGB image for gray level images if len(displayimg)==3
        otherwise, will average on this list of images
- nfig is the figure number to display the img
- dilatet allow to expand the time scale by duplicating the corresponding lines

"""

def resliceinput(imgseq, dilatet=1, nfig=1, display=[]):
    if display==[]: # start middle and end of the sequence
        display = np.array([0, len(imgseq)/2 , len(imgseq)-1])

    img=np.zeros(imgseq[0].shape)
    if len(img.shape)==2 and len(display)==3:# we can make an RGB image
        img=np.zeros((img.shape[0],img.shape[1],3)) # initialize RGB img
        for k in range(3):
            img[:,:,k] = imgseq[display[k]]
        img = 255-img # invert the image to keep the background identical
    else: # averaging the images in displayimg
        for k in display:
            img = img+imgseq[k]
        img = img/len(display)

    # creates a figure with adapted shape
    plt.close(nfig)
    fig = plt.figure(nfig, figsize=(8*img.shape[1]/float(img.shape[0]),8))

    ax = fig.add_subplot(111)
    ax.imshow(img) # display image
    print('Click on the boundaries of the reslice line on figure '+ str(nfig)+
          ' (right click to cancel)')
    ax.set_title('Click on the boundaries of the reslice line (right click to cancel)')
    fig.show()
    # get user input for coords:
    coords = plt.ginput(2, timeout=0)
    # extract coordinates:
    xslice = [coords[0][0], coords[1][0]]
    yslice = [coords[0][1], coords[1][1]]

    ax.plot(xslice,yslice,'.-r')
    return reslice(imgseq,xslice,yslice,dilatet=dilatet), [xslice,yslice]


"""
reslice_rot calculate the radial profile for each image around a given center
and averages it along the angles in order to extract only one line/image
Return an spatiotemporal image of radius vs time

imseq is a concatenated imageseq: see skimage.io.concatenate_images(image_collection)

parameters:
- Nangle sets the number of angle to calculate
- color BGcolor defines the background to fill the result image
- startangle define the origin of the first line (default = top)
- radiusimage = True returns the radius vs angle image seq instead
- fullcircle = True allow to calculate radius where only part of the circle is visible
 ( = False restricts the calculation below the distance of the center to a lateral side of the image)
NB
 - in this function, the limiting size is set by the x size of the image
 - typical Nangle needed to extract the px at the edge= im.shape[0]/(2*np.arcsin(im.shape[0]*1./im.shape[1]))*2*pi

 - suggested pre-treatment of the image seq for impact of drops:
# concatenate image sequence:
imageseq=skimage.io.concatenate_images(imseq[1:])
# substract background: (in abs value):
imageseq = np.where(imseq[0]>imageseq[:], imseq[0]-imageseq[:], imageseq[:]-imseq[0])
# remove irrelevent values (noise) (threshold = 8?)
imageseq[imageseq < threshold] = 1
"""
def reslice_rot(imageseq, xcenter, ycenter, Nangle = 10*360 , BGcolor=0, startangle=-pi/2, radiusimage=False, fullcircle=True):
    # rounds and converts to an integer
    xcenter, ycenter = np.rint(xcenter).astype(int), np.rint(ycenter).astype(int)
    # image dimensions
    tmax, ymax, xmax = imageseq.shape
    if ymax > xmax:
        print('In reslice_rot: y dimension larger than x dimension. Transposed for calculation: untested, verify the result')
        return reslice_rot(np.transpose(imageseq, axes=[0,2,1]),
                           xcenter, ycenter,
                           Nangle = Nangle , BGcolor=BGcolor,
                           startangle=startangle-pi/2,
                           radiusimage=radiusimage, fullcircle=fullcircle)

    # max distance in radius (ASSUMING THAT X is the relevent axis)
    if not(fullcircle):# allows to calculate radius beyond the distance of the center to the lateral side of the image
        dmax = np.amax([xmax-xcenter, xcenter])-1
    else:
        dmax = np.amin([xmax-xcenter, xcenter])-1
    # initialisation (useless)
#    reslice = np.ones((tmax-1,dmax+1))*BGcolor
#    radiusseq = np.ones((tmax-1,Nangle,dmax+1))*BGcolor

    # initialize line vectors so that they will be negative if unasigned:
    xlines = - np.ones((Nangle,dmax+1)).astype(int)
    ylines = - np.ones((Nangle,dmax+1)).astype(int)

    # construct the lines of coordinates to extract px from each angle:
    for kangle in range(Nangle):
        angle = kangle*2.*pi/Nangle + startangle
# set the radius to test if we are in the direction of the upper/lower edges of the image
        if not(fullcircle):
        # the distance depends on which side of the image we are
            if np.cos(angle)<0:
                dtest = xcenter-1 #left side
            else:
                dtest = xmax-xcenter-1 # right side
        else:
        # only one distance as dmax is never bigger than the distance from edge
            dtest = dmax

        # upper edge
        if ycenter + dtest*np.sin(angle) >= ymax-1:
            yend = ymax-1
#            if np.cos(kangle*2*pi/Nangle)>0:
            xend = np.floor(xcenter + (yend-ycenter)/np.tan(angle)).astype(int)
        # lower edge of the image
        elif ycenter +  dtest*np.sin(angle) <= 0 :
            yend = 0
            xend = np.floor(xcenter + (yend-ycenter)/np.tan(angle)).astype(int)
# TDL: add similar conditions in x if the image is not elongated along x direction?
# pb in previous attempt: need to evaluate simultaneously the conditions on x and y... > use "np.where" instead of "if"?
        # inside the image follow a circle with max radius possible
        else:
            xend = np.floor(xcenter + dtest*np.cos(angle)).astype(int)
            yend = np.floor(ycenter + dtest*np.sin(angle)).astype(int)

        # determine which px to extract
        coords = skimage.draw.line(ycenter, xcenter, yend, xend)
        # scale using the total distance of the line
        nline = np.floor(np.sqrt((xend-xcenter)**2+(yend-ycenter)**2)).astype(int)
        # coordinates of each line
        ylines[kangle,0:nline] = coords[0][(len(coords[0])*np.arange(nline))/nline]
        xlines[kangle,0:nline] = coords[1][(len(coords[0])*np.arange(nline))/nline]
    # generate the image sequence of the "radial images" (radius,angle)
    radialseq= np.where(ylines>=0,imageseq[:,ylines,xlines],BGcolor)
    # exit and provide this matrix if radiusimage== True
    if radiusimage:
        return radialseq

    # else, average it along the angular dimension:
    # sum of relevent elements
    reslice = np.sum(np.where(radialseq!=BGcolor,radialseq,0),axis=1).astype(float)
    # number of relevent elements as a matrix with the same size:
    nb = np.matmul(np.ones(tmax).reshape((tmax,1)),
                   ((ylines>=0).sum(0)).reshape((1,dmax+1)))
    # return the average:
    return reslice/nb
"""
radiusimage return an image showing the radial evolution around a given center
in the new image, each row corresponds to an angle, and the column are radii

parameters:
- Nangle sets the number of angle to calculate
- dilate allows to duplicate each angle line for better visualization
- color BGcolor defines the background to fill the result image
- startangle define the origin of the first line (default = top)

NB
 - in this function, the limiting size is set by the x size of the image
 - typical Nangle needed to extract the px at the edge= im.shape[0]/(2*np.arcsin(im.shape[0]*1./im.shape[1]))*2*pi
"""
def radiusimage(im, xcenter, ycenter, Nangle = 10*360 , dilate=1, BGcolor=0, startangle = -90, ):
    # rounds and converts to an integer
    xcenter, ycenter = np.rint(xcenter).astype(int), np.rint(ycenter).astype(int)
    # from image dimensions
    ymax, xmax = im.shape
    if ymax > xmax: print('Error: y dimension larger than x dimension. Call the function with transpose(im)')
    # max distance in the final image
    dmax = np.amin([xmax-xcenter, xcenter])-1
#    result = np.ones((Nangle*dilate,dmax+1), dtype='uint8')*BGcolor

    # initialize line vectors so that they will be negative if unasigned:
    xlines = - np.ones((Nangle,dmax+1)).astype(int)
    ylines = - np.ones((Nangle,dmax+1)).astype(int)

    # extract the px from each angle:
    for kangle in range(Nangle):
        angle = kangle*2.*pi/Nangle + startangle*pi/180

        # upper edge
        if ycenter + dmax*np.sin(angle) >= ymax-1:
            yend = ymax-1
#            if np.cos(kangle*2*pi/Nangle)>0:
            xend = np.floor(xcenter + (yend-ycenter)/np.tan(angle)).astype(int)
        # lower edge of the image
        elif ycenter +  dmax*np.sin(angle) <= 0 :
            yend = 0
            xend = np.floor(xcenter + (yend-ycenter)/np.tan(angle)).astype(int)
# TDL :add similar conditions in x if the image is not elongated along x direction
        # inside the image follow a circle with max radius possible
        else:
            xend = np.floor(xcenter + dmax*np.cos(angle)).astype(int)
            yend = np.floor(ycenter + dmax*np.sin(angle)).astype(int)

        # determine which px to extract
        coords = skimage.draw.line(ycenter, xcenter, yend, xend)
        # scale using the total distance of the line
        nline = np.floor(np.sqrt((xend-xcenter)**2+(yend-ycenter)**2)).astype(int)
        # coordinates of each line
        ylines[kangle,0:nline] = coords[0][(len(coords[0])*np.arange(nline))/nline]
        xlines[kangle,0:nline] = coords[1][(len(coords[0])*np.arange(nline))/nline]
    # generate the image sequence of the "radial images" (radius,angle)
    return np.where(ylines>=0,im[ylines,xlines],BGcolor)

#%% example 0 diagonal:
path = './example_spatiotemporal-img/'
# get an image sequence
imgseq = skimage.io.imread_collection(path+"/diago*.tif")
plt.close()
fig = plt.figure(figsize=(15,5))
a1 = fig.add_subplot(131)
a2 = fig.add_subplot(132)
a3 = fig.add_subplot(133)

#generate a color image to display the sequence:
sequence = 255*np.ones((imgseq[0].shape[0],imgseq[0].shape[1],3)).astype('uint8')
nimg=len(imgseq)
for k in range(nimg):
    sequence[:,:,0] = np.where(imgseq[k]<100, int((255*k)/nimg),sequence[:,:,0])
    sequence[:,:,1] = np.where(imgseq[k]<100, 0, sequence[:,:,1])
    sequence[:,:,2] = np.where(imgseq[k]<100, 255-int((255*k)/nimg),sequence[:,:,2])


# display an image:
a1.imshow(imgseq[len(imgseq)/2], cmap= 'gray')
xslice = [0, 49]
yslice = [0,49]
# show the line along which the spatiotemporal is done
a1.plot(xslice,yslice,':k')
a1.set_title('image n.'+str(len(imgseq)/2))

# show colored sequence
a2.imshow(sequence)
a2.set_title('time increases from blue to red')
a2.plot(xslice,yslice,':k')

# generates the spatiotemporal diagram
spatiotemporal = reslice(imgseq,xslice,yslice, dilatet=1)
a3.imshow(spatiotemporal, cmap='gray')
a3.set_xlabel('spatial (along diagonal) (px)')
a3.set_ylabel('time (frame)')
a3.set_title('spatiotemporal')


#%% image sequence for the next examples
path = './example_spatiotemporal-img/'
# get an image sequence
imgseq = skimage.io.imread_collection(path+"/img*.tif")

#%% example 1: direct spatio temporal:
plt.close()
fig = plt.figure(figsize=(15,5))
a1 = fig.add_subplot(131)
a2 = fig.add_subplot(132)
a3 = fig.add_subplot(133)
# display an image:
a1.imshow(imgseq[len(imgseq)/2], cmap= 'gray')
xslice = [50, 450]
yslice = [250,250]
# show the line along which the spatiotemporal is done
a1.plot(xslice,yslice,'.-g')
a1.set_title('image n.'+str(len(imgseq)/2))
# generates the spatiotemporal diagram
spatiotemporal = reslice(imgseq,xslice,yslice, dilatet=1)
a2.imshow(spatiotemporal, cmap='gray')
a2.set_xlabel('spatial (px)')
a2.set_ylabel('time (frame)')
a2.set_title('spatiotemporal')

# generates the spatiotemporal diagram with dilated time
spatiotemporaldilated = reslice(imgseq,xslice,yslice, dilatet=7)
a3.imshow(spatiotemporaldilated, cmap='gray')
a3.set_xlabel('spatial (px)')
a3.set_ylabel('time (frame*dilatet)')
a3.set_title('spatiotemporal dilated')

#%% example 2: resliceinput : ask the user for boundaries of the line
plt.close()

# will ask for the boundary throught plt.ginput:
spatiotemporal, line = resliceinput(imgseq, display=[5,10,20])
# returns the diagrams and the bounds used

fig = plt.figure(figsize=(10,5))
a1 = fig.add_subplot(121)
a2 = fig.add_subplot(122)

# display an image:
a1.imshow(imgseq[len(imgseq)/2], cmap= 'gray')
a1.plot()
# show the line along which the spatiotemporal is done
a1.plot(line[0],line[1],'.-r')
a1.set_title('image n.'+str(len(imgseq)/2))

a2.imshow(spatiotemporal, cmap='gray')
a2.set_xlabel('spatial (px)')
a2.set_ylabel('time (frame)')

#%% example3: reslicerot : generates a radial spatiotemporal
plt.close()
plt.close()

# a concatenated imagesequence is needed:
# concatenate image sequence:
imageseq=skimage.io.concatenate_images(imgseq[1:])
# for clearer result, we can do some pre-processing:
# substract background, here, first image (in abs value):
imageseq = np.where(imgseq[0]>imageseq[:], #determine the sign of the difference
                    imgseq[0]-imageseq[:], # then
                    imageseq[:]-imgseq[0]) # else
# remove irrelevent values (noise) (here, threshold = 8)
imageseq[imageseq < 8] = 1

# determinates the center coordinates (black circle)
center = np.where(imgseq[0]<50)# returns a tuple (y,x)
xcenter,ycenter = np.mean(center[1]),np.mean(center[0])

# creates a radial reslice from this center:
spatiotemporal = reslice_rot(imageseq, xcenter, ycenter)

# angle evolution:
radial = radiusimage(imageseq[20,:,:], xcenter, ycenter)
# alternative method:
# get the reslices along each angle
#allradial = reslice_rot(imageseq, xcenter, ycenter, radiusimage=True)
#radial = allradial[20,:,:]


fig = plt.figure(figsize=(12,5))
a1 = fig.add_subplot(131)
a2 = fig.add_subplot(132)
a3 = fig.add_subplot(133)


a1.imshow(imageseq[20,:,:], cmap='gray')
a1.set_title('image n.20')
a1.plot(xcenter,ycenter,'.r')
#
a2.imshow(spatiotemporal, cmap='gray')
a2.set_xlabel('radius (px)')
a2.set_ylabel('time (frame)')
a2.set_title('radial spatiotemporal')

a3.imshow(radial[0:-1:10], cmap='gray')
a3.set_title('radial evolution on image n.20')
a3.set_xlabel('radius (px)')
a3.set_ylabel('angle ($^\circ$)')
