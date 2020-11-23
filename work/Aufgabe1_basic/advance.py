import numpy as np
from surface import Surface

def advance(surface: Surface, dtime):
    v = 1
    nX, nY = surface.normal_vector()

    surface.xVals += v*nX*dtime
    surface.yVals += v*nY*dtime

def timestep(dtime, time, end_time):
    return dtime if (time + dtime) <= end_time else (end_time - time)
