"""
Usage: $ python3 main.py <simulation time> <timestep>

includes to functions:
"mini_topsim": reads the Simulation parameters and starts the Simulation
"simulation": simulates the surface movement with the given parameters 
"""

import sys
import matplotlib.pyplot as plt


from surface import Surface
from advance import advance
from advance import timestep
import parameters as par

def mini_topsim():
    """
    Reads the Simulation parameters, starts the sim, plots and writes to file

    the first sys.argv[1] is the simulation time 
    the second sys.argv[2] is the timestep

    if no sys arguments are passed the simulation starts with tend=10 and dt=1
    creates a Surface Object and starts the simulation. 
    the correct timestep is calculated with the timestep function 
    from the advance module. 
    Writes all calculated datapoints to a file with the 
    filenname: basic_<tend>_<dt>.srf
    plots the simulation fpr t = 0 and t = tend

    """
    print('Running miniTopSim ...')

    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = './config1.cfg'

    if not config_file.endswith('.cfg'):
        print('Error: Incorrect config.')
        sys.exit()

    filename = config_file[:-4] + '.srf'

    par.load_parameters(config_file)

    tend = par.TOTAL_TIME
    dt = par.TIME_STEP

    surface = Surface()
    time = 0
    surface.plot(time)

    while time < tend:
        surface.write(time, filename)
        dtime = timestep(dt, time, tend)
        advance(surface, dtime)
        time += dtime

    surface.write(time, filename)
    surface.plot(time)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    mini_topsim()
