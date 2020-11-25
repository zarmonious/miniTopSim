"""
Script to test basic delooping to be implemented in the project.
This should be a standalone file
"""

import numpy as np
import matplotlib.pyplot as plt

def deloop2(p):
    pplusone = np.roll(p, -1, axis=0)
    pmove = p
    pmoveplusone = np.roll(pmove, -1, axis=0)
    print('p = {}'.format(p))
    print(np.shape(p))
    #print('pplusone = {}'.format(pplusone))
    #print(np.shape(pplusone))
    print('pmove = {}'.format(pmove))
    print(np.shape(pmove))
    #print('pmoveplusone = {}'.format(pmoveplusone))
    #print(np.shape(pmoveplusone))
    a_1 = pplusone - p
    a_1 = np.reshape(a_1, 14, 'C')
    a_2 = -pmoveplusone + pmove
    a_2 = np.reshape(a_2, 14, 'C')
    a = np.transpose(np.array([a_1, a_2]))

    b = (np.array(pmove - p))
    print('a = {}'.format(a))
    print(np.shape(a))
    print('a_1 = {}'.format(a_1))
    print(np.reshape(a_1, 14, 'C'))
    print(np.reshape(a_1, 14, 'F'))
    print(np.reshape(a_1, 14, 'A'))
    print(np.shape(a_1))
    print('a_2 = {}'.format(a_2))
    print(np.shape(a_2))
    print('a = {}'.format(a))
    print(np.shape(a))
    print('b = {}'.format(b))
    print(np.shape(b))
    erg = np.linalg.solve(a, b)
    print(erg)
    return None


def deloop(p):
    """Nimm zuerst die ersten beiden Punkte und dieser Streckenabschnitt wird mit den anderen auf einen Schnittpunkt
    verglichen"""


    for i, workingpoint in enumerate(p):
        if i < 7:
            workingpointplusone = p[i + 1, :]
            for j, movingpoint in enumerate(p):
                if i == j:
                    continue
                if j < 7:
                    movingpointplusone = p[j + 1]
                    #print('i:{} und j:{}',format((i, j)))
                    #print(workingpoint)
                    #print(workingpointplusone)
                    #print(movingpoint)
                    #print(movingpointplusone)
                    #print(np.array([workingpointplusone - workingpoint, -movingpointplusone + movingpoint]))
                    #print(np.transpose(np.array([workingpointplusone - workingpoint, -movingpointplusone + movingpoint])))
                    #print(np.array(movingpoint-workingpoint))
                    a = np.transpose(np.array([workingpointplusone - workingpoint, -movingpointplusone + movingpoint]))
                    b = (np.array(movingpoint - workingpoint))
                    #print('a = {}'.format(a))
                    #print('b = {}'.format(b))
                    erg = np.linalg.solve(a, np.transpose(b))
                    if 0 < erg[0] < 1 and 0 < erg[1] < 1:
                        print('Kreuzung')
                        print('Ergebnis = {}'.format(erg))

                    #print(erg[0])
                    #print(erg[1])
                    #print('Ergebnis = {}'.format(erg))
                    #ergebnis = np.linalg.solve(np.transpose(np.array(workingpointplusone - workingpoint), np.array(-movingpointplusone + movingpoint)), np.array(movingpoint - workingpoint))
                    # print(ergebnis)
                    # if ergebnis[0] <= 1:
                    #    print(ergebnis)



        #np.linalg.solve(np.transpose(np.array(workingpointplusone - workingpoint, - )))
        #np.linalg.solve(np.transpose(np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]])), (np.array(p[1, :] - p[0, :])))
        print('xxxxxxxxxxxxxx')


""" In zweidimensionalen Numpy Arrays werden die Punkte gespeichert
x0 y0
x1 y1
x2 y2
x3 y3
"""

x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))

print('Starting deloop')
deloop2(p)
#deloop(p)
print('Stopping deloop')
print('..............')
print(np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]]))
print('Eval Line')
print(np.transpose(np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]])))
ergebnis = np.linalg.solve(np.transpose(np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]])), (np.array(p[1, :] - p[0, :])))
ergebnis2 = np.linalg.solve(np.transpose(np.array([p[2, :] - p[1, :], -p[4, :] + p[3, :]])), (np.array(p[3, :] - p[1, :])))

print('Matrix A:')
print(np.transpose(np.array([p[1, :] - p[0, :], -p[2, :] - p[1, :]])))
print('Matrix b:')
print((np.array(p[:, 1] - p[:, 0])))
print('---------')

print(ergebnis)
print(ergebnis2)
print('---------')






plt.plot(x, y, 'b+-', label='Surfacepoints')
plt.show()