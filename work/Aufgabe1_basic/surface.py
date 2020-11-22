import numpy as np
import init_surface
import matplotlib.pyplot as plt



class Surface:

    def __init__(self):
        self.dx = 1
        self.xVals = np.arange(-50,51,self.dx)
        self.yVals = init_surface.init_surface(self.xVals)      

    def normal_vector(self):
        #x = np.zeros_like(self.xVals)
        x = np.full_like(self.xVals, 2*self.dx)
        y = np.zeros_like(self.yVals)

        #x[0] = self.xVals[1] - self.xVals[0]
        x[0] = self.dx
        y[0] = self.yVals[1] - self.yVals[0]
        
        #x[-1] = self.xVals[-1] - self.xVals[-2]
        x[-1] = self.dx
        y[-1] = self.yVals[-1] - self.yVals[-2]
        
        
        y[1:-1] = np.array(self.yVals[2::] -self.yVals[:-2:])
        #x[1:-1] = np.array(self.xVals[2::] - self.xVals[:-2:])
    
        magnitude = np.linalg.norm([x, y], axis=0)
        
        return np.array((y / magnitude, -x / magnitude))


    def plot(self):

        plt.plot(self.xVals,self.yVals)
        plt.title('Surface')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def write(self):
        return 0
    

s = Surface()
x, y = s.normal_vector()
s.plot()