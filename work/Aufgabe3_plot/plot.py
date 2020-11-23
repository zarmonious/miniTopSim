'''
Functions for creating an interactive plot of a 2D-surface with the data of a .srf file.

This module offers functionality to create an interactive matplotlib-plot of a 2D-surface with the
data from a .srf file.  To create a plot you have to invoke the \'plot(filename)\' function. 
Internally a private class is used to handle the plotting.

The .srf file is expected to have the following format and can also include multiple surfaces:
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
    USAGE: $ python3 plot.py [path to .srf file]

Classes:
    WrongFileExtensionError: Exception that gets raised if the passed file doesn't have the correct FileExtension

Functions:
    plot(filename): plots the surface passed by the .srf file

Author: Haberl Alexander
Part of the miniTopSim Project: 
'''


import os
import sys
import numpy as np
import matplotlib.pyplot as plt
# The _SurfacePlotter class overwrites the default plt keybindings. 
# When overwriting some of these keybindings, matplotlib prints a warning message, because they are 
# bound to functions that will be removed in later matplotlib versions. 
# The following lines stop these warnings from being printed and cluttering the terminal.
#
# Note: for later matplotlib releases we might have to remove the following line from 
# the _SurfacePlotter class:
#       'plt.rcParams['keymap.all_axes'] =''
#import warnings
#import matplotlib.cbook
#warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#


class _SurfacePlotter:
    '''
    Private class that handles the plotting. This class should not be used outside of this module.
    If you want to plot a .srf file use the function \'plot(filename)\' instead!
    '''

    def __init__(self, filename):
        self.filename = filename
        self.xPointsList = list()
        self.yPointsList = list()
        self.timeList = list()
        self.nPointList = list()
        self.surfaceIndex = 0
        self.forwardDirectory = True
        self.length = 0
        self.aspectRatioAuto = True
        self.deletePlotMode = True
        self.stepSize = 1
        self.boundaryModeAuto = True
        self.yLim = 0
        self.alreadyPlottedList = None
        plt.rcParams['keymap.fullscreen'] = ['ctrl+f']
        plt.rcParams['keymap.yscale'] = ['ctrl+l']
        plt.rcParams['keymap.home'] = ['h','home']
        plt.rcParams['keymap.all_axes'] = ''
        plt.rcParams['keymap.save'] = ['ctrl+s']
        plt.rcParams['keymap.quit'] = ['ctrl+w','cmd+w']

    def read_srf_file(self):
        with  open(self.filename) as file:
            if (self.filename.endswith(('.srf_save', '.srf')) == False):
                raise WrongFileExtensionError('plot.py:    Expected \'.srf\' or \'.srf_save\' file')
            
            xPoints = None
            yPoints = None
            i=0

            for line in file:
                if 'surface:' in line:
                    stringArray = line.split(' ')
                    self.timeList.append(float(stringArray[1]))
                    self.nPointList.append(int(stringArray[2]))
                    xPoints = np.empty(self.nPointList[i], dtype=np.float64)
                    yPoints = np.empty(self.nPointList[i], dtype=np.float64)
                    self.xPointsList.append(xPoints)
                    self.yPointsList.append(yPoints)
                    i=i+1
                    j=0
                else:
                    stringArray = line.split(' ')
                    xPoints[j] = float(stringArray[0])
                    yPoints[j] = float(stringArray[1])
                    j=j+1
            self.length = i
            self.alreadyPlottedList = [False] * self.length

    def on_key_press(self, event):
        if(event.key == 'l'):
            lastElementIndex = self.length - 1
            self.surfaceIndex = lastElementIndex

        elif(event.key == 'f'):
            self.surfaceIndex = 0
        
        elif(event.key == ' '):
            if(self.forwardDirectory == True):
                self.surfaceIndex = self.surfaceIndex + self.stepSize
                if(self.surfaceIndex >= self.length):
                    self.surfaceIndex = 0

            else:
                self.surfaceIndex = self.surfaceIndex - self.stepSize
                if(self.surfaceIndex <= -1):
                    self.surfaceIndex = self.length - 1

        elif(event.key == 'r'):
            self.forwardDirectory = not self.forwardDirectory
            return

        elif(event.key == 'a'):
            self.aspectRatioAuto = not self.aspectRatioAuto
        
        elif(event.key == 'd'):
            self.deletePlotMode = not self.deletePlotMode
            return
        
        elif(event.key == 's'):
            fname = self.filename.split('.')
            fname = fname[0] + '.png'
            plt.savefig(fname)
            return
        
        elif(event.key == 'b'):
            self.boundaryModeAuto = not self.boundaryModeAuto
            if(self.boundaryModeAuto == False):
                    ax = plt.gca()
                    self.ylim = ax.get_ylim()

        elif(event.key == 'q'):
            plt.close('all')
            return 
        
        elif(event.key.isnumeric() == True):
            self.stepSize = 2 ** int(event.key)
            return

        self.update_plot()
        return None


    def update_plot(self):
        if(self.deletePlotMode == True):
            plt.clf()
            for i in range(self.length):
                self.alreadyPlottedList[i] = False
            

        if(self.alreadyPlottedList[self.surfaceIndex] == False):
            plt.plot(self.xPointsList[self.surfaceIndex], self.yPointsList[self.surfaceIndex], 
                label = 't = ' + str(self.timeList[self.surfaceIndex]) + 's')
            self.alreadyPlottedList[self.surfaceIndex] = True

        if(self.boundaryModeAuto != True):
            plt.ylim(self.ylim)
        if(self.aspectRatioAuto != True):
            ax = plt.gca()
            ax.set_aspect(aspect = 1)
        plt.title("2D-Plot der Oberfläche")
        plt.legend()
        plt.xlabel('x in nm')
        plt.ylabel('y in nm')
        plt.grid(True, 'both', 'both')
        plt.draw()

    def plot_interactive(self):
        '''

        '''
        self.read_srf_file()
        fig = plt.figure()
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.update_plot()
        plt.show()


class WrongFileExtensionError(Exception):
    pass


def plot(filename):
    plotter = _SurfacePlotter(filename)
    plotter.plot_interactive()


if __name__ == '__main__':
    if(len(sys.argv) >= 2):
        plot(sys.argv[1])
    else:
        print('plot.py: no file specified! Using default file.')
        plot('trench.srf_save')

