"""
Defines the class Surface

includes function 
"normal_vector" which calculates the normal vectors in every point of the surface
"plot" which plots the surface
"write" which writes the surface points into a .srf file
"""
import numpy as np
import init_surface
import matplotlib.pyplot as plt


class Surface:

    def __init__(self):
        """
        Initializes the x and y-Values with the init_surface module
        """
        self.xVals = np.arange(-50., 51., 1.)
        self.yVals = init_surface.init_surface(self.xVals)

    def normal_vector(self):
        """
        calculates the normal vectors in every point of the surface

        calculates the vector between the nearest neigbours of the point
        and returns the normal vector of it

        :returns: x Values, y Values of the normal vectors
        """
        x = np.zeros_like(self.xVals)
        y = np.zeros_like(self.yVals)

        #start and endpoint only have one neighbor 
        x[0] = self.xVals[1] - self.xVals[0]
        y[0] = self.yVals[1] - self.yVals[0]
        x[-1] = self.xVals[-1] - self.xVals[-2]
        y[-1] = self.yVals[-1] - self.yVals[-2]


        #right neigbour - left neigbour
        y[1:-1] = np.array(self.yVals[2::] - self.yVals[:-2:])
        x[1:-1] = np.array(self.xVals[2::] - self.xVals[:-2:])

        magnitude = np.linalg.norm([x, y], axis=0)

        return (y / magnitude), (-x / magnitude)

    def plot(self, time):
        """
        plots the surface

        :param time: current simulation time
        """
        plt.plot(self.xVals, self.yVals, "x-", label=f"t = {time}")
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
            f.write(f"surface: {time} {len(self.xVals)} x-positions y-positions\n")
            for x, y in zip(self.xVals, self.yVals):
                f.write(f"{x} {y}\n")