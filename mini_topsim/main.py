"""
Usage: $ python3 main.py <simulation time> <timestep>

includes to functions:
"mini_topsim": reads the Simulation parameters and starts the Simulation 
"""

import sys
import os
from time import time as currenttime

import matplotlib.pyplot as plt

from surface import Surface
from advance import advance
from advance import timestep
import mini_topsim.sputtering as sputter
import parameters as par


import plot

def mini_topsim(config_file = None):
    """
    Loads parameters from config_file, starts the sim, plots and writes to file

    :param config_file: config_file with simulation parameters


    Loads parameters from config_file.   
    If no config_file is passed passed, None is returned.
    Creates a Surface Object and starts the simulation. 
    The correct timestep is calculated with the timestep function 
    from the advance module. 
    
    If a *.srf_save file with the same filename exists, the plot function with
    both surfaces is called.

    """
    print('Running miniTopSim ...')

    if config_file is None:
        if len(sys.argv) > 1:
            config_filename = sys.argv[1]
        else:
            config_filename = 'config1.cfg'

        config_file = config_filename

    if not config_file.endswith('.cfg'):
        print('Error: Incorrect config.')
        sys.exit()
        
    filename = os.path.splitext(config_file)[0] + '.srf'

    if os.path.exists(filename):
        os.remove(filename)
        
    par.load_parameters(config_file)

    tend = par.TOTAL_TIME
    dt = par.TIME_STEP

    surface = Surface()
    sputter.init_sputtering()
    time = 0
    start_simulation_time = currenttime()

    while time < tend:
        surface.write(time, filename)
        dtime = timestep(dt, time, tend)
        advance(surface, dtime)
        surface.eliminate_overhangs()
        time += dtime

    surface.write(time, filename) 
    
    filename_save = filename + '_save'
    
    if os.path.exists(filename_save):
        print('*.srf_save file exists... plotting both!')
        plot.plot(filename, filename_save)
    elif par.PLOT_SURFACE:
        plot.plot(filename)
        

if __name__ == '__main__':

    
    mini_topsim()

