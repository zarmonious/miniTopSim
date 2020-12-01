import numpy as np
import matplotlib.pyplot as plt


x = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 6.0))
y = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 6.0))

p = np.transpose(np.concatenate((x, y)).reshape((2, 7)))


x1 = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 3.0, 4.0, 5.0, 3.0, 2.0))
y1 = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 5.5, 4.0, 5.0, 4.7, 4.0))

p1 = np.transpose(np.concatenate((x1, y1)).reshape((2, 11)))

p2 = np.random.rand(100, 2)



if __name__ == '__main__':

    plt.plot(p[:, 0], p[:, 1], 'b+-', label='Surfacepoints')
    plt.show()