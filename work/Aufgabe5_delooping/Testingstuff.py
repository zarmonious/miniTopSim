import numpy as np
from scipy import linalg
from time import time as t
import TestingSurfaces

def intersection(solution, further_information):
    zeroes = np.zeros(solution.shape)
    ones = np.ones(solution.shape)
    first_row = zeroes < solution
    print(first_row)
    second_row = solution < ones
    print(second_row)
    intersection = first_row == second_row
    result = np.logical_and(intersection[:, 0], intersection[:, 1])
    print(result)
class Segment_a:
    def __init__(self, p11, p12, p21, p22):
        self.x11 = p11[0]
        self.y11 = p11[1]
        self.x12 = p12[0]
        self.y12 = p12[1]
        self.x21 = p21[0]
        self.y21 = p21[1]
        self.x22 = p22[0]
        self.y22 = p22[1]
        self.a = np.array([[self.x12 - self.x11,
                   -self.x22 + self.x21],
                  [self.y12 - self.y11,
                   -self.y22 + self.y21]])

    def __call__(self):
        return self.a


class Segment_b:
    def __init__(self, p11, p21):
        self.x11 = p11[0]
        self.y11 = p11[1]
        self.x21 = p21[0]
        self.y21 = p21[1]
        self.b = np.array([[self.x21 - self.x11],
                  [self.y21 - self.y11]])

    def __call__(self):
        return self.b


Start_Time = t()
x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))
print(p)
print(np.size(p))
intervall = np.arange(2, 4)
print('Intervall = {}'.format(intervall))
print(np.delete(p, intervall, 0))
i = 0
print(np.array((3, 4)))
test = np.array((3, 4))
test = np.reshape(test, (1, 2))
print(test.shape)
while i < 10000:
    i += 1

newpoint = np.array([99, 99])
print(newpoint)

p = np.insert(p, 2, newpoint, axis=0)
print(p)

# intervall = np.arange(3, 5)
# for point in intervall:
#    print(point)
#    deloopedsurface = np.delete(p, point)
#    print(deloopedsurface)
#    print('XXXXXXXXXXXXXXXXXXXXXX')
print('Size of p = {}'.format(np.size(p) / 2))

testbool = True
print(testbool)
testbool = False
print(testbool)

Stop_Time = t()
print('++++++++++++++++')
print(Stop_Time - Start_Time)
print('//////////////////////')
print(x)
x = np.delete(x, (1, 3, 5), axis=0)
print(x)

point1 = np.array([2, 3]).reshape((1, 2))
point2 = np.array([3, 4]).reshape((1, 2))
point3 = np.array([6, 3]).reshape((1, 2))
point4 = np.array([3, 5]).reshape((1, 2))
point5 = np.array([6, 7]).reshape((1, 2))
points = np.concatenate((point1, point2, point3, point4, point5), axis=0)
restult = np.concatenate((point2 - point1, -point4 + point3), axis=0)

print(restult)

a1 = np.array([[1.0, 2.0], [3.0, 4.0]])
a2 = np.array([[2, 3], [5, 7]])
a3 = np.array([[1, 2], [3, 4]])
a4 = np.array([[1, 2], [3, 4]])
b1 = np.array([[1.0], [2.0]])
b2 = np.array([[5], [8]])
b3 = np.array([[5], [8]])
b4 = np.array([[5], [8]])
# a_versuch = np.array([a1, a2], [a3, a4])
# solution = np.linalg.solve(a_versuch, [[b1, b2], [b3, b4]])
# print('Solution:{}'.format(solution))
# print('shape:{}'.format(a_versuch.shape))
a_test = np.zeros((int(points.size / 2) - 1, int(points.size / 2) - 1),
                  Segment_a)
b_test = np.zeros((int(points.size / 2) - 1, int(points.size / 2) - 1),
                  Segment_b)

for i, pointi in enumerate(points):
    if i < int(points.size / 2) - 1:
        pointiplusone = points[i + 1, :]
        for j, pointj in enumerate(points):
            if i + 1 < j and j < int(points.size / 2) - 1:
                pointjplusone = points[j + 1, :]
                # element = (pointiplusone - pointi, -pointjplusone + pointj)
                print('shape/type = {}'.format(pointi.shape))
                element_a = Segment_a(pointi, pointiplusone, pointj,
                                    pointjplusone)
                print(element_a.a)
                if np.linalg.det(element_a()) != 0:
                    a_test[i, j] = element_a
                    print(
                        'b element:{}'.format((pointj - pointi).reshape(2, 1)))
                    element_b = Segment_b(pointi, pointj)
                    b_test[i, j] = element_b

print(a_test)
#erg = np.linalg.solve(a_test, b_test)
print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
points1 = TestingSurfaces.p
number_of_segments = (int(points1.size / 2) - 1)
number_of_pairs = int(number_of_segments**2/2+number_of_segments/2)
print('number of points in the test = {}'.format(points1.shape))
a = np.zeros((number_of_pairs, 2, 2))
b = np.zeros((number_of_pairs, 2, 1))
further_information = np.zeros(((int(points1.size / 2) - 1) ** 2, 2))
print(a.shape)
print('datatype of a1 = {}'.format(a1.dtype))
print(b.shape)

k = 0
for i, pointi in enumerate(points1):
    if i < int(points1.size / 2) - 1:
        pointiplusone = points1[i + 1, :]
        for j, pointj in enumerate(points1):
            if i + 1 < j and j < int(points1.size / 2) - 1:
                print('k = {}'.format(k))
                pointjplusone = points1[j + 1, :]
                element = (pointiplusone - pointi, -pointjplusone + pointj)
                if np.linalg.det(element) != 0:
                    a[k, :, :] = element
                    b[k, :, :] = (pointj - pointi).reshape(2, 1)
                    further_information[k, :] = (i, j)
                    k = k + 1

# print('matrix a = {}'.format(a))
# print(a.shape)

# print('matrix b = {}'.format(b))
# print(b)
solution = np.linalg.solve(a[:k], b[:k])
print('Solution 3d = {}'.format(solution))
intersection(solution, further_information)
# print(a1)
# print(b1)
