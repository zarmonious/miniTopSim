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

    def _update_points(self):
        """TODO: Dockstring"""
        self.points = np.concatenate((self.xvals.reshape((self.xvals.size, 1)),
                                      self.yvals.reshape((self.xvals.size, 1))),
                                     axis=1)

    def _intersections(self, result):
        """TODO: Dockstring"""
        zeroes = np.zeros(result.shape)
        ones = np.ones(result.shape)
        first_column = zeroes < result
        #print(first_column)
        second_column = result < ones
        #print(second_column)
        intersection = first_column == second_column
        #print(intersection)
        result_bool = np.logical_and(intersection[:, 0], intersection[:, 1])
        return result_bool

    def _calculate_new_points(self, results, result_bool):
        """TODO: Dockstring"""
        self.newpoints = np.zeros(self.further_information.shape)
        self.newpoints[:] = np.NaN
        for k, result in enumerate(results):
            if result_bool[k]:
                i = self.further_information[k, 0]
                # print('i= {}'.format(i))
                # print('point = {}'.format(self.points[i]))
                self.newpoints[k] = self.points[i] + (self.points[i + 1] -
                                                      self.points[i]) * result[
                                                                             0]
        # print('new points = {}'.format(self.newpoints))

    def _setvals(self):
        """TODO: Dockstring"""
        self.xvals = self.points[:, 0]
        self.yvals = self.points[:, 1]

    def _create_matrices(self):
        """TODO: Dockstring"""
        number_of_segments = (int(self.points.size / 2) - 1)
        number_of_pairs = int(
            (number_of_segments ** 2) / 2 + number_of_segments / 2)
        self.a = np.zeros((number_of_pairs, 2, 2))
        self.b = np.zeros((number_of_pairs, 2, 1))
        self.further_information = np.zeros(
            ((int(self.points.size / 2) - 1) ** 2, 2), dtype=int)
        self.k = 0

        for i, pointi in enumerate(self.points):
            if i < number_of_segments:
                pointiplusone = self.points[i + 1]
                for j, pointj in enumerate(self.points):
                    if i + 1 < j and j < number_of_segments:
                        # print('k = {}'.format(self.k))
                        pointjplusone = self.points[j + 1]
                        element = np.transpose((
                            pointiplusone - pointi, -pointjplusone + pointj))
                        if np.linalg.det(element) != 0:
                            self.a[self.k] = element
                            self.b[self.k] = (pointj - pointi).reshape(2, 1)
                            self.further_information[self.k] = (i, j)
                            self.k = self.k + 1

    def _flaglooppoints(self, result_bool):
        """TODO: Dockstring"""
        for k, intersection in enumerate(result_bool):
            if intersection:
                i = self.further_information[k, 0]
                j = self.further_information[k, 1]
                interval = np.arange(i + 1, j + 1)
                for point_index in interval:
                    self.points[point_index] = np.array((None, None))

    def _insertintersectionpoints(self, result_bool):
        """TODO: Dockstring"""
        for k, newpoint in enumerate(self.newpoints):
            if not np.isnan(newpoint[0]):
                i = self.further_information[k, 0]
                # print('k = {}'.format(k))
                # print('i= {}'.format(i))
                # print('newpoint = {}'.format(newpoint))
                self.points[i + 1] = newpoint

    def _removeflaged(self):
        """TODO: Dockstring"""
        interval = np.zeros((1, 0), dtype=int)
        for i, point in enumerate(self.points):
            if np.isnan(point[0]):
                interval = np.append(interval, i)
        self.points = np.delete(self.points, interval, axis=0)

    def deloop(self):
        """This method removes the loopes created by advancing the simulation

        format:

        :param <>:
        """
        self._update_points()
        self._create_matrices()
        result = np.linalg.solve(self.a[:self.k], self.b[:self.k])
        result_bool = self._intersections(result)
        self._calculate_new_points(result, result_bool)
        self._flaglooppoints(result_bool)
        self._insertintersectionpoints(result_bool)
        self._removeflaged()
        self._setvals()
