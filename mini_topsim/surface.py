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
from numpy import arccos, dot, pi, cross
from numpy.linalg import norm

import parameters as par

class Surface:

    def __init__(self):
        """
        Initializes the x and y-Values with the init_surface module
        """
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
    
    def distance(self, refsrf):
        """
        calculates the distance to a reference surface 
                
        :param refsrf: reference surface object
        """
        distances12 = np.zeros_like(self.xvals)
        distances21 = np.zeros_like(self.xvals)
        
        tmp = np.zeros(len(refsrf.xvals)-1)
        for i in range(len(self.xvals)):
            p = [self.xvals[i], self.yvals[i]]
            for j in range(len(refsrf.xvals)-1):
                seg = np.asarray([[refsrf.xvals[j], refsrf.yvals[j]], 
                       [refsrf.xvals[j+1], refsrf.yvals[j+1]]])
                tmp[j] = point2segment_dist(p, seg)
            distances12[i] = min((np.abs(tmp)))
            
        del tmp
        tmp = np.zeros(len(self.xvals)-1)      
        for i in range(len(refsrf.xvals)):
            p = [refsrf.xvals[i], refsrf.yvals[i]]
            for j in range(len(self.xvals)-1):
                seg = np.asarray([[self.xvals[j], self.yvals[j]], 
                       [self.xvals[j+1], self.yvals[j+1]]])
                tmp[j] = point2segment_dist(p, seg)
            distances21[i] = min((np.abs(tmp)))
            
        return (np.mean(distances12) + np.mean(distances21))/2
            
def point2segment_dist(p, seg):
    """
    calculates the distance between a point and a surface segment.

    If point projects onto the line segment, the orthogonal distance
    from the point to the line is returned.
    If the point does not project to the line segment, the distances
    to both segment endpoints is calculated and take the shortest 
    distance is returned.

    :param point: Numpy array p=[x,y]
    :param line: list of segment endpoints [pstart, pend]=[[x1,y1],[x2,y2]]
    :return: The minimum distance between point and surface segment.
    """
    start = seg[0]
    end = seg[1]
    if all(start == p) or all(end == p):
        return 0
    if arccos(round(dot((p - start) / norm(p - start),
        (end - start) / norm(end - start)), 8)) > pi / 2:
        return norm(p - start)
    if arccos(round(dot((p - end) / norm(p - end), 
        (start - end) / norm(start - end)), 8)) > pi / 2:
        return norm(p - end)
    return norm(cross(start - end, start - p))/norm(end-start)