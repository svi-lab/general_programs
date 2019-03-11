# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine
This script exemplifies and test the function White_Balance_Auto of
Picture_Functions file. This program compares the automatic correction
of the white balance proposed by White_Balance_Auto and a manual correction.
This script uses a frame of a video, but it is easy to adapt it to a
simple picture.
This script does not work with inline plot because of the ginput function, if
needed use #matplotlib qt5.
To play with videos, I use imageio package, you can install easily with
Anaconda. In the Anaconda prompt write:
    conda install -c conda-forge imageio
Then in spyder, in the console:
    imageio.plugins.ffmpeg.download()
"""

# Packages
import numpy as np
import imageio  # package useful for video
from matplotlib import pyplot as plt
import Picture_Functions as pif


# ------------------------------- Parameters -------------------------------- #

Input_Name = 'video_test_input.avi'  # video path and name you want to correct
Frame_Number = 1  # frame number you want to use

# Manual correction you want to compare with the automatic correction.
Manual_Saturation = [0.97, 0.91, 1.]
Manual_Luminence = [0., 0., 0.1]

# ------------------------------ Program begin ------------------------------ #

# Extraction of the test image
Video_ID = imageio.get_reader(Input_Name, 'ffmpeg')
Image = np.array(Video_ID.get_data(Frame_Number))/255.
Video_ID.close()

# Automatic correction done by the White_Balance_Auto function
Saturation_Auto, Luminence_Auto = pif.White_Balance_Auto(Image)

# Display of the proposed correction
Color = ['R=', 'G=', 'B=']
Saturation_Text = [C + str(round(SA, 2)) for C, SA
                   in zip(Color, Saturation_Auto)]
Luminence_Text = [C + str(round(LA, 2)) for C, LA
                  in zip(Color, Luminence_Auto)]

print('The program suggests the following correction: \n' +
      '\t - satutation: ' + ' '.join(Saturation_Text) + '\n' +
      '\t - luminence: ' + ' '.join(Luminence_Text))

# Correction of the image with the specified parameters
Manual_Image = pif.White_Balance(Image.copy(), Manual_Saturation,
                                 Manual_Luminence)

# Display of the result
plt.figure()
plt.imshow(Manual_Image)
plt.axis('equal')
plt.title('Manual correction')
plt.show()
