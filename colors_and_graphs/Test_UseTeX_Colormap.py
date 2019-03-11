# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine
This script is a minimal working exemple to test the some functions of
Plot_Functions.py.
"""

import numpy as np
import imageio
import matplotlib.pyplot as plt
import Plot_Functions as pf

# --- Parameters to choose --- #

Do_Save = True
UseTeX = True
Serif = False
Save_Name = 'plotfunctions_test'

# --- Initiatilsation --- #

Turquoise, Blue, Dark_blue, Red, Orange, Black, White = pf.SaintGobain_Colors()
pf.Init_Graphs(UseTeX=UseTeX, Serif=Serif)

# ----------- Log plot: tests Init_Graphs with UseTeX=True ------------------ #

X = np.arange(0, 4, 0.1)
Y = X**2

# Plots

plt.figure()
p = []
p.append(plt.loglog(X, Y, '-', color=Red)[0])
p.append(plt.loglog(X[::3], 2*Y[::3], 'o', mfc=Blue, mec='k')[0])

Legends = ['line', 'dots']

pf.Set_Graph(p, Title='Log test', X_Label=r'$f$', Y_Label=r'$\frac{R}{R_0}$',
             Legends_Names=Legends, Legends_Position='upper left')

# ------------------ Colormap: \micro{} and Draw_Colormap ------------------- #


Max_Thickness = 200  # µm
Min_Thickness = 130  # µm
Color_Map_Name = 'GnBu'

File_Name = 'dewetting.jpg'

Image = imageio.imread(File_Name)

# Plots

plt.figure()
pf.Draw_Colormap(Image, Extrema=[Max_Thickness, Min_Thickness],
                 Title='Colormap test', Colorbar_Title=u'\micro{}m',
                 Color_Map_Name=Color_Map_Name)

# ------------------------------- Save graphs ------------------------------- #

Figure_List = plt.get_fignums()
pf.Save_Graphs(Do_Save, Save_Name, Figure_List=Figure_List)
pf.Save_Graphs_wo_title(Do_Save, Save_Name + 'wo-title', Figure_List=Figure_List)
