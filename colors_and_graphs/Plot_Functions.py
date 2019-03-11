#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by Quentin Magdelaine
This file gathers together sereval functions to play with colors and plots.
Theses functions are exemplified in Test_UseTeX_Colormap.py script.
"""

# Packages
import numpy as np  # scientific computation
from matplotlib import pyplot as plt  # plots
from matplotlib.backends.backend_pdf import PdfPages
# to save several graphs in one pdf
from mpl_toolkits.axes_grid1 import make_axes_locatable
# useful to adjust the colorbar of colormaps
import skimage  # images


def Get_Color_Map(Color_Map_Name, N_Data=256):
    """
    This function extracts a specified number of colors, linearly
    distributed, from the specified colormap. Exemples of matplotlib
    colormap are viridis, magma, coolwarm, spectral, BrBG, RdBu, Blues,
    Reds, PRgn.
    Inputs : Color_Map_Name is a string corresponding to an existing colormap.
    N_Data is a interger, corresponding to the number of different colors you
    want, equal to 256 by default.
    The output is a uint8 bidimensional numpy array.
    """
    Color_Map = plt.get_cmap(Color_Map_Name, N_Data)
    Colors = np.array([list(Color_Map(i)[0:3]) for i in range(N_Data)])
    return skimage.img_as_ubyte(Colors)


def SaintGobain_Colors():
    Turquoise = np.array([103., 185., 176.])/255.
    Blue = np.array([33., 156., 220.])/255.
    Dark_blue = np.array([23., 66., 140.])/255.
    Red = np.array([206., 20., 49.])/255.
    Orange = np.array([229., 83., 26.])/255.
    Black = np.array([0., 0., 0.])/255.
    White = np.array([1., 1., 1.])
    return Turquoise, Blue, Dark_blue, Red, Orange, Black, White


def Interpolate_Colors(N_Data, Colors):
    """
    This function returns a specified number of colors, linearly
    distributed, extrapolated between the specified colors.
    The output is a bidimensional list.
    Inputs: N_Data is the number of different color you want. Colors is a list
    or numpy array of the colors (3 elements tuple, list or numpy array)
    between which you want interpolate. N_Data can be either smaller or larger
    than the Colors list length.
    """
    if N_Data < 2:
        return Colors[0]
    else:
        N_Colors = len(Colors)
        Data_Color_Index = np.arange(N_Data) * float(N_Colors-1) / float(N_Data-1)
        Data_Color_Index_0 = np.floor(Data_Color_Index).astype(int)
        Delta_Data_Color = Data_Color_Index - Data_Color_Index_0
        Colors = np.concatenate((Colors, Colors[-1].reshape(1, 3)), axis=0)

        Colors_Inter = [(1 - DDC) * Colors[DCI0] + DDC * Colors[DCI0+1]
                        for DDC, DCI0 in zip(Delta_Data_Color, Data_Color_Index_0)]
        return Colors_Inter


def Init_Graphs(UseTeX=False, Serif=False):
    """
    This function initializes matplotlib paremeters to have nice graphs.
    I recommand to call it at the beginning of each program with plots.
    The parameters proposed can be adapted to your needs and preferences. Their
    are fixed directly in the code and not in argument. The two only inputs are
    boolean, telling the program if want to use TeX font and if you want a
    serif or sans-serif font.
    If you use TeX font, the font is computer modern by default. Otherwise the
    default fonts are times new roman with serif and arial without.
    """

    # Choice of font
    # ------------ #
    plt.rcParams['text.usetex'] = UseTeX  # tells matplotlib to use TeX
    plt.rcParams['text.latex.unicode'] = UseTeX  # allows some unicode symbols
    if UseTeX:
        if Serif:
            plt.rcParams['text.latex.preamble'] = [r'\usepackage[squaren,Gray]{SIunits}']
            # Package allowing upright greek mu with the function \micro{} in
            # math mode. This upright mu is necessary for micrometer symbol.
            plt.rcParams['font.family'] = 'serif'
            plt.rcParams['font.serif'] = 'cm'  # computer modern, standard TeX font
        else:
            plt.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}',
                                                   r'\usepackage[squaren,Gray]{SIunits}']
            # sfmath parckage make that even math mode is without serif.
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = 'cm'
    else:
        if Serif:
            plt.rcParams['font.family'] = 'Times New Roman'
        else:
            plt.rcParams['font.family'] = 'arial'

    # Figure size
    # -------- #
    plt.rc('figure', figsize=[7, 5.6])
    # horizontal and vertical sizes of the figure, label included, in inches
    plt.rc('figure.subplot', left=0.1, bottom=.015)
    # not tested, probably space between subfigures

    # Font sizes
    # -------- #
    plt.rc('font', size=16)  # general font size
    plt.rc('axes', labelsize=16)  # x & y label
    plt.rc('axes', titlesize=16)  # title
    plt.rc('xtick', labelsize=13)  # x ticks
    plt.rc('ytick', labelsize=13)  # y ticks

    plt.rc('lines', markersize=6, markeredgewidth=0.5)
    # size and edge width of makers
    plt.rc('lines', linewidth=1.5)  # width of the lines

    # Parameters for the legends
    # ------------------------ #
    plt.rc('legend', frameon=False, fancybox=False)
    # fancybox rounds the angles of legend box
    plt.rc('legend', numpoints=1)  # number of marker per legend
    plt.rc('legend', markerscale=1)  # maker size in the legend
    plt.rc('legend', fontsize=16)
    plt.rc('legend', handlelength=0.6)    # length of the legend handles
    plt.rc('legend', handletextpad=0.6)   # pad between legend handle and text
    plt.rc('legend', labelspacing=0.6)    # vertical space between entries

    # Parameters for the ticks
    # ---------------------- #
    """
    You can choose the direction of the ticks, in or out the frame, and where
    they are : left, right, bottem and left. Default is inwards, everywhere.
    """
    plt.rc('xtick', direction='in', bottom='true', top='true')
    plt.rc('ytick', direction='in', left='true', right='true')

    """
    These parameters seem good for lot of graphs, but may be wrong for some
    others, e.g. inwards ticks are not readable on colormaps. You can change
    theses parameters specicaly for one graph adding these lines in your script
    after the plot:
        plt.gca().tick_params(which='both', bottom='true', top='false',
                              left='false', right='true')
        plt.gca().tick_params(which='both', direction='out')
    both meaning major and minor ticks (and not x and y)
    """

    """
    Major is the usual ticks, and minor is for subdvision, e.g. in logscale.
    These lines are commented because default matplotlib parameters seem good.
    """
    # plt.rc('xtick.major', size=3, width=1)
    # plt.rc('xtick.minor', size=2, width=1)
    # plt.rc('ytick.major', size=3, width=1)
    # plt.rc('ytick.minor', size=2, width=1)

    # Parameters for the global frame
    # ----------------------------- #
    # plt.rc('axes', linewidth=2)  # thickness of the global frame

    # Parameters to save figures
    # ------------------------ #
    """
    This line allows to save graphs without blank around the graph (and without
    cutting the labels), with transparent background and with a nice but not
    exagerated definition.
    """
    plt.rc('savefig', bbox='tight', transparent=True, dpi=300)


def Set_Graph(Plots, Title='', X_Label='', Y_Label='', Legends_Names=[],
              Legends_Position='best'):
    """
    After having plotted your data, this function sets all the
    parameters.
    Inputs : Plots is the list of the diffent data sets you plotted on your
    figure, you can omit the data sets for which you do not want legend.
    Title, X_Lable, Y_Label and Legends_Position are self-explanatory.
    Legends_Names is a list of strings having the same length as Plots.
    """
    if Title:
        plt.title(Title, y=1.04)
    if X_Label:
        plt.xlabel(X_Label)
    if Y_Label:
        plt.ylabel(Y_Label)
    if Legends_Names:
        [P.set_label(LN) for P, LN in zip(Plots, Legends_Names)]
        plt.legend()
        plt.rc('legend', loc=Legends_Position)
    """
    Possible location for the legends: 'upper left', 'center', 'upper center',
    'lower left', 'lower right', 'center left', 'upper right', 'right',
    'lower center', 'center right' and 'best'.
    """

    plt.tight_layout(pad=0.)  # adjusts figures to suppress blank.

    """
    # Optionnal lines about ticks
    Lines to add in this function or directly in your script if you want
    to do diffently as you set in Init_Graph.
    which='both' specifies that you want to apply the new parameters to minor
    and major ticks. The first command specifies where ticks are.
    The second specifies if the ticks are in or out the frame.
    """
    # plt.gca().tick_params(which='both', bottom='true', top='false',
    #                       left='false', right='true')
    # plt.gca().tick_params(which='both', direction='out')
    """
    if you set all positions to false, you will delete all the ticks, but not
    the numbers. If you want to delete them as well, use:
    """
    # plt.gca().get_xaxis().set_visible(False)
    # plt.gca().get_yaxis().set_visible(False)


def Draw_Colormap(Image, Extrema=False, Title=False, X_Label=False,
                  Y_Label=False, Colorbar_Label=False, Colorbar_Title=False,
                  Color_Map_Name='magma'):
    """
    Plots an image with the specified colormap.
    Colorbar label is a text longside the colorbar, whereas its title is above.
    Each one of these texts should have its command, but the one for title does
    not seem to work, so I use the one for the label and move it to have a text
    above, which is nice if you just want the specify the units. Therefore,
    colorbar title and label are not compatible for now.
    Extrema are the min and max values you want on your map: values below and
    above will be drawn as they were equal to the min and max values.
    """
    plt.set_cmap(Color_Map_Name)  # set the colormap
    Axes = plt.gca()

    # Plots
    if Extrema:
        Im = Axes.imshow(Image, vmin=Extrema[0], vmax=Extrema[1])
    else:
        Im = Axes.imshow(Image)

    # Colormap title and labels
    if Title:
        plt.title(Title, y=1.04)
    if X_Label:
        plt.xlabel(X_Label)
    if Y_Label:
        plt.ylabel(Y_Label)

    # Color bar at the right size and place
    divider = make_axes_locatable(Axes)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    Colorbar = plt.colorbar(Im, cax=cax)

    # Colorbar label or title
    if Colorbar_Label:
        Colorbar.set_label(Colorbar_Label)
    if Colorbar_Title:
        # Colorbar.ax.set_title(Colorbar_Title) doesn't work
        Colorbar.set_label(Colorbar_Title, labelpad=-35, y=1.1, rotation=0,
                           size=18)
        """
        labelpad and y value has to be changed if you change the font size or
        figure size.
        """

    plt.tight_layout(pad=0.)  # adjusts figures to suppress blank.

    # Ticks
    """
    On color map you may want to delete the ticks, or at least to set them
    outwards for readability.
    """
    # Deletes the ticks but keeping the border
    Axes.tick_params(which='both', direction='out')
    Axes.get_xaxis().set_visible(False)
    Axes.get_yaxis().set_visible(False)
    """
    If you want to delete the ticks but not the numbers, use instead:
        Axes.tick_params(which='both', bottom='false', top='false',
                         left='false', right='false')
    If you want to delete border, ticks and number, use simply:
        plt.axis('off')
    """
    # Colorbar ticks
    Colorbar.ax.tick_params(direction='out')


def Save_Graphs(Do_Save, Save_Name, Figure_List=False, PNG=False):
    """
    I like to have vectorial graphs so I save my graphs in PDF files. Python
    allows you to save several graph in one file, which I find practical.
    The goal if this function is essentially to use this option.
    Inputs:
    - Do_Save is a boolean, true of false. It is convenient to set it at
      the beginning of your script in order to change it when you do some tests
      and do not want to erase previous graphs.
    - Save_Name: name of the future figure file without the extention.
    - Figure_List: list of the figure you want to save. If you want to save all
      the active figures, use : Figure_List = plt.get_fignums(). By default, it
      is set at False, in this case it will just save the last figure.
    - PNG is a boolean, if set on true, the function saves the graph twice, in
      PDF and PNG.
    """
    if Do_Save:
        if not Figure_List:
            plt.savefig(Save_Name + '.pdf')
            if PNG:
                plt.savefig(Save_Name + '.png')
        else:
            with PdfPages(Save_Name + '.pdf') as pp:
                [pp.savefig(FL) for FL in Figure_List]
            if PNG:
                for FL in Figure_List:
                    plt.figure(FL)
                    plt.savefig(Save_Name + '_' + str(FL) + '.png')


def Save_Graphs_wo_title(Do_Save, Save_Name, Figure_List=False, PNG=False):
    """
    This function saves figures in the same manner than Save_Graphs but
    deletes the title before: titles are convenient when you look at the graphs,
    but you do not need it anymore when you put it in a presentation or report.
    """
    if Do_Save:
        Save_Name = Save_Name
        if not Figure_List:
            plt.gcf().axes[0].title.set_text('')
            plt.tight_layout(pad=0.)
            plt.savefig(Save_Name + '.pdf')
            if PNG:
                plt.savefig(Save_Name + '.png')
        else:
            for FL in Figure_List:
                Fig = plt.figure(FL)
                Fig.axes[0].title.set_text('')
                plt.tight_layout(pad=0.)
            with PdfPages(Save_Name + '.pdf') as pp:
                [pp.savefig(FL) for FL in Figure_List]
            if PNG:
                for FL in Figure_List:
                    plt.figure(FL)
                    plt.savefig(Save_Name + '_' + str(FL) + '.png')
