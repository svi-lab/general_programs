# created by Pascal Raux
import numpy as np  # calcul matriciel et scientifique
import matplotlib.pyplot as plt  # figure and graphs
#%% Figure insets
"""
insetposition returns the position quadruplet [x,y, w,h] of an inset
corresponding to the current position of an parent axis label given as argument

arguments x, y, w, h are the components of inset position normalized by the parent axis width/height
    x,y position of the bottom left corner of the inset
    w,h vertical width and horizontal height of the inset
    they are expected to be given in a quadruplet xywh= [x, y, w, h]

 NB to be used directly as insetlabel= plt.axes(insetposition(parentax, xywh= [x,y,w,h]), facecolor='w')
"""
def insetposition(parentID, xywh = [.6, .6, .35, .35]):
    x,y,w,h = xywh[0], xywh[1], xywh[2], xywh[3]

    pos = np.array(parentID.get_position()) # get BBox = [[x,y], [x+w,y+h]] of the parent axis
    # positions of the bottom left normalised by height/width of the parent axis
    xinset = pos[0, 0] + x*(pos[1, 0] - pos[0, 0])
    yinset = pos[0, 1] + y*(pos[1, 1] - pos[0, 1])
    # height/width of the inset
    winset = w*(pos[1, 0] - pos[0, 0])
    hinset = h*(pos[1, 1] - pos[0, 1])
    return [xinset, yinset, winset, hinset] # return the quadruplet [x,y, w, h]

"""
createinset creates an automatic inset for an axes
arguments x, y, w, h are the components of inset position normalized by the parent axis width/height
          to be given in a quadruplet xywh= [x, y, w, h]
"""
def createinset(parentID, xywh = [.6, .6, .35, .35], color='w'):
    #creates new axes with the quadruplet created by insetposition
    insetlabel = plt.axes(insetposition(parentID , xywh = xywh),
                          facecolor= color)
    return insetlabel

plt.close('all')
#%% example 1

fig = plt.figure()
plt.plot(np.linspace(1,10), np.linspace(8,2),'k')

axID = plt.gca() # get the axes' ID
insetID = createinset(axID)  # create the new axes, saving its ID into insetID
# plot inside the inset using insetID:
insetID.plot(np.linspace(0,3,10),np.linspace(0,3,10)**2,'or')
# Set inset labels
insetID.set_xlabel('$X_{inset}$')
insetID.set_ylabel('$Y_{inset}$')

#%% example 2

fig = plt.figure(figsize=(10,4.5))
# build a double column figure:
a1 = fig.add_subplot(121)
a2 = fig.add_subplot(122)
a1.plot(np.linspace(1,10), np.linspace(1,10)**2,'-b')
a2.plot(np.linspace(1,10), np.linspace(1,10)**.5,':k')
# create an inset in axes a1 on the top left
inseta1 = createinset(a1, xywh= [.1, .6,.35, .35])
inseta1.plot(np.linspace(0,3,10),np.linspace(0,3,10),'dg')
# create another inset in axes a2 on the top left
inseta2 = createinset(a2, xywh=[.1,.6,.35,.35])
inseta2.plot(np.linspace(0,3,10),np.linspace(0,3,10)**2,'sr')
# create an inset in axes a2 on the bottom right, with bigger dimensions
inseta2b = createinset(a2,xywh = [.55, .1, .4, .4])
inseta2b.plot(np.linspace(0,3,10), np.linspace(0,3,10)**-1, 'om')

# create an inset inside this second inset:
insetption = createinset(inseta2b)
insetption.plot(np.linspace(1,10), np.linspace(1,10)**.5,'-k')
