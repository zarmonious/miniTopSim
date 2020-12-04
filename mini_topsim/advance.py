"""
Implements the functions to calculate the surface movement

function advance: calculates the movement of the surface
function timestep: calculates the timestep for a given time  

"""


import numpy as np
import mini_topsim.surface 

import parameters as par

def advance(surface, dtime):
    """
    calculates the movement of the surface for a timestep dtime

    :param surface: surface that is being calculated
    :param dtime: timstep of the calculation
    """
    v = par.ETCH_RATE
    nx, ny = surface.normal_vector()

    surface.xvals += nx*dtime*v
    surface.yvals += ny*dtime*v


def timestep(dtime, time, end_time):
    """
    calculates the timestep for a given time

    returns the timestep if the calculation isnt overstepping the endtime
    if it would overstep it returns the resttime to calculte to the endtime

    :param dtime: timestep
    :param time: current time in simulation
    :param end_time: endtime of the simulation

    :returns: correct timestep to reach the calculation endtime
    """
    return dtime if (time + dtime) <= end_time else (end_time - time)