"""
Defines the class Surface

includes function 
"normal_vector" calculates the normal vectors in every point of the surface
"plot" which plots the surface
"write" which writes the surface points into a .srf file
"""
import numpy as np
import init_surface as init
import matplotlib.pyplot as plt
import os

import parameters as par

class Surface:

    def __init__(self):
        """
        Initializes the x and y-Values with the init_surface module
        """
        if par.INITIAL_SURFACE_TYPE == 'File':          
            
            srf_file = par.INITIAL_SURFACE_FILE
            self.xvals, self.yvals = init.read_srf_file(srf_file, 
                                                        par.TOTAL_TIME)

        else:    
            self.xvals = np.arange(par.XMIN, par.XMAX + 1, par.DELTA_X)
            self.yvals = init.init_surface(self.xvals)

    def normal_vector(self):
        """
        calculates the normal vectors in every point of the surface

        calculates the vector between the nearest neigbours of the point
        and returns the normal vector of it

        :returns: x Values, y Values of the normal vectors
        """
        dx = np.zeros_like(self.xvals)
        dy = np.zeros_like(self.yvals)

        # start and endpoint only have one neighbor
        dx[0] = self.xvals[1] - self.xvals[0]
        dy[0] = self.yvals[1] - self.yvals[0]
        dx[-1] = self.xvals[-1] - self.xvals[-2]
        dy[-1] = self.yvals[-1] - self.yvals[-2]

        # right neigbour - left neigbour
        dy[1:-1] = self.yvals[2:] - self.yvals[:-2]
        dx[1:-1] = self.xvals[2:] - self.xvals[:-2]

        magnitude = np.linalg.norm([dx, dy], axis=0)

        nx = dy / magnitude
        ny = -dx / magnitude
        return nx, ny

    def plot(self, time):
        """
        plots the surface

        :param time: current simulation time
        """
        plt.plot(self.xvals, self.yvals, "x-", label=f"t = {time}")
        plt.title('Surface')
        plt.xlabel('x[nm]')
        plt.ylabel('y[nm]')

    def write(self, time, filename):
        """
        writes the surface values into an srf file

        format: surface: <time> <npoints> x-positions y-positions
                x[0] y[0]

        :param time: current simulation time
        :param filename: name of the file
        """
        with open(filename, 'a') as f:
            f.write(
                f"surface: {time} {len(self.xvals)} x-positions y-positions\n")
            for x, y in zip(self.xvals, self.yvals):
                f.write(f"{x} {y}\n")
