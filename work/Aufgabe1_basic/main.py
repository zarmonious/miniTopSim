from surface import Surface
from advance import advance
from advance import timestep
import matplotlib.pyplot as plt
import sys


def mini_topsim():
    if len(sys.argv) > 1:
        tend = float(sys.argv[1])
        dt = float(sys.argv[2])
    else:
        tend = 10
        dt = 1
    simulation(tend, dt)


def simulation(tend, dt):
    s = Surface()
    time = 0
    filename = f"basic_{tend}_{dt}.srf"
    s.plot(time)
    while time < tend:
        s.write(time, filename)
        advance(s, timestep(dt, time, tend))
        time += timestep(dt, time, tend)
    s.plot(time)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    mini_topsim()
