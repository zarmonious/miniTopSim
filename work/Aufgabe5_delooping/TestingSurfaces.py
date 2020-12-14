import numpy as np
import matplotlib.pyplot as plt


x = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))


x1 = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 3.0, 4.0, 5.0, 3.0, 2.0, 5.0, 5.7, 6.0, 7.0))
y1 = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 5.5, 4.0, 5.0, 4.7, 4.0, 3.5, 4.9, 5.0, 5.5))

p1 = np.transpose(np.concatenate((x1, y1)).reshape((2, 15)))

p2 = np.random.rand(100, 2)

x3 = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 3.0, 4.0, 5.0, 3.0, 2.0, 5.0, 5.7,
               6.0, 7.0, 8.0, 7.0, 7.3, 8.0, 9.0, 10.0, 11.0, 9.0, 8.0, 11.0, 12.0, 13.0, 14.0, 14.0, 14.0))
y3 = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 5.5, 4.0, 5.0, 4.7, 4.0, 3.5, 4.9,
               5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 5.5, 4.0, 5.0, 4.7, 4.0, 3.5, 5, 5, 5, 6, 7))

p3 = np.transpose(np.concatenate((x3, y3)).reshape((2, x3.size)))


if __name__ == '__main__':

    plt.plot(p3[:, 0], p3[:, 1], 'b+-', label='Surfacepoints')
    plt.show()