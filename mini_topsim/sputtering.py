import os

import parameters as par

import numpy as np
from scipy.interpolate import interp1d


def init_sputtering():
    """
    initializes the get_sputter_yield module variable

    depending on the set parameters this function either attaches a callable
    object that implements the yamamura function to the get_sputter_yield
    variable, or one that reads the sputter yields from a given table.
    """
    global get_sputter_yield
    if par.SPUTTER_YIELD_FILE == '':
        get_sputter_yield = Sputter_yield_Yamamura(par.SPUTTER_YIELD_0,
            par.SPUTTER_YIELD_F, par.SPUTTER_YIELD_B)
    else:
        get_sputter_yield = Sputter_yield_table(par.SPUTTER_YIELD_FILE)

class Sputter_yield_Yamamura():
    """
    Describes a callable object that implements the yamamura function.
    """
    def __init__(self, y0,f, b):
        self.y0 = y0
        self.f = f
        self.b = b
    
    def __call__(self, costheta):
        """
        calculates the sputter yield according to the yamamura function.

        :param costheta: the cosine of the angle between the surface normal 
        and the sputter beam direction.
    
        :returns: Sputter yield Y
        """
        y=self.y0*costheta**(-self.f) * np.exp(self.b*(1-1/costheta))

        #removes division by 0 errors. If costheta = 0 -> Y should be 0
        y[np.isnan(y)]=0 
        return y

class Sputter_yield_table():
    """
    Describes a callable object that interpolates sputter yields from a given file.
    """
    def __init__(self, filename):
        self.filename = filename

    def __call__(self, costheta):
        """
        interpolates sputter yields from given data in a file

        :param costheta: the cosine of the angle between the surface normal 
        and the sputter beam direction.

        :returns: Sputter yield Y
        """
        filepath = os.path.dirname(__file__) + "\\tables\\" + self.filename
        data = np.genfromtxt(filepath, skip_header = 1)
        tiltvals = data[:,0]
        yieldvals = data[:,1]
        theta = np.arccos(costheta)
        yfunc = interp1d(tiltvals, yieldvals)
        return yfunc(theta)
