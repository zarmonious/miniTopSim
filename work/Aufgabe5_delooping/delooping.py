"""
Script to test basic delooping to be implemented in the project.
This should be a standalone file
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import TestingSurfaces


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


def create_matrix(points):
    compare_matrix = np.zeros(
        (int((np.size(points) / 2) - 2), int((np.size(points) / 2) - 2)),
        Segment_pair)
    for i, pointi in enumerate(points):
        if i < int((np.size(points) / 2) - 1):
            pointiplusone = points[i + 1, :]
            for j, pointj in enumerate(points):
                if j > i and j < int((np.size(points) / 2) - 1):
                    pointjplusone = points[j + 1, :]
                    compare_matrix[i, j - 1] = Segment_pair(pointi,
                                                            pointiplusone,
                                                            pointj,
                                                            pointjplusone)
    return compare_matrix


def intersectionPoint2(points, result, i, j):
    newpoint = points[i, :] + (points[i + 1, :] - points[i, :]) * result[0, 0]
    return np.reshape(newpoint, (1, 2))


def compare_segments(segment_pair):
    a = [[segment_pair.x12 - segment_pair.x11,
          -segment_pair.x22 + segment_pair.x21],
         [segment_pair.y12 - segment_pair.y11,
          -segment_pair.y22 + segment_pair.y21]]

    b = [[segment_pair.x21 - segment_pair.x11],
         [segment_pair.y21 - segment_pair.y11]]
    erg = np.linalg.solve(a, b)

    if 0 < erg[0] < 1 and 0 < erg[1] < 1:
        return np.transpose(erg)


def removelooppoints2(restult_list, points):
    for intersection in restult_list:
        intervall = np.arange(int(intersection[2]), int(intersection[3]))
        for element in intervall:
            points[element, :] = np.array((None, None))
    return points


def insertintersectionpoint2(result_list, points_noloop):
    for intersection in result_list:
        points_noloop[int(intersection[2]), :] = intersection[:2]
    return points_noloop


def removeflaged(points):
    intervall = np.zeros((1, 0), dtype=int)
    for i, point in enumerate(points):
        if np.isnan(point[0]):
            intervall = np.append(intervall, i)
    points = np.delete(points, (intervall), axis=0)
    return points

def deloop2(points):
    """Hier wird versucht das ganze als whole array operationen zu machen"""
    print('Strart deloop2')
    # Die Matrix der Vergleichspunkte füllen
    compare_matrix = create_matrix(points)
    result_list = np.zeros((0, 4), dtype=float)
    for i, j in np.ndindex(compare_matrix.shape):
        if compare_matrix[i, j] != 0:
            print(compare_matrix[i, j])
            result = compare_segments(compare_matrix[i, j])
            if result is not None:
                newpoint = intersectionPoint2(points, result, i, j)
                indexarray = np.array((i + 1, j + 2)).reshape((1, 2))
                resultij = np.concatenate((newpoint, indexarray), axis=1)
                result_list = np.concatenate((result_list, resultij))
    result_list = np.flip(result_list, axis=0)
    points_noloop = removelooppoints2(result_list, points)
    points = insertintersectionpoint2(result_list, points_noloop)
    points = removeflaged((points))
    return points


def intersectionPoint(workingpoint, workingpointplusone, erg):
    newpoint = workingpoint + (workingpointplusone - workingpoint) * erg[0]
    print('This is the new Point inserted: {}'.format(newpoint))
    return newpoint


def removelooppoints(p, start, end):
    print('i = {}, j = {}'.format(start, end))
    intervall = np.arange(start + 1, end + 1)
    p = np.delete(p, intervall, axis=0)
    return p


def insertIntersectionPoint(deloopedsurface, newpoint, place):
    print('This is the new delooped surface:')
    print(deloopedsurface)
    print(place)
    newsurface = np.insert(deloopedsurface, place, newpoint, axis=0)
    print(newsurface)
    return newsurface


def deloop(p):
    """Nimm zuerst die ersten beiden Punkte und dieser Streckenabschnitt wird mit den anderen auf einen Schnittpunkt
    verglichen"""

    for i, workingpoint in enumerate(p):
        if i < np.size(p) / 2 - 1:
            workingpointplusone = p[i + 1, :]
            for j, movingpoint in enumerate(p):
                if i == j:
                    continue
                if j < np.size(p) / 2 - 1:
                    movingpointplusone = p[j + 1]
                    a = np.transpose(np.array(
                        [workingpointplusone - workingpoint,
                         -movingpointplusone + movingpoint]))
                    b = (np.array(movingpoint - workingpoint))
                    # print('a = {}'.format(a))
                    # print('b = {}'.format(b))
                    erg = np.linalg.solve(a, np.transpose(b))
                    if 0 < erg[0] < 1 and 0 < erg[1] < 1:
                        """Du hast eine Intersection gefunden! Entferne Sie doch bitte"""
                        newpoint = intersectionPoint(workingpoint,
                                                     workingpointplusone, erg)
                        print('These are the 2 sections:')
                        print(p[i, :])
                        print(p[j, :])
                        print('This is the old surface:')
                        print(p)
                        deloopedsurface = removelooppoints(p, i, j)

                        p = insertIntersectionPoint(deloopedsurface, newpoint,
                                                    i + 1)
                        print('This is the new surface!!')
                        print(p)
                        print('Kreuzung')
                        print('Ergebnis = {}'.format(erg))
                        # plt.plot(p[:, 0], p[:, 1], 'b+-', label='Surfacepoints')
                        # plt.show()
                        print('This is before the continue:')
                        print(p)
                        print('i = {}'.format(i))
                        print('j = {}'.format(j))

                        return p
                        # removeIntersection(workingpoint, workingpointplusone, movingpoint, movingpointplusone, erg)

                    # print(erg[0])
                    # print(erg[1])
                    # print('Ergebnis = {}'.format(erg))
                    # ergebnis = np.linalg.solve(np.transpose(np.array(workingpointplusone - workingpoint), np.array(-movingpointplusone + movingpoint)), np.array(movingpoint - workingpoint))
                    # print(ergebnis)
                    # if ergebnis[0] <= 1:
                    #    print(ergebnis)

        # np.linalg.solve(np.transpose(np.array(workingpointplusone - workingpoint, - )))
        # np.linalg.solve(np.transpose(np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]])), (np.array(p[1, :] - p[0, :])))

        print('xxxxxxxxxxxxxx')
    global deloopagain
    deloopagain = False
    return p


""" In zweidimensionalen Numpy Arrays werden die Punkte gespeichert
x0 y0
x1 y1
x2 y2
x3 y3
"""

surface = TestingSurfaces.p3
surfaceold = np.copy(TestingSurfaces.p3)

plt.plot(surface[:, 0], surface[:, 1], 'b+-', label='Surfacepoints')
plt.show()
deloopagain = True

start_time = time.time()
deloopedsurface2 = deloop2(surface)
stop_time = time.time()
print(float(stop_time-start_time))

plt.plot(surfaceold[:, 0], surfaceold[:, 1], 'b+-', label='Surfacepoints')
plt.plot(deloopedsurface2[:, 0], deloopedsurface2[:, 1], 'k*-', label='Delooped Surface')
plt.grid()
plt.show()
