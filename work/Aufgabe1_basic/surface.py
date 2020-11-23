import numpy as np
import init_surface
import matplotlib.pyplot as plt


class Surface:

    def __init__(self):
        self.xVals = np.arange(-50., 51., 1.)
        self.yVals = init_surface.init_surface(self.xVals)

    def normal_vector(self):
        x = np.zeros_like(self.xVals)
        y = np.zeros_like(self.yVals)

        x[0] = self.xVals[1] - self.xVals[0]
        y[0] = self.yVals[1] - self.yVals[0]

        x[-1] = self.xVals[-1] - self.xVals[-2]
        y[-1] = self.yVals[-1] - self.yVals[-2]

        y[1:-1] = np.array(self.yVals[2::] - self.yVals[:-2:])
        x[1:-1] = np.array(self.xVals[2::] - self.xVals[:-2:])

        magnitude = np.linalg.norm([x, y], axis=0)

        return (y / magnitude), (-x / magnitude)

    def plot(self, time):

        plt.plot(self.xVals, self.yVals, "x-", label=f"t = {time}")
        plt.title('Surface')
        plt.xlabel('x[nm]')
        plt.ylabel('y[nm]')

    def write(self, time, filename):
        with open(filename, 'a') as f:
            f.write(f"surface: {time} {len(self.xVals)} x-positions y-positions\n")
            for x, y in zip(self.xVals, self.yVals):
                f.write(f"{x} {y}\n")
