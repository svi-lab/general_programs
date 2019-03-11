# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine
This file gathers together several functions to edit pictures and videos.
Python is a not so bad candidate to edit videos: you can speed them up (or even
write video with a changing frame rate to slow it down at the right moment),
cut them, crop them, correct colors, add text, convert them in image sequences
or convert an image sequence in a video.
Most of these operations are exemplified in Test_Video_Speed_Crop_Whitebalance
script. Some useful functions are defined here.
To play with videos, I use imageio package, you can install easily with
Anaconda. In the Anaconda prompt write:
    conda install -c conda-forge imageio
Then in spyder, in the console:
    imageio.plugins.ffmpeg.download()
"""

# Packages
import numpy as np
from matplotlib import pyplot as plt


def Extrema(Video_ID, Image_Numbers_to_Get):
    # Return global extrema in R, B and B over the whole video
    Minima = []
    Maxima = []
    for N in Image_Numbers_to_Get:
        Image = np.array(Video_ID.get_data(N))
        Minima.append(np.min(Image, axis=(0, 1)))
        Maxima.append(np.max(Image, axis=(0, 1)))
    return np.min(Minima, axis=0), np.max(Maxima, axis=0)


def Improve_Contrast(Image, Min, Max):
    """
    To improve contrast, the function sets to Min and Max the values of the
    picture which are below and above the Min and Max value and applies the
    linear transformation over all the value that send Min to 0 and Max to 1.
    Image input, Min and Max have to be consitant (0 - 1 or uint8), image
    output is between 0 and 1.
    """
    Image[Image > Max] = Max
    Image[Image < Min] = Min
    Image = (Image - Min)/(Max - Min)
    return Image


def Improve_Contrast_Colors(Image, Minima, Maxima):
    """
    The function does the same transformation than Improve_Contrast but
    individually for each color. Minima and Maxima are then min and max for
    each color: R, G and B. Return of Extrema function can be use as input
    here.
    Image input, Minima and Maxima have to be consitant (0 - 1 or uint8), image
    output is between 0 and 1.
    """
    for i, m, M in zip(range(3), Minima, Maxima):
        Image[:, :, i] = (Image[:, :, i] - m)/(M - m)
    Image[Image > 1] = 1
    Image[Image < 0] = 0
    return Image


def White_Balance(Image, Saturation, Luminence):
    """
    The function modifies the white balance of a picture given saturation and
    luminence coefficient for R, G, B. Luminence and saturation correction are
    defined this way:
        R' = Saturation*R*(1.-Luminence) + Lumincence
    To get an idea of which correction to apply you can use the
    White_Balance_Auto function and compare it result with some manual
    parameters with the Test_Auto_WhiteBalance script.
    Image input has to between 0 and 1, image output is between 0 and 1.
    """
    for i, S, L in zip(range(3), Saturation, Luminence):
        Image[:, :, i] = (1. - L)*S*Image[:, :, i] + L
    return Image


def White_Balance_Auto(Image):
    """
    The function corrects the white balance of a picture by measuring the
    colors of a specified rectangle supposed to be white or grey.It computes
    the saturation and luminence parameters to apply to get real white or grey.
    These parameters can be not completely satisfying, but it is a good start
    from which you can search better parameters for your image or video.
    Test_Auto_WhiteBalance script compares the result of the function and
    manually chosen parameters.
    Image input has to between 0 and 1, image output is between 0 and 1.
    Because of ginput, the function does not work with inline plots, use
    #matplotlib qt5 if needed.
    """

    # Choice of a white or grey region on the picture
    print('Choose a white rectangle, clicking on two points')

    plt.figure()
    plt.imshow(Image)
    plt.title('Choose a white rectangle, clicking on two points')
    plt.show()
    Points = plt.ginput(2)  # let you choose two points to define a rectangle

    # Croping of the image
    Crop = [Points[0][1], Points[1][1],
            Points[0][0], Points[1][0]]
    Crop = [int(C) for C in Crop]
    Crop_Image = Image[Crop[0]:Crop[1], Crop[2]:Crop[3], :].copy()  # crop

    # Display of the cropped picture
    plt.figure()
    plt.imshow(Crop_Image)
    plt.title('Cropped picture')
    plt.show()

    # Computing the averaged R, G and B over the rectangle
    Average_RGB = np.mean(Crop_Image, axis=(0, 1))
    Average_Light = np.mean(Average_RGB)
    """
    # Saturation and luminence parameters to correct the white balance
    If the color is higher than the average light, we apply a saturation
    correction which will lower it.
    If the color is larger than the average light, we apply a luminence
    correction which will increase it.
    At the end, we keep the same average light.
    """
    Saturation = np.array([Average_Light/C for C in Average_RGB])
    Saturation[Saturation > 1] = 1.
    Luminence = np.array([(Average_Light - C)/(1 - C) for C in Average_RGB])
    Luminence[Luminence < 0] = 0.

    # Correction of the cropped picture with White_Balance function
    Crop_Image = White_Balance(Crop_Image, Saturation, Luminence)
    plt.figure()
    plt.imshow(Crop_Image)
    plt.title('Corrected crop')
    plt.show()

    # Correction of whole picture with White_Balance function
    Image_Auto = White_Balance(Image.copy(), Saturation, Luminence)
    plt.figure()
    plt.imshow(Image_Auto)
    plt.title('Auto correction')
    plt.show()

    return(Saturation, Luminence)
