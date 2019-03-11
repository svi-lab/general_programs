# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine
This script exemplifies and test several function of Picture_Functions and show
how to do other simple operations on pictures and videos: crop and acceleration.
Given a video file, the program corrects the video save it writing a new video
.avi file and a image sequence.
To play with videos, I use imageio package, you can install easily with
Anaconda. In the Anaconda prompt write:
    conda install -c conda-forge imageio
Then in spyder, in the console:
    imageio.plugins.ffmpeg.download()
"""

import os
import numpy as np

import imageio
import skimage
import Picture_Functions as pif

# ------------------------------- Parameters -------------------------------- #

Do_Image_Sequence = True
Input_Name = 'video_test_input.avi'  # name of the original video
Save_Name = 'video_test_output'  # name of the output video

# Times at which you want the new video to start and end.
Start_Time = 1.5  # s
End_Time = 3.5  # s

"""
# Acceleration
To speed up a video, you have two possibilies.
The first one is to keep only regularly
spaced frame and delete the other ones. If the original frame rate was
sufficent (around 25 fps), it is probably the best thing to do because you
reduce the size of your video. To do this with this script choose an
Acceleration_factor greater than 1.
The second possibility is to save the new video with a higher frame rate. To
do this with this script choose set the parameter One_Over to in integer larger
than 1.
"""
Acceleration_Factor = 1.  # Factor by which fps will be multiplied in the ouput
One_Over = 1  # Factor by which fps will be multiplied in the ouput

"""
# Picture corrections
This script allows you to edit the pictures of the video. You can correct :
- the white balance choosing the saturation and luminence correction for R, G
  and B, see White_Balance function to know more;
- the contrast choosing min and max value, see Improve_Contrast function to
  know more;
- the framing choosing a crop rectangle: be careful, final heigth and width
  have to be a multiple of 16.
"""
# White balance correction
Saturation = [0.97, 0.91, 1.]
Luminence = [0., 0., 0.1]

# Contrast correction
Minimum = 0.05
Maximmum = 0.8

# Framing
Crop = [220, 1180, 740, 1860]  # first row, last row, first column, last column

# ------------------------------ Program begin ------------------------------ #

# Preparation of video reader and writer
Video_ID = imageio.get_reader(Input_Name, 'ffmpeg')  # video reader

Input_fps = Video_ID.get_meta_data()['fps']  # get the input video fps
Output_fps = Acceleration_Factor*Input_fps  # compute the output video fps

# Computing frame number corresponding to the start and end time
Fisrt_Frame_Number = np.int(np.floor(Start_Time*Input_fps))
Last_Frame_Number = np.int(np.ceil(End_Time*Input_fps))

# List of the image number to correct and save in the new video
Image_Numbers_to_Get = np.arange(Fisrt_Frame_Number, Last_Frame_Number,
                                 One_Over)

# Opening of the video writer with the right fps
Video_Writer = imageio.get_writer(Save_Name + '.avi', fps=Output_fps)

# Creation of the directory for the image sequence
if Do_Image_Sequence and not os.path.isdir(Save_Name):
    os.mkdir(Save_Name)

# ---- Loop over the pictures to correct them save them in the new video ---- #

for N in Image_Numbers_to_Get:
    """
    Load the image from the video reader and convert the uint8 values to [0-1]
    value.
    """
    Image = np.array(Video_ID.get_data(N))/255.
    # Crop
    Image = Image[Crop[0]:Crop[1], Crop[2]:Crop[3], :]
    # Improving contrast
    Image = pif.Improve_Contrast(Image, Minimum, Maximmum)
    # Correct white balance
    Image = pif.White_Balance(Image, Saturation, Luminence)
    # Convert the [0-1] values back to uint8.
    Image = skimage.img_as_ubyte(Image)
    # Write the new image in the new video
    Video_Writer.append_data(Image)
    # Save the image in the image sequence if asked
    if Do_Image_Sequence:
        imageio.imwrite(Save_Name + '/image-' + str(N-Image_Numbers_to_Get[0])
                        + '.jpg', Image)

# Closing of the video writer and reader
Video_Writer.close()
Video_ID.close()
