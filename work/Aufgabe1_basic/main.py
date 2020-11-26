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


def mini_topsim():
    """
    Reads the Simulation parameter from the system arguments ands starts the simulation

    the first sys.argv[1] is the simulation time 
    the second sys.argv[2] is the timestep
    if no sys arguments are passed the simulation starts with tend = 10 and dt = 1
    """

    if len(sys.argv) > 1:
        tend = float(sys.argv[1])
        dt = float(sys.argv[2])
    else:
        tend = 10
        dt = 1
    simulation(tend, dt)


def simulation(tend, dt):
    """
    starts the simulation, plots and writes the data

    creates a Surface Object and starts the simulation. 
    the correct timestep is calculated with the timestep function 
    from the advance module. 
    Writes all calculated datapoints to a file with the 
    filenname: basic_<tend>_<dt>.srf
    plots the simulation fpr t = 0 and t = tend

    :param tend: endtime of the simulation
    :param dt: timestep of the simulation
    """
    s = Surface()
    time = 0
    filename = f"basic_{tend}_{dt}.srf"
    s.plot(time)

    while time < tend:
        s.write(time, filename)
        advance(s, timestep(dt, time, tend))
        time += timestep(dt, time, tend)

    s.write(time, filename)
    s.plot(time)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    mini_topsim()
