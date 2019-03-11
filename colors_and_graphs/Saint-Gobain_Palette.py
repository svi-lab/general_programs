# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine

This script write a text file with the Saint-Gobain colors. It written in the
right way and at the right place to be seen as a color palette by inkscape.
The only parameter you have to choose is your username on your computer.
I have written a Python script to do that instead of directly write the text
file, just to calculate the RGB codes of the lighter version of the orignal
colors.
"""

import numpy as np
import skimage

# Parameters to choose

username = 'Q7964538'
Folder_Path = 'C:/Users/' + username + '/AppData/Roaming/inkscape/palettes/'
Palette_Name = 'SG_palette.gpl'

# Definition of the Saint-Gobain colors

Turquoise = np.array([103., 185., 176.])/255.
Blue = np.array([33., 156., 220.])/255.
Dark_blue = np.array([23., 66., 140.])/255.
Red = np.array([206., 20., 49.])/255.
Orange = np.array([229., 83., 26.])/255.
Black = np.array([0., 0., 0.])/255.
White = np.array([1., 1., 1.])

Names = ['Turquoise', 'Blue', 'Dark Blue', 'Red', 'Orange', 'Black']

Colors = np.array([Turquoise, Blue, Dark_blue, Red, Orange, Black])

"""
# Five lighter versions for each color
# ---------------------------------- #
The graphic style guide of Saint-Gobain define three lighter version of the
five colors : 80 %, 50 % and 30 %. Personnaly I find often useful to have much
lighter version. I have added 10 % and 5 %.
"""

Eighty_Colors = skimage.img_as_ubyte(0.8*Colors + 0.2*White)
Fifty_Colors = skimage.img_as_ubyte(0.5*Colors + 0.5*White)
Thirty_Colors = skimage.img_as_ubyte(0.3*Colors + 0.7*White)
Ten_Colors = skimage.img_as_ubyte(0.1*Colors + 0.9*White)
Five_Colors = skimage.img_as_ubyte(0.05*Colors + 0.95*White)

with open(Folder_Path + Palette_Name, 'w') as File_ID:
    File_ID.writelines('GIMP Palette\nName: SaintGobain\nColumns: 0\n#\n')
    for C, EC, FC, TC, TEC, FIC, N in zip(Colors, Eighty_Colors, Fifty_Colors,
                                          Thirty_Colors, Ten_Colors,
                                          Five_Colors, Names):
        C = skimage.img_as_ubyte(C)
        File_ID.writelines(str(C[0]) + ' ' + str(C[1]) + ' ' + str(C[2]) + ' ' + N + '\n')
        File_ID.writelines(str(EC[0]) + ' ' + str(EC[1]) + ' ' + str(EC[2]) + ' ' + N + ' 80 %\n')
        File_ID.writelines(str(FC[0]) + ' ' + str(FC[1]) + ' ' + str(FC[2]) + ' ' + N + ' 50 %\n')
        File_ID.writelines(str(TC[0]) + ' ' + str(TC[1]) + ' ' + str(TC[2]) + ' ' + N + ' 30 %\n')
        File_ID.writelines(str(TEC[0]) + ' ' + str(TEC[1]) + ' ' + str(TEC[2]) + ' ' + N + ' 10 %\n')
        File_ID.writelines(str(FIC[0]) + ' ' + str(FIC[1]) + ' ' + str(FIC[2]) + ' ' + N + ' 5 %\n')

    File_ID.writelines('255 255 255 White')
