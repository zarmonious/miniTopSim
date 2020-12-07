"""
Implements a function "init_surface" to initialize the Surface
"""

import numpy as np
import math

import parameters as par


def init_surface(xvals):
    """
    initializes the starting values of the Surface 

    INITIAL_SURFACE_TYPE can be: 
        "Flat","Cosine","DoubleCosine","Step","V-Shape","File"
    
    In case of "File":
        A srf-File from INTITIAL_SURFACE_FILE will be read and used as input.
    
    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.
    """
    
    if par.INITIAL_SURFACE_TYPE == 'Flat':
        yvals=_flat(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'DoubleCosine':
        yvals=_double_cosine(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'Step':
        yvals=_step(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'V-Shape':
        print('Noch nicht implementiert!!')
        
    elif par.INITIAL_SURFACE_TYPE == 'File':
        print('Noch nicht implementiert!!')
        
    else:
        yvals=_cosine(xvals)
        
        
    return yvals

def _flat(xvals):
    """
    Function for flat surface y=0, with boundary conditions

    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.

    """
    yvals = np.zeros_like(xvals)
    return yvals


def _cosine(xvals):
    """
    Function for cosine surface with boundary conditions

    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.

    """
    mask = ((xvals >= par.FUN_XMIN) & (xvals <= par.FUN_XMAX))
    yvals = np.zeros_like(xvals)
    
    yvals[mask] = ((par.FUN_PEAK_TO_PEAK / 2) * (1 +
        np.cos((2*np.pi*xvals[mask])/50))) 
    
    return yvals

def _double_cosine(xvals):
    """
    Function for double cosine surface with boundary conditions

    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.

    """
    mask = ((xvals >= par.FUN_XMIN) & (xvals <= par.FUN_XMAX))
    yvals = np.zeros_like(xvals)
    
    yvals[mask] = ((par.FUN_PEAK_TO_PEAK / 2) * (1 +
        np.cos(((4*np.pi*xvals[mask])+50*np.pi)/50))) 
    
    return yvals

def _step(xvals):
    """
    Function for step surface with boundary conditions
    
    Step function with or without angle of inclination (depending on:
    FUN_XMIN=FUN_XMAX or FUN_XMIN<FUN_XMAX).                                                   

    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.

    """
    mask = ((xvals >= par.FUN_XMIN) & (xvals <= par.FUN_XMAX))
    mask_min= (xvals<par.FUN_XMIN)
    
    yvals = np.zeros_like(xvals)
    yvals[mask_min]=par.FUN_PEAK_TO_PEAK
    

    k,d=find_linar_poly(par.FUN_XMIN, par.FUN_PEAK_TO_PEAK, par.FUN_XMAX, 0)


    yvals[mask] = k*xvals[mask]+d

    return yvals

def _vshape(xvals):
    """
    Function for v-shape surface with boundary conditions

    Parameters
    ----------
    xvals : list
        x-values of the surface.

    Returns
    -------
    yvals : list
        y-Values of the initialized surface.

    """
    mask = ((xvals >= par.FUN_XMIN) & (xvals <= par.FUN_XMAX))
    yvals = np.zeros_like(xvals)
    
    yvals[mask] = ((par.FUN_PEAK_TO_PEAK / 2) * (1 +
        np.cos((2*np.pi*xvals[mask])/50))) 
    
    return yvals

#def _file()

def find_linar_poly(p1_x, p1_y, p2_x, p2_y):
    
    k = (p2_y-p1_y)/(p2_x - p1_x)
    d = p1_y - k * p1_x
    return k,d