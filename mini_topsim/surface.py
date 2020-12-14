"""
Defines the class Surface

includes function 
"normal_vector" calculates the normal vectors in every point of the surface
"plot" which plots the surface
"write" which writes the surface points into a .srf file
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import init_surface as init
from numpy import arccos, dot, pi, cross
from numpy.linalg import norm

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
    
    def eliminate_overhangs(self):
        """
        Eliminates overhanging structures iteratively
        """        
        #from left to right
        for index in range(0, len(self.xvals)-1):
            if (self.xvals[index] > self.xvals[index+1] and
            self.yvals[index] < self.yvals[index+1]):
                    self.xvals[index+1] = self.xvals[index]

        #from right to left        
        for index in range(len(self.xvals)-1, 0,-1):
            if (self.xvals[index] < self.xvals[index-1] and
            self.yvals[index-1] > self.yvals[index]):
                self.xvals[index-1] = self.xvals[index]


    def _update_points(self):
        """updates the points of the Object for further calculations"""

        self.points = np.concatenate((self.xvals.reshape((self.xvals.size, 1)),
                                      self.yvals.reshape((self.xvals.size, 1))),
                                     axis=1)

    def _intersections(self, _results):
        """determines if an intersection has occured and returns a bool array

        :param _results: numpy array of all the results for the intersections
        :returns _result_bool: numpy array where TRUE indicates an intersection
        and FALSE indicates no intersection in the interested part
        """
        zeroes = np.zeros(_results.shape)
        ones = np.ones(_results.shape)
        first_column = zeroes < _results
        #print(first_column)
        second_column = _results < ones
        #print(second_column)
        intersection = first_column == second_column
        #print(intersection)
        _result_bool = np.logical_and(intersection[:, 0], intersection[:, 1])
        return _result_bool

    def _calculate_new_points(self, _results, _result_bool):
        """calculates the points of intersection

        :param _results: contains the results of all compared segments as numpy
        array
        :param _result_bool: contains the information if there was an
        intersection or not as bool value
        """
        self._newpoints = np.zeros(self._further_information.shape)
        self._newpoints[:] = np.NaN
        for k, result in enumerate(_results):
            if _result_bool[k]:
                i = self._further_information[k, 0]
                # print('i= {}'.format(i))
                # print('point = {}'.format(self.points[i]))
                self._newpoints[k] = self.points[i] + (self.points[i + 1] -
                                                      self.points[i]) * result[
                                                                             0]
        # print('new points = {}'.format(self._newpoints))

    def _setvals(self):
        """writes the x and y yalues back"""
        self.xvals = self.points[:, 0]
        self.yvals = self.points[:, 1]

    def _create_matrices(self):
        """creates the two matrices a and b so that a*x=b can be solved

        For each Segment Pair that has to be compared there is an entry in a and
        b to solve the linear equation system a*x=b.
        """
        number_of_segments = (int(self.points.size / 2) - 1)
        number_of_pairs = int(
            (number_of_segments ** 2) / 2 + number_of_segments / 2)
        self._a = np.zeros((number_of_pairs, 2, 2))
        self._b = np.zeros((number_of_pairs, 2, 1))
        self._further_information = np.zeros(
            ((int(self.points.size / 2) - 1) ** 2, 2), dtype=int)
        self._k = 0

        for i, pointi in enumerate(self.points):
            if i < number_of_segments:
                pointiplusone = self.points[i + 1]
                for j, pointj in enumerate(self.points):
                    if i + 1 < j and j < number_of_segments:
                        # print('k = {}'.format(self._k))
                        pointjplusone = self.points[j + 1]
                        element = np.transpose((
                            pointiplusone - pointi, -pointjplusone + pointj))
                        if np.linalg.det(element) != 0:
                            self._a[self._k] = element
                            self._b[self._k] = (pointj - pointi).reshape(2, 1)
                            self._further_information[self._k] = (i, j)
                            self._k = self._k + 1

    def _flaglooppoints(self, _result_bool):
        """Flags entries in self.points with None if they should be removed

        If there is an intersection of two segments there is an interval of
        points witch should be removed. Flagging them makes it possible to
        enter the new points in the right position.

        :param result_bool: contains the information if there was an
        intersection or not as bool value
        """

        for k, intersection in enumerate(_result_bool):
            if intersection:
                i = self._further_information[k, 0]
                j = self._further_information[k, 1]
                interval = np.arange(i + 1, j + 1)
                for point_index in interval:
                    self.points[point_index] = np.array((None, None))

    def _insertintersectionpoints(self):
        """inserts the new points in the corresponding place"""

        for k, newpoint in enumerate(self._newpoints):
            if not np.isnan(newpoint[0]):
                i = self._further_information[k, 0]
                # print('k = {}'.format(k))
                # print('i= {}'.format(i))
                # print('newpoint = {}'.format(newpoint))
                self.points[i + 1] = newpoint

    def _removeflaged(self):
        """removes the remaining Flaged points"""

        interval = np.zeros((1, 0), dtype=int)
        for i, point in enumerate(self.points):
            if np.isnan(point[0]):
                interval = np.append(interval, i)
        self.points = np.delete(self.points, interval, axis=0)

    def deloop(self):
        """This method removes the loopes created by advancing the simulation.

        When the surface is changed there is a chance that loops are created.
        Those are detected and removed by calculating the intersection point
        and adding it and removing the loop points. So the total number of
        points can change.
        """
        self._update_points()
        self._create_matrices()
        _results = np.linalg.solve(self._a[:self._k], self._b[:self._k])
        _result_bool = self._intersections(_results)
        self._calculate_new_points(_results, _result_bool)
        self._flaglooppoints(_result_bool)
        self._insertintersectionpoints()
        self._removeflaged()
        self._setvals()
    def distance(self, refsrf):
        """
        calculates the distance to a reference surface 
                
        :param refsrf: reference surface object
        """
        distances12 = np.zeros_like(self.xvals)
        distances21 = np.zeros_like(refsrf.xvals)
        
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
