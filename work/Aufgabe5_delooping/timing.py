"""
Running the main simulation with the added timing tests
"""
import sys
import os
import numpy as np

filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)
from time import time as currenttime
import matplotlib.pyplot as plt
from mini_topsim.surface import Surface
from advance import advance
from advance import timestep
import parameters as par
import plot


def mini_topsim_timing():
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
    par.DELTA_X = 10
    simulation_time_array = np.empty((2, 0))

    while par.DELTA_X > 0.2:
        # print(par.DELTA_X)
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
        simulation_time_array = np.append(simulation_time_array, np.array(
            (int(100 / par.DELTA_X), simulation_time)).reshape(2, 1), axis=1)
        # print('The Simulation took: {}s'.format(float(simulation_time)))
        # print(np.array((int(100/par.DELTA_X))))
        # print(par.DELTA_X)
        surface.write(time, filename)
        par.DELTA_X = par.DELTA_X - 0.6
        # print(par.DELTA_X)

    plt.title('Simulationtime in dependence of the number of points')
    plt.plot(simulation_time_array[0], simulation_time_array[1], 'b+-')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Number of points')
    plt.ylabel('Time in Seconds')
    plt.grid(which='both')
    plt.show()
    if par.PLOT_SURFACE:
        plot.plot(filename)
