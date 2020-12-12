"""
Defines the class Surface

includes function
"normal_vector" calculates the normal vectors in every point of the surface
"plot" which plots the surface
"write" which writes the surface points into a .srf file
"""
import numpy as np
#import init_surface as init
import matplotlib.pyplot as plt
import TestingSurfaces

#import parameters as par


class Segment_pair:
    def __init__(self, p11, p12, p21, p22):
        self.x11 = p11[0]
        self.y11 = p11[1]
        self.x12 = p12[0]
        self.y12 = p12[1]
        self.x21 = p21[0]
        self.y21 = p21[1]
        self.x22 = p22[0]
        self.y22 = p22[1]


class Surface:

    def __init__(self, x, y):
        """
        Initializes the x and y-Values with the init_surface module
        """
        self.xvals = x
        self.yvals = y

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
        plt.show()

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
        self.points = np.concatenate((self.xvals.reshape((self.xvals.size, 1)),
                                      self.yvals.reshape((self.xvals.size, 1))),
                                     axis=1)

    def _intersections(self, result):

        zeroes = np.zeros(result.shape)
        ones = np.ones(result.shape)
        first_row = zeroes < result
        #print(first_row)
        second_row = result < ones
        #print(second_row)
        intersection = first_row == second_row
        result_bool = np.logical_and(intersection[:, 0], intersection[:, 1])
        return result_bool

    def _calculate_new_points(self, results, result_bool):
        self.newpoints = np.zeros((self.further_information.shape))
        self.newpoints[:] = np.NaN
        for k, result in enumerate(results):
            if result_bool[k]:
                i = int(self.further_information[k, 0])
                j = int(self.further_information[k, 1])
                #print('i= {}'.format(i))
                #print('j = {}'.format(j))
                #print('point = {}'.format(self.points[i]))
                self.newpoints[k] = self.points[i] + (self.points[i + 1] -
                                                self.points[i]) * result[0]
        #print('new points = {}'.format(self.newpoints))


    def _setvals(self):
        self.xvals = self.points[:, 0]
        self.yvals = self.points[:, 1]

    def _create_matrix(self):

        self.number_of_segments = (int(self.points.size / 2) - 1)
        self.number_of_pairs = int(
            self.number_of_segments ** 2 / 2 + self.number_of_segments / 2)
        self.a = np.zeros((self.number_of_pairs, 2, 2))
        self.b = np.zeros((self.number_of_pairs, 2, 1))
        self.further_information = np.zeros(
            ((int(self.points.size / 2) - 1) ** 2, 2))

        self.k = 0
        for i, pointi in enumerate(self.points):
            if i < int(self.points.size / 2) - 1:
                pointiplusone = self.points[i + 1, :]
                for j, pointj in enumerate(self.points):
                    if i + 1 < j and j < int(self.points.size / 2) - 1:
                        #print('k = {}'.format(self.k))
                        pointjplusone = self.points[j + 1, :]
                        element = (
                            pointiplusone - pointi, -pointjplusone + pointj)
                        if np.linalg.det(np.transpose(element)) != 0:
                            self.a[self.k] = np.transpose(element)
                            self.b[self.k] = (pointj - pointi).reshape(2, 1)
                            self.further_information[self.k] = (i, j)
                            self.k = self.k + 1

    def _compare_segments(self, segment_pair):
        a = [[segment_pair.x12 - segment_pair.x11,
              -segment_pair.x22 + segment_pair.x21],
             [segment_pair.y12 - segment_pair.y11,
              -segment_pair.y22 + segment_pair.y21]]

        b = [[segment_pair.x21 - segment_pair.x11],
             [segment_pair.y21 - segment_pair.y11]]
        # print('Checking for intersection!')
        # print('a is: {}'.format(a))
        # print('Determinat is: {}'.format(np.linalg.det(a)))
        if np.linalg.det(a) != 0:
            # print('Determinat is non Zero')
            erg = np.linalg.solve(a, b)
            if 0 < erg[0] < 1 and 0 < erg[1] < 1:
                # print('Intersection found!')
                return np.transpose(erg)

    def _intersectionpoint(self, result, i, j):
        newpoint = self.points[i, :] + (
                self.points[i + 1, :] - self.points[i, :]
        ) * result[0, 0]
        # print('new Point: {}'.format(newpoint))
        return np.reshape(newpoint, (1, 2))

    def _flaglooppoints(self, result_bool):

        for k, intersection in enumerate(result_bool):
            if intersection:
                i = int(self.further_information[k, 0])
                j = int(self.further_information[k, 1])
                intervall = np.arange(i+1, j+1)
                for element in intervall:
                    self.points[element, :] = np.array((None, None))

    def _insertintersectionpoint(self, result_bool):
        for k, newpoint in enumerate(self.newpoints):
            if not np.isnan(newpoint[0]):
                i = int(self.further_information[k, 0])
                j = int(self.further_information[k, 1])
                #print('k = {}'.format(k))
                #print('i= {}'.format(i))
                #print('j = {}'.format(j))
                #print('newpoint = {}'.format(newpoint))
                self.points[i+1] = newpoint

    def _removeflaged(self):
        intervall = np.zeros((1, 0), dtype=int)
        for i, point in enumerate(self.points):
            if np.isnan(point[0]):
                intervall = np.append(intervall, i)
        self.points = np.delete(self.points, intervall, axis=0)

    def deloop(self):
        """This method removes the loopes created by advancing the simulation

        format:

        :param <>:
        """
        # print('Entering deloop!')
        # print('in deloop yvals : {}'.format(self.yvals))
        # print(self.xvals.reshape((self.xvals.size, 1)).shape)
        # (self.points)
        self._update_points()
        print('Before deloop = {}'.format(self.points))
        self._create_matrix()
        # print('Compare Matrix shape: {}'.format(compare_matrix.shape))
        # print(compare_matrix[0,0].x11)
        # print(compare_matrix[0, 0].y11)
        print('a = {}'.format(self.a[:self.k]))
        print('b = {}'.format(self.b[:self.k]))
        result = np.linalg.solve(self.a[:self.k], self.b[:self.k])
        print('result  = {}'.format(result))
        print('further_information  = {}'.format(self.further_information))
        print('result shape = {}'.format(result.shape))
        print('further_information shape = {}'.format(self.further_information.shape))
        print('k = {}'.format(self.k))
        result_bool = self._intersections(result)
        print('The result_bool is: {}'.format(result_bool))
        self._calculate_new_points(result, result_bool)
        print('new calculated points = {}'.format(self.newpoints))
        self._flaglooppoints(result_bool)
        print('show flaged points = {}'.format(self.points))

        # print('points after inserting none outside the method: {}'.format(self.points))
        self._insertintersectionpoint(result_bool)
        #print('number of points = {}'.format(self.points.shape))
        #print('number of xvals = {}'.format(self.xvals.shape))
        self._removeflaged()
        self._setvals()
        print('After deloop = {}'.format(self.points))

surface = Surface(TestingSurfaces.x, TestingSurfaces.y)
plt.plot(surface.xvals, surface.yvals, "x-", label=f"t = {1}")
plt.title('Surface')
plt.xlabel('x[nm]')
plt.ylabel('y[nm]')

surface.deloop()
plt.plot(surface.xvals, surface.yvals, "x-", label=f"t = {1}")
plt.show()

