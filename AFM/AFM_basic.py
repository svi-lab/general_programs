# -*- coding: utf-8 -*-
"""
How to use pySPM librairy for AFM data
ploting, flaten, profiles

This script uses pySPM, you can download it from https://github.com/scholi/pySPM
Documentation is here https://github.com/scholi/pySPM/blob/master/doc/pySPM%20Documentation.ipynb
You have to install it for example with 'conda install [your_Package]' in anaconda prompt.
"""

import pySPM
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import os
from skimage import exposure, filters
from skimage import img_as_ubyte

"""
Exemple 1: Simple description of pySPM
           for more see the documentation
"""

#Exemple is given for Burker AFM = SVI version
filename = os.path.realpath('image_test_AFM.001')
ScanB = pySPM.Bruker(filename) 

#Print all possible channels             
ScanB.list_channels()
#choose your channel into the list printed
channel="Height Sensor"
imageSPM = ScanB.get_channel(channel=channel)

#You can plot your image
fig, ax = plt.subplots(1,2,figsize=(10,5))
imageSPM.show(ax=ax[0])
#You can flaten in lines 
image_flaten=imageSPM.correct_lines(inline=False)
image_flaten.show(ax=ax[1])
#You can plot a profil
fig, ax = plt.subplots(1,2,figsize=(10,5))
image_flaten.plot_profile(9,61,89,116,ax=ax[1],img=ax[0]);
image_flaten.show(ax=ax[0],pixels=True)
plt.tight_layout()

"""
Exemple 2: /!\Warning pySPM use a class named SPM_image
           so you CANNOT use tools for picture directly 
           but you can save your picture as a numpyarray thanks to .pixels
"""
def correct_lines_objects(im):
    """
    flaten the picture taking into acount main holes (average in lines without holes)
    input : image /!\it must be a squared image
    output : image corrected
    """
    image_correct_line = im - np.tile(np.mean(im, axis=1).T,(im.shape[0], 1)).T
    p_min = np.amin(image_correct_line)
    p_max = np.amax(image_correct_line)
    image_g = img_as_ubyte(1-(image_correct_line-p_min)/(p_max-p_min))
    im_eq = exposure.equalize_adapthist(image_g)
    seuil = filters.threshold_otsu(im_eq)
    mask = im_eq > seuil+0.05
    imx = ma.masked_array(im,mask) 
    im_corrected = image_square - np.tile(np.mean(imx, axis=1).T,(image_square.shape[0], 1)).T
    return im_corrected

image = imageSPM.pixels
#Working with square is simpler and sometimes SVI AFM bugs
if image.shape[0] != image.shape[1]:
    square = np.min(image.shape)
    image_square = image[:square,:square]
else :
    image_square = image
    
#Same as .correct_lines but for numpyarray
image_correct_line = image_square - np.tile(np.mean(image_square, axis=1).T,(image_square.shape[0], 1)).T 
#Best way to correct lines if you have big objects 
im_corrected = correct_lines_objects(image_square)

fig, ax = plt.subplots(1,3,figsize=(15,5))
plt.subplot(131)
plt.imshow(image, cmap='gray') 
plt.colorbar()
plt.title('raw image')

plt.subplot(132)
plt.imshow(image_correct_line, cmap='gray')
plt.colorbar()
plt.title('image flaten by line') 

plt.subplot(133)
plt.imshow(im_corrected, cmap='gray') 
plt.colorbar()
plt.title('image flaten by line improved')
plt.show()