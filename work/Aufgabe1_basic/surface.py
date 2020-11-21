import numpy as np
import init_surface
import matplotlib.pyplot as plt



class Surface:

    def __init__(self):
       
        self.xVals = np.arange(-50,51,1)
        self.yVals = init_surface.init_surface(self.xVals)
    
    def normal_vector(self):
        return 0
    def plot(self):
        plt.plot(self.xVals,self.yVals)
        plt.title('Surface')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()
    def write(self):
        return 0
    

s = Surface()
s.plot()