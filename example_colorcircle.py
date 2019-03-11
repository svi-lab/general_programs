"""
Created by Pascal Raux
"""

import numpy as np  # calcul matriciel et scientifique
import matplotlib.pyplot as plt  # figure and graphs
import matplotlib.patches as mpatches
from math import pi

#%%
"""
# COLORCIRCLE function:

 this functions return a RGB triplet depending on the input
 default input corresponds to an angle in degrees
 (from 0 (red) to 120 (green) to 240 (blue) to 360 (red))
 if input is NaN, returns black
 optional parameters :
 - saturation of the color: sat (between 0 and 1)
 - luminosity of the color : lum (between 0 and 1)
 - exponent affects the color gradient in each sector : colorexp
 - customcolors allows to define the colors used in the circle
"""
def colorcircle(angle, sat=.95, lum=0, colexp=.75, customcolors=[]):
    if np.isnan(angle): # black color if NaN value
        return np.zeros(3)
    # initialisation:
    if len(customcolors)==0: # default is a chromatic RGB circle
        # angle // 60 determine which colors we will have to combine
        # first color bound for each sector of 60°
        colini = np.array([[1,0,0], [1,1,0], [0,1,0], [0,1,1], [0,0,1], [1,0,1]])
    else:
        # custom color are defined
        colini = np.array(customcolors)


    # dcol is the difference between the two bounding colors in each sector
    dcol = np.concatenate((colini[1:], colini[0:1])) - colini
    # angular width of each sector
    width = 360/float(colini.shape[0])
    # angle value between 0 and 360°
    angle = angle % 360
    # get the sector index with angle//width
    sector = int(angle//width)

    # angle % width determines the angular difference in the current sector
    # color using exponent to improve the contrast
    # formula= col1 + (col2-col1)*dangle**colexp
    RGB = np.array(colini[sector] + dcol[sector]*(angle%width)/float(width))**colexp

    #adjust saturation and luminosity
    RGB = (sat*RGB) * (1 - lum) + lum * np.ones(3)
    return RGB


#plt.close('all')
#%% example 1 basic use for shades of colors
#plt.close()
plt.figure()

time = np.linspace(0,2*pi) # xaxis
N = 20
for i in range(N):
    colorangle = i*240/float(N) # an angle in degrees
    sine = (N-i)*np.sin(time) # sine with a different amplitude for each i
    plt.plot(time, sine, '-', color=colorcircle(colorangle))


#%% example 2: custom colors
#plt.close()
plt.figure()
# argument for custom colors: array of RGB triplets
colorarray = np.array([[252,35,90],[80,130,220],[90,180,50], [255,120,15]])/255. # raspberry, blue, forest, orange
time = np.linspace(0,2*pi) # xaxis
N = 20
for i in range(N):
    colorangle = i*360/float(N) # an angle in degrees
    sine = (N-i)*np.sin(time) # sine with a different amplitude for each i
    plt.plot(time, sine, '-', color=colorcircle(colorangle, sat=1, customcolors = colorarray))

N=10
colorarray2 = [[1,0,0],[0,0,0],[0,0,1]] # red, black blue
for i in range(N):
    colorangle = 120+i*240/float(N) # an angle in degrees
    fun =(time-pi)*.5*(i+1) # sine with a different amplitude for each i
    plt.plot(time, fun, '-', color=colorcircle(colorangle, customcolors = colorarray2))


# %% example 3 show a chromatic color circle
#plt.close()
# default parameters of colorcircle:
sat=.95 # saturation of the colors (see example 4)
lum=.0 # luminosity of the colors (see example 4)
colorexp=.75 # exponent for the transition between one color and another
colorarray = []
#colorarray = [[1,0,0],[0,0,0],[0,0,1]] # array of colors to show custom colors

step= 2 # angular step for wedges
theta = np.arange(360//step)
fig = plt.figure()
ax = fig.add_subplot(111)


for t in theta:
    # color of this wedge:
    col = colorcircle(theta[t]*step, sat=sat, lum=lum,
                      colexp=colorexp, customcolors = colorarray)
    # colored wedges
    ax.add_patch(mpatches.Wedge((0, 0), .5, t*step, (t+1)*step,
                                color=col))
# NaN value as a dot in the center
plt.plot(0,0,'o',
         color=colorcircle(float('NaN'), sat=sat, lum=lum,colexp=colorexp))
# comments:
if len(colorarray)==0:
    plt.text(.55, -.01, 'Red = 0', color='r')
    plt.text(.2, .5, 'Yellow = 60', color='y')
    plt.text(-.45, .5, 'Green = 120', color='g')
    plt.text(-.8, -.01, 'Cyan = 180', color='c')
    plt.text(.2, -.55, 'Magenta = -60', color='m')
    plt.text(-.45, -.55, 'Blue = -120', color='b')

plt.axis('equal')
plt.axis('off')
plt.show(fig)
#%% example 4: map of saturation and luminosity
#plt.close()

angle = 120 # angle of the color to display
N=40 # size of the image
img = np.zeros((N+1,N+1,3)) # RGB square image
s = np.arange(N+1)/float(N)
l = np.arange(N+1)/float(N)
fig = plt.figure(figsize=(5,5))

for col, sat in enumerate(s):
    for row, lum in enumerate(l):
        # the RGB colors channels defined by colorcircle are between 0 and 1
        img[row,col,:] = colorcircle(angle, sat=sat, lum=lum)

# converts this image as uint8 and display it
img = (255*img).astype('uint8')
plt.imshow(img)

plt.xlabel('Saturation')
plt.ylabel('Luminosity')

# show a square for default settings:
defaultset=[.95, 0]
rect = np.array([[0, 0, 1, 1, 0], [0, 1, 1, 0, 0]])-.5  # rectangle as [x, y], centered around 0
plt.plot((defaultset[0]*N)//1+rect[0], (defaultset[1]*N)//1+ rect[1], '-k',linewidth =.5)

# adjust axes limits and ticks
plt.gca().set_xlim([-.5,N+.5])
plt.gca().set_ylim([-.5,N+.5])
_ = plt.xticks(np.arange(0,N+1,N/5),
               np.round(np.arange(0,1.1,.2), decimals =2).astype('str'))
_ = plt.yticks(np.arange(0,N+1,N/5),
               np.round(np.arange(0,1.1,.2), decimals=2).astype('str'))

_ = plt.title('angle = '+str(angle)+'$^\circ$')

