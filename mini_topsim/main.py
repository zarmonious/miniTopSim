"""
Usage: $ python3 main.py <simulation time> <timestep>

includes to functions:
"mini_topsim": reads the Simulation parameters and starts the Simulation
"simulation": simulates the surface movement with the given parameters 
"""

import sys
import os
from time import time as currenttime

import matplotlib.pyplot as plt

from surface import Surface
from advance import advance
from advance import timestep
import parameters as par

import plot

def mini_topsim():
    """
    Reads the Simulation parameters, starts the sim, plots and writes to file

    the first sys.argv[1] is the config file name.

    if no sys argument is passed the programm will stop.
    Writes all calculated datapoints to a file with the 
    filenname: <config_file_name>.srf

    """
    print('Running miniTopSim ...')

    if len(sys.argv) > 1:
        config_filename = sys.argv[1]
    else:
        print("Error: No config passed.")
        sys.exit()

    config_file = os.path.join(os.path.dirname(__file__), config_filename)


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
    time = 0
    start_simulation_time = currenttime()

    while time < tend:
        surface.write(time, filename)
        dtime = timestep(dt, time, tend)
        advance(surface, dtime)
        time += dtime

    stop_simulation_time = currenttime()
    simulation_time = stop_simulation_time - start_simulation_time
    print('The Simulation took: {}s'.format(float(simulation_time)))
    surface.write(time, filename)

    if par.PLOT_SURFACE:
        plot.plot(filename)

if __name__ == '__main__':


    mini_topsim()



