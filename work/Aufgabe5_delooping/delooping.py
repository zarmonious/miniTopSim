"""
Script to test basic delooping to be implemented in the project.
This should be a standalone file
"""

import numpy as np
import matplotlib.pyplot as plt

def pointstosection(p):

    return None


def deloop(p):
    """Nimm zuerst die ersten beiden Punkte und dieser Streckenabschnitt wird mit den anderen auf einen Schnittpunkt
    verglichen"""


    for i, workingpoint in enumerate(p):
        if i < 9:
            workingpointplusone = p[i + 1, :]
            for j, movingpoint in enumerate(p):
                if i == j:
                    continue
                if j < 9:
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
x0 x1 x2 x3 x4 x5 x6 x7 x8 x9
y0 y1 y2 y3 y4 y5 y6 y7 y8 y9
"""

x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0, 7.0, 8.0, 9.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0, 7.0, 8.0, 9.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 10)))
print(p)
print(np.transpose(p[:, 1] - p[:, 0]))
print((p[0, 1]))
print(p[:,0])
testmatrix = np.array([p[1, :] - p[0, :], -p[2, :] + p[1, :]])
print(type(testmatrix))
print(testmatrix.shape)
print(np.transpose(testmatrix))
print('Starting deloop')
deloop(p)
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