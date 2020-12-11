"""
Usage: $ python3 main.py <simulation time> <timestep>

includes to functions:
"mini_topsim": reads the Simulation parameters and starts the Simulation
"simulation": simulates the surface movement with the given parameters 
"""

import sys
import os

import matplotlib.pyplot as plt


from surface import Surface
from advance import advance
from advance import timestep
import mini_topsim.sputtering as sputter
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

   
    if not config_filename.endswith('.cfg'):
        print('Error: Incorrect config.')
        sys.exit()

    filename = os.path.splitext(config_filename)[0] + '.srf'

    if os.path.exists(filename):
        os.remove(filename)



    par.load_parameters(config_filename)

    tend = par.TOTAL_TIME
    dt = par.TIME_STEP

    surface = Surface()
    sputter.init_sputtering()
    time = 0

    while time < tend:
        surface.write(time, filename)
        dtime = timestep(dt, time, tend)
        advance(surface, dtime)
        surface.eliminate_overhangs()
        time += dtime

    surface.write(time, filename)

    if par.PLOT_SURFACE:
        plot.plot(filename)

if __name__ == '__main__':
    mini_topsim()
