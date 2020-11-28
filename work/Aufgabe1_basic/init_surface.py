"""
Implements a function "init_surface" to initialize the Surface
"""

import numpy as np
import math


def init_surface(xVals):
    """
    initializes the starting values of the Surface 

    funct ion: y = 0 if |x| < 25 else -50*(1+cos((2*Pi*x)/50))

    :param xVals: x-values of the surface

    :returns: y-Values of the initialized surface
    """

    return np.array([0 if (x < -24 or x > 24)
                     else ((-50) * (1 + math.cos((2*math.pi*x)/50)))
                     for x in xVals])
