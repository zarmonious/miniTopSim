"""
Usage: $ python3 main.py <simulation time> <timestep>

includes to functions:
"mini_topsim": reads the Simulation parameters and starts the Simulation
"simulation": simulates the surface movement with the given parameters
"""

import sys
import os
import numpy as np
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)
from time import time as currenttime
import matplotlib.pyplot as plt
from mini_topsim.main import mini_topsim
from mini_topsim.surface import Surface
from advance import advance
from advance import timestep
import parameters as par

import plot

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
n_max = 100
simulation_time_array = np.empty((2, 0))

for i in range(n_max):
    if par.DELTA_X > 0.8:
        #print(par.DELTA_X)
        surface = Surface()
        time = 0
        start_simulation_time = currenttime()

        while time < tend:
            surface.write(time, filename)
            dtime = timestep(dt, time, tend)
            advance(surface, dtime)
            # print('Start delooping')
            surface.deloop()
            # print('Stop delooping')
            time += dtime

        stop_simulation_time = currenttime()
        simulation_time = stop_simulation_time - start_simulation_time
        #file = open('timing.txt','w')
        #file
        simulation_time_array = np.append(simulation_time_array, np.array((int(100/par.DELTA_X), simulation_time)).reshape(2, 1), axis=1)
        with open("timing.txt", 'a') as file:
            file.write(str(int(100/par.DELTA_X))+', '+str(simulation_time)+'\n')
        print('The Simulation took: {}s'.format(float(simulation_time)))
        #print(par.DELTA_X)
        surface.write(time, filename)
        par.DELTA_X = par.DELTA_X - 0.5
        #print(par.DELTA_X)
print(simulation_time_array)
print(simulation_time_array.shape)

plt.plot(simulation_time_array[0, :],simulation_time_array[1, :], 'b+-')
plt.show()
#if par.PLOT_SURFACE:
    #plot.plot(filename)

#if __name__ == '__main__':


#mini_topsim()



