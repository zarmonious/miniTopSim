"""
Implements the functions to calculate the surface movement

function advance: calculates the movement of the surface
function timestep: calculates the timestep for a given time  

"""


import numpy as np
import mini_topsim.surface 
import mini_topsim.sputtering as sputter
import scipy.constants as sciconst

import parameters as par

def advance(surface, dtime):
    """
    calculates the movement of the surface for a timestep dtime

    :param surface: surface that is being calculated
    :param dtime: timstep of the calculation
    """
    
    nx, ny = surface.normal_vector()
    v = get_velocities(ny)

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

def get_velocities(ny):
    """
    returns the surface velocities for each point

    depending on the ETCHING parameter this function either returns the value
    of the ETCH_RATE parameter for etching, or calculates the surface
    velocity depending on the sputter flux density.

    :param ny: y-component of the surface normal

    :returns: surface velocity for each surface point
    """
    if par.ETCHING is True:
        v = par.ETCH_RATE
    else:
        costheta = abs(ny)
        y = sputter.get_sputter_yield(costheta)
        v=(par.BEAM_CURRENT_DENSITY/sciconst.e * y * costheta) / par.DENSITY
        v=v*1e7 #converting cm/s --> nm/s
        
    return v