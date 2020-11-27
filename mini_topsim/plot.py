#!/usr/bin/python3
'''
Functions to interactively plot 2D-surfaces with data read from a .srf file.

This module offers functionality to create an interactive matplotlib-plot of 
2D-surfaces with the data read from a .srf file. To create a plot you have to 
invoke the \'plot(filename)\' function. Internally a private class is used to 
handle the plotting.

Keybindings:
    [Space]: shows next/previous surface
    [0-9]: only show each 2^n-th surface when pressing [Space]
    [f]: show first surface
    [l]: show last surface
    [r]: reverse direction of movement 
    [a]: toggle between automatic and 1:1 aspect ratio
    [d]: toggle between showing multiple surfaces or only the current surface
    [s]: saves plot as .png in cwd with the same filename as the .srf file
    [b]: switch between automatic and fixed y-boundaries
    [q]: quit the plot

The .srf file is expected to have the following format and can also include 
multiple surfaces:

    surface: (time) (npoints) x-positions y-positions
    x[0] y[0]
    x[1] y[1]
    ...
    x[npoints-1] y[npoints-1]
    surface: (time2) (npoints2) x-positions y-positions
    ...

x[n]: x-position in nm
y[n]: y-position in nm
time: time in s
npoints: number of points


Additionally this module can be used as a script:
    USAGE: $ python3 plot.py [Name of .srf file]


Classes:
    WrongFileExtensionError: Exception that gets raised if the passed file 
                             doesn't have the correct FileExtension

Functions:
    plot(filename): extracts surface data from the .srf file and creates an 
                    interactive plot with the data


Author: Haberl Alexander
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim
'''


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
# The _SurfacePlotter class overwrites the default plt keybindings.
# When overwriting some of these keybindings, matplotlib prints a warning 
# message, because they are bound to functions that will be removed in later 
# matplotlib versions.
# The following lines stop these warnings from being printed and cluttering 
# the terminal.
#
# Note: for later matplotlib releases we might have to remove the following 
# line from the _SurfacePlotter class:
#       'plt.rcParams['keymap.all_axes'] =''
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#


class _SurfacePlotter:
    '''
    Private class that handles the plotting. 
    
    This class should not be used outside of this module. If you want to plot 
    a .srf file use the function \'plot(filename)\' instead! Lists where used to
    save the information of multiple surfaces. Each list element represents a 
    surface at a specific point in time.

    Args:
        filename(string): Name of the .srf file

    Attributes:
        filename(string): Name of the .srf file
        xpoints_list(list): List of np-arrays. Each np-array holds all x-values 
            of one surface
        ypoints_list(list): List of np-arrays. Each np-array holds all y-values 
            of one surface
        time_list(list): Contains the timepoints from all surfaces.
        n_point_list(list): Contains the number of points from all surfaces.
        alreadyplotted_list(list): Contains information if a specific surface 
            has already been plotted
        surface_index(int): Used for indexing the lists mentioned above. Points 
            to the current surface
        forward_movement(bool): Toggling between moving forward/backwards.
        length(int): Length of the lists mentioned above.
        aspectratio_auto(bool): Toggling between automatic and 1:1 aspect-ratio
        deleteplot_mode(bool): Toggling between showing multiple surfaces 
            or only the current one
        stepsize(int): Size of step when switching between surfaces
        boundarymode_auto(bool): Toggling between fixed and automatic 
            x/y-boundaries
        ylim(Tuple of two floats): Bottom and Top y-limit of the plot.
        xlim(Tuple of two floats): Left and right x-limit of the plot.

    Raises:
        FileNotFoundError: if file is not found
        WrongFileExtensionError: if file doesn't have the correct file extension
        IndexError: if file is not formatted correctly
        ValueError: if file is not formatted correctly
    '''

    def __init__(self, filename):
        '''
        Initializes all class parameters and changes default plt keybindings.
        '''
        self.filename = filename
        self.xpoints_list = list()
        self.ypoints_list = list()
        self.time_list = list()
        self.n_point_list = list()
        self.alreadyplotted_list = None
        self.surface_index = 0
        self.forward_movement = True
        self.length = 0
        self.aspectratio_auto = True
        self.deleteplot_mode = True
        self.stepsize = 1
        self.boundarymode_auto = True
        self.ylim = None
        self.xlim = None
        plt.rcParams['keymap.fullscreen'] = ['ctrl+f']
        plt.rcParams['keymap.yscale'] = ['ctrl+l']
        plt.rcParams['keymap.home'] = ['h', 'home']
        plt.rcParams['keymap.all_axes'] = ''
        plt.rcParams['keymap.save'] = ['ctrl+s']
        plt.rcParams['keymap.quit'] = ['ctrl+w', 'cmd+w']
        self._read_srf_file()

    def _read_srf_file(self):
        '''
        Extracts x/y-values, time and number of points from the .srf file
        '''
        with open(self.filename) as file:

            if (self.filename.endswith(('.srf_save', '.srf')) == False):
                raise WrongFileExtensionError(
                    'plot.py:    Expected \'.srf\' or \'.srf_save\' file')

            xpoints = None
            ypoints = None
            i = 0
            j = 0

            for line in file:
                if 'surface:' in line:
                    string_array = line.split(' ')
                    self.time_list.append(float(string_array[1]))
                    self.n_point_list.append(int(string_array[2]))

                    xpoints = np.empty(self.n_point_list[i], dtype=np.float64)
                    ypoints = np.empty(self.n_point_list[i], dtype=np.float64)
                    self.xpoints_list.append(xpoints)
                    self.ypoints_list.append(ypoints)

                    i = i+1
                    j = 0
                else:
                    string_array = line.split(' ')
                    xpoints[j] = float(string_array[0])
                    ypoints[j] = float(string_array[1])
                    j = j + 1

            self.length = i
            self.alreadyplotted_list = [False] * self.length

    def on_key_press(self, event):
        '''
        Changes attributes of the class depending on the pressed key.

        Gets called by plt when a key is pressed. 

        Attributes:
            event: the key press event that causes this function to be called
        '''

        if(event.key == 'l'):
            lastelement = self.length - 1
            self.surface_index = lastelement

        elif(event.key == 'f'):
            self.surface_index = 0

        elif(event.key == ' '):
            if(self.forward_movement == True):
                self.surface_index = self.surface_index + self.stepsize
                if(self.surface_index >= self.length):
                    self.surface_index = 0

            else:
                self.surface_index = self.surface_index - self.stepsize
                if(self.surface_index <= -1):
                    self.surface_index = self.length - 1

        elif(event.key == 'r'):
            self.forward_movement = not self.forward_movement
            return

        elif(event.key == 'a'):
            self.aspectratio_auto = not self.aspectratio_auto

        elif(event.key == 'd'):
            self.deleteplot_mode = not self.deleteplot_mode
            return

        elif(event.key == 's'):
            fname = self.filename[:-4] + '.png'
            plt.savefig(fname, dpi = 420)
            return

        elif(event.key == 'b'):
            self.boundarymode_auto = not self.boundarymode_auto
            if(self.boundarymode_auto == False):
                ax = plt.gca()
                self.ylim = ax.get_ylim()
                self.xlim = ax.get_xlim() 

        elif(event.key == 'q'):
            plt.close('all')
            return

        elif(event.key.isnumeric() == True):
            self.stepsize = 2 ** int(event.key)
            return

        self.update_plot()

        return None

    def update_plot(self):
        '''
        Updates the plot depending on the saved parameters
        '''
        if(self.deleteplot_mode == True):
            plt.clf()
            self.alreadyplotted_list = [False for i in range(self.length)]
            ax = plt.gca()
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])


        if(self.alreadyplotted_list[self.surface_index] == False):
            plt.plot(self.xpoints_list[self.surface_index], 
                   self.ypoints_list[self.surface_index], 
                   label='t = ' + str(self.time_list[self.surface_index]) + 's')
            self.alreadyplotted_list[self.surface_index] = True

        if(self.boundarymode_auto != True):
            plt.ylim(self.ylim)
            plt.xlim(self.xlim)
        else:
            ax = plt.gca()
            ax.relim()
            ax.autoscale(True, 'both', False)

        ax = plt.gca()
        if(self.aspectratio_auto != True):
            ax.set_aspect(aspect=1)
        else:
            ax.set_aspect(aspect = 'auto')

        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlabel('x in nm')
        plt.ylabel('y in nm')
        plt.title("Surfaces: 2D-Plot")
        plt.grid(True, 'both', 'both')
        plt.draw()
        

    def plot_interactive(self):
        '''
        Starts the interactive plot
        '''
        fig = plt.figure()
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.update_plot()
        plt.show()


class WrongFileExtensionError(Exception):
    '''
    Gets raised if the FileExtension is not correct
    '''
    pass


def plot(filename):
    '''
    Plots the 2D-surfaces from a \'.srf\' file in an interactive plt-plot.

    Keybindings:
    [Space]: shows next/previous surface
    [0-9]: only show each 2^n-th surface when pressing [Space]
    [f]: show first surface
    [l]: show last surface
    [r]: reverse direction of movement 
    [a]: toggle between automatic and 1:1 aspect ratio
    [d]: toggle between showing multiple surfaces or only the current surface
    [s]: saves plot as .png in cwd with the same filename as the .srf file
    [b]: switch between automatic and fixed y-boundaries
    [q]: quit the plot

    The .srf file is expected to have the following format and can also include 
    multiple surfaces:

    surface: (time) (npoints) x-positions y-positions
    x[0] y[0]
    x[1] y[1]
    ...
    x[npoints-1] y[npoints-1]
    surface: (time2) (npoints2) x-positions y-positions
    ...

    x[n]: x-position in nm
    y[n]: y-position in nm
    time: time in s
    npoints: number of points

    Args:
        filename(str): Name of the \'.srf\' file.

    Raises:
        FileNotFoundError: if file is not found
        WrongFileExtensionError: if file doesn't have the correct file extension
        IndexError: if file is not formatted correctly
        ValueError: if file is not formatted correctly
    '''
    plotter = _SurfacePlotter(filename)
    plotter.plot_interactive()


if __name__ == '__main__':
    '''
    This module can be used as a script to plot 2D-surfaces from a \'.srf\' file

        USAGE: $ python3 plot.py [filename of .srf file]

    If no filename is specified the default name 'trench.srf_save' will be used.
    '''
    if(len(sys.argv) >= 2):
        plot(sys.argv[1])
    else:
        print('plot.py: no file specified! Using default file.')
        plot('work/Aufgabe3_plot/trench.srf_save')
