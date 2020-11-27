"""
Implements a function "init_surface" to initialize the Surface
"""

import numpy as np
import math


def init_surface(xvals):
    """
    initializes the starting values of the Surface 

    function: y = 0 if |x| < 25 else -50*(1+cos((2*Pi*x)/50))

    :param xVals: x-values of the surface

    :returns: y-Values of the initialized surface
    """
    mask = ((xvals >= -25) & (xvals <= 25))
    yvals = np.zeros_like(xvals)

    yvals[mask] = ((-50) * (1 + np.cos((2*np.pi*xvals[mask])/50)))

    return yvals