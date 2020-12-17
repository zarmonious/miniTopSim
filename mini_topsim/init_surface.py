"""
Implements a function "init_surface" to initialize the Surface
"""

import numpy as np
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
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
        y-Values of the initialized surface.
    """
    
    if par.INITIAL_SURFACE_TYPE == 'Flat':
        yvals=_flat(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'DoubleCosine':
        yvals=_double_cosine(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'Step':
        yvals=_step(xvals)
        
    elif par.INITIAL_SURFACE_TYPE == 'V-Shape':
        yvals=_vshape(xvals)
        
        
    else:
        yvals=_cosine(xvals)
        
        
    return yvals

def _flat(xvals):
    """
    Function for flat surface y=0, with boundary conditions

    Parameters
    ----------
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
        y-Values of the initialized surface.

    """
    yvals = np.zeros_like(xvals)
    return yvals


def _cosine(xvals):
    """
    Function for cosine surface with boundary conditions

    Parameters
    ----------
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
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
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
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
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
        y-Values of the initialized surface.

    """
    mask = ((xvals >= par.FUN_XMIN) & (xvals <= par.FUN_XMAX))
    mask_min = (xvals<par.FUN_XMIN)
    
    yvals = np.zeros_like(xvals)
    yvals[mask_min] = par.FUN_PEAK_TO_PEAK
    

    k,d = _find_linar_poly(par.FUN_XMIN, par.FUN_PEAK_TO_PEAK, par.FUN_XMAX, 0)


    yvals[mask] = k*xvals[mask] + d

    return yvals

def _vshape(xvals):
    '''
    Function for v-shape surface with boundary conditions

    Parameters
    ----------
    xvals : np.array
        x-values of the surface.

    Returns
    -------
    yvals : np.array
        y-Values of the initialized surface.

    '''

    center = par.FUN_XMIN + (par.FUN_XMAX-par.FUN_XMIN)/2

    mask_left = ((xvals >= par.FUN_XMIN) & (xvals <= center))
    mask_right = ((xvals >= center) & (xvals <= par.FUN_XMAX))

    yvals = np.zeros_like(xvals)
    

    k1,d1 = _find_linar_poly(par.FUN_XMIN, 0, center, par.FUN_PEAK_TO_PEAK)
    k2,d2 = _find_linar_poly(center, par.FUN_PEAK_TO_PEAK, par.FUN_XMAX, 0)


    yvals[mask_left] = k1*xvals[mask_left] + d1
    yvals[mask_right] = k2*xvals[mask_right] + d2
    
    return yvals



#def _file()

def _find_linar_poly(p1_x, p1_y, p2_x, p2_y):
    """
    Finding the linear polynomial y=kx+d from two points

    Parameters
    ----------
    p1_x : float
        X value of first point.
    p1_y : float
        Y value of first point.
    p2_x : float
        X value of second point.
    p2_y : float
        Y value of second point.

    Returns
    -------
    k : float
        Slope of the linear polynomial.
    d : float
        Intersection with y-axis.

    """
    k = (p2_y-p1_y)/(p2_x - p1_x)
    d = p1_y - k * p1_x
    return k,d

def read_srf_file(filename,time):
    '''
    Reads x/y Values from srf-file at given time_stamp

    Parameters
    ----------
    filename : str
        Absolut path of given srf-file.
    time : float
        The time stamp where data will be taken.
        
    Returns
    -------
    xvalues : np.array
        x-Values of the initialized surface.
    yvalues : np.array
        y-Values of the initialized surface.

    '''
    xvalues_list = list()
    yvalues_list = list()

    n_values = 0

    print(filename)
    
    with open(filename) as file:

        for line_index, line in enumerate(file):
            if 'surface:' +' '+ str(time) in line:
                string_array = line.split(' ')

                n_values=(int(string_array[2]))
                
                for n, line in enumerate(file):
                    if n<n_values:
                        value_array = line.split(' ')
                        xvalues_list.append(float(value_array[0]))
                        yvalues_list.append(float(value_array[1]))
                        
    xvalues = np.array(xvalues_list)
    yvalues = np.array(yvalues_list)
               
                  
    return xvalues, yvalues

