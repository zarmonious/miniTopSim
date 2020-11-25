"""
Script to test basic delooping to be implemented in the project.
This should be a standalone file
"""

import numpy as np
import matplotlib.pyplot as plt


def deloop(p):
    """Nimm zuerst die ersten beiden Punkte und dieser Streckenabschnitt wird mit den anderen auf einen Schnittpunkt
    verglichen"""

    #Baue den ersten Steckenabschnitt

    #s0 = p[:, 0] + (p[:, 1] - p[:, 0]) * t
    #numpy.linalg.solve(a,b)

    np.linalg.solve(np.array([p[:, 1] - p[:, 0], p[:, 2] - p[:, 1]]), np.array(p[:, 1] - p[:, 0]))

""" In zweidimensionalen Numpy Arrays werden die Punkte gespeichert
x0 x1 x2 x3 x4 x5 x6 x7 x8 x9
y0 y1 y2 y3 y4 y5 y6 y7 y8 y9
"""

x = np.array((0.0, 1.0, 2.0, 1.0, 2.3, 5.0, 6.0, 7.0, 8.0, 9.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 6.5, 5.0, 6.0, 7.0, 8.0, 9.0))

p = np.concatenate((x, y)).reshape((2, 10))

ergebnis = np.linalg.solve(np.transpose(np.array([p[:, 1] - p[:, 0], -p[:, 2] + p[:, 1]])), (np.array(p[:, 1] - p[:, 0])))
ergebnis2 = np.linalg.solve(np.transpose(np.array([p[:, 2] - p[:, 1], -p[:, 4] + p[:, 3]])), (np.array(p[:, 3] - p[:, 1])))

print('Matrix A:')
print(np.transpose(np.array([p[:, 1] - p[:, 0], -p[:, 2] - p[:, 1]])))
print('Matrix b:')
print((np.array(p[:, 1] - p[:, 0])))
print('---------')

print(ergebnis)
print(ergebnis2)
print('---------')




print(p)
print(np.transpose(p[:, 1] - p[:, 0]))
print((p[0, 1]))
print(p[:,0])
testmatrix = np.array([p[:, 1] - p[:, 0], -p[:, 2] + p[:, 1]])
print(type(testmatrix))
print(testmatrix.shape)
print(np.transpose(testmatrix))

plt.plot(x, y, 'b+-', label='Surfacepoints')
plt.show()