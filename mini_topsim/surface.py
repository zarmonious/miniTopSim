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
        self.points = np.concatenate((self.xvals.reshape((self.xvals.size, 1)),
                                      self.yvals.reshape((self.xvals.size, 1))),
                                     axis=1)
    def _setvals(self):
        self.xvals = self.points[:, 0]
        self.yvals = self.points[:, 1]

    def _create_matrix(self):
        compare_matrix_a = np.zeros(
            (int(self.xvals.size - 2), int(self.xvals.size - 2)))
        compare_matrix_b = np.zeros((int(self.xvals-2), 1))
        #print('comparematrix shape : {}'.format(compare_matrix.shape))
        for i, pointi in enumerate(self.points):
            if i < int(self.xvals.size - 1):
                pointiplusone = self.points[i+1, :]
                for j, pointj in enumerate(self.points):
                    if j > i and j < int(self.xvals.size - 1):
                        pointjplusone = self.points[j + 1, :]
                        compare_matrix_a[i, j - 1] = np.concatenate((pointiplusone
                                    - pointi, -pointjplusone+pointj), axis=0)
                        #compare_matrix[i, j - 1] = Segment_pair(pointi,
                         #                                       pointiplusone,
                          #                                      pointj,
                           #                                     pointjplusone)
        compare_matrix_b[i] = np.concatenate(pointj - pointi)
        return compare_matrix_a, compare_matrix_b

    def _compare_segments(self, segment_pair):
        a = [[segment_pair.x12 - segment_pair.x11,
              -segment_pair.x22 + segment_pair.x21],
             [segment_pair.y12 - segment_pair.y11,
              -segment_pair.y22 + segment_pair.y21]]

        b = [[segment_pair.x21 - segment_pair.x11],
             [segment_pair.y21 - segment_pair.y11]]
        #print('Checking for intersection!')
        #print('a is: {}'.format(a))
        #print('Determinat is: {}'.format(np.linalg.det(a)))
        if np.linalg.det(a) != 0:
            #print('Determinat is non Zero')
            erg = np.linalg.solve(a, b)
            if 0 < erg[0] < 1 and 0 < erg[1] < 1:
                #print('Intersection found!')
                return np.transpose(erg)

    def _intersectionpoint(self, result, i, j):
        newpoint = self.points[i, :] + (self.points[i+1, :] - self.points[i, :]
                                        )* result[0, 0]
        #print('new Point: {}'.format(newpoint))
        return np.reshape(newpoint, (1, 2))

    def _removelooppoints(self, restult_list):
        for intersection in restult_list:
            intervall = np.arange(int(intersection[2]), int(intersection[3]))
            for element in intervall:
                self.points[element, :] = np.array((None, None))
                #print('points after inserting none: {}'.format(self.points))

    def _insertintersectionpoint(self, result_list):
        for intersection in result_list:
            self.points[int(intersection[2]), :] = intersection[:2]

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
        #print('Entering deloop!')
        #print('in deloop yvals : {}'.format(self.yvals))
        #print(self.xvals.reshape((self.xvals.size, 1)).shape)
        #(self.points)
        self._update_points()
        compare_matrix = self._create_matrix()
        #print('Compare Matrix shape: {}'.format(compare_matrix.shape))
        #print(compare_matrix[0,0].x11)
        #print(compare_matrix[0, 0].y11)
        result_list = np.zeros((0, 4), dtype=float)
        for i, j in np.ndindex(compare_matrix.shape):
            if compare_matrix[i, j] != 0:
                result = self._compare_segments(compare_matrix[i, j])
                if result is not None:
                    newpoint = self._intersectionpoint(result, i, j)
                    indexarray = np.array((i + 1, j + 2)).reshape((1, 2))
                    resultij = np.concatenate((newpoint, indexarray), axis=1)
                    result_list = np.concatenate((result_list, resultij))
        result_list = np.flip(result_list, axis=0)
        #print('The resultlist is: {}'.format(result_list))
        self._removelooppoints(result_list)
        #print('points after inserting none outside the method: {}'.format(self.points))
        self._insertintersectionpoint(result_list)
        self._removeflaged()
        self._setvals()



