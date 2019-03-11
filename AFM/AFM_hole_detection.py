# -*- coding: utf-8 -*-
"""
How to detect holes in a AFM picture (diameters and depths)

This script uses pySPM, you can download it from https://github.com/scholi/pySPM
Documentation is here https://github.com/scholi/pySPM/blob/master/doc/pySPM%20Documentation.ipynb
You have to instal it for example with 'Conda install [your_Package]' in anaconda prompt.
"""

import pySPM
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import os
import ntpath
from math import sqrt, pi
from skimage.feature import blob_log
from skimage import exposure, filters
from skimage import segmentation, measure, morphology, draw
from skimage import img_as_ubyte
from scipy import ndimage

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

def find_holes(im, min_sigma=1, max_sigma=25, num_sigma=20, threshold=.1):
    """
    find holes in a picture
    input : image
    output : image 0=background int=different regions=holes
    """
    #Pretreatment
    p_min = np.amin(im)
    p_max = np.amax(im)
    im_corrected_g = img_as_ubyte(1-(im-p_min)/(p_max-p_min))
    im_cor_eq = exposure.equalize_adapthist(im_corrected_g)
    
    #Use blob_log fonction (Laplacian of Gaussian) to find approach size of holes
    #to stay short time analysis : num_sigma=20
    #to small holes : min_sigma=1 , max_sigma=25
    #to big holes : min_sigma=15 , max_sigma=60
    blobs_log = blob_log(im_cor_eq, min_sigma=min_sigma , max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
    blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

    #plot holes, the black area (0) will be the background marker
    blob=np.zeros(np.shape(im))
    for i in range(len(blobs_log[:,0])):
        r,c=draw.circle(blobs_log[i][0], blobs_log[i][1], blobs_log[i][2], shape=np.shape(im))
        blob[r,c]=1
    blob=morphology.binary_dilation(blob)
    
    #plot center of holes, will be markers 
    blob_peak=np.zeros(np.shape(im))
    for i in range(len(blobs_log[:,0])):
        r,c=draw.circle(blobs_log[i][0], blobs_log[i][1], 2, shape=np.shape(im))
        blob_peak[r,c]=1

    #label markers
    markers_black = (blob < 0.4).astype(np.int)
    labels_peaks = measure.label(blob_peak)
    markers_black +=  labels_peaks

    # /!\ watershed method take a gradient in argument
    gradient = ndimage.gaussian_gradient_magnitude(im_cor_eq, 2)
    ws = morphology.watershed(gradient, markers_black)
    final=morphology.opening(ws)

    return final

def find_properties(im, scaling):
    """
    find diameters and depth of the holes
    input:  im: image of regions
            scaling: 
    output: particules give [:,0]=x [:,1]=y [:,2]=dimeters in nm [:,3]=depth in nm
    """
    #Find properties of each detected region
    #suppress objects on edges
    im_wo_edges=segmentation.clear_border(im) 
    proportions=measure.regionprops(im_wo_edges)

    #Calculate droplets density (nb of droplets / size of picture)
    #density given in µm-2
    obj=[]
    for prop in proportions:
        b=prop.centroid
        b=(round(b[0]),round(b[1]))
        obj.append(b)
 
    #Calculate droplets diameters
    area=[]
    for prop in proportions:
        area.append(prop.area)
    area_part=np.asarray(area)     
    diameter=np.zeros(len(area_part))
    for i in range(len(area_part)):
        diameter[i]=2*sqrt(area_part[i]/pi)*scaling
        
    obj = np.asarray(obj)
    particules = np.insert(obj,2,diameter,axis=1)
    
    #Find maximum depth
    max_depth = np.zeros((len(particules),))
    for p in range(len(particules)) :
        depth = []
        rpix = particules[p][2]/2/scaling
        jmin = int(particules[p][1]- rpix)
        jmax = int(particules[p][1]+ rpix)
        j0 = ((jmin+jmax)/2)
        imin = int(particules[p][0]-sqrt(rpix*rpix - (particules[p][1]-j0)*(particules[p][1]-j0)))
        imax = int(particules[p][0]+sqrt(rpix*rpix - (particules[p][1]-j0)*(particules[p][1]-j0)))
        for j in range(jmin, jmax):
            for i in range(imin , imax):
                depth.append(im_corrected[i][j])
        depth = np.asarray(depth)
        d=np.amin(depth)
        max_depth[p] = d
        
        particules = np.insert(particules, 3, max_depth, axis=1)
            
    return particules


#Exemple is given for Burker AFM = SVI version
filename = os.path.realpath('image_test_AFM.001')
ScanB = pySPM.Bruker(filename) 

#Print all possible channels             
ScanB.list_channels()
#choose your channel
channel="Height Sensor"
imageSPM = ScanB.get_channel(channel=channel)
image = imageSPM.pixels
#Working with square is simpler and sometimes SVI AFM bugs
if image.shape[0] != image.shape[1]:
    square = np.min(image.shape)
    image_square = image[:square,:square]
else :
    image_square = image
  
#Best way to correct lines if you have big objects 
im_corrected = correct_lines_objects(image_square)
   
#Find holes in AFM picture 
im_object = find_holes(im_corrected)

#Save the scale to convert pixels in lenght 
#Here I assume you work in nm
if imageSPM.size['real']['unit'] == 'um' :
    scaling= 1000 * imageSPM.size['real']['x']/imageSPM.size['pixels']['x']
else:
    scaling= imageSPM.size['real']['x']/imageSPM.size['pixels']['x'] 
    
#Collect dimaeters and depths
particules = find_properties(im_object, scaling)

##Save data
folder_name = ntpath.dirname(filename)
title = ntpath.basename(filename).replace('.001','')
if os.path.exists(folder_name) is False:
    os.mkdir(folder_name)
np.savetxt(folder_name+'/Diam_Dep_'+title+'.txt', particules[:,2:4],'%.2f %.2f')

#Plot figure and object coutours
fig, ax = plt.subplots(1,2,figsize=(10,5))
fig.subplots_adjust(wspace = 0.5)
plt.subplot(121)
final_trace = im_object > 1
plt.imshow(im_corrected, cmap='gray')
plt.contour(final_trace, colors='lime',linewidths=0.5)
plt.title(title)
plt.show()

plt.subplot(122)
plt.plot(particules[:,2], particules[:,3], 'ro')
plt.xlabel(r'$Diamètre\:des\:objets\:(nm)$',fontsize=14)
plt.ylabel(r"$Profondeur\:d'objets$",fontsize=14)
plt.show()