import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)


from surface import Surface
import parameters as par

import matplotlib.pyplot as plt


config_filename="test_overhangs.cfg"
config_file = os.path.join(os.path.dirname(__file__), config_filename)

if not config_file.endswith('.cfg'):
    print('Error: Incorrect config.')
    sys.exit()

filename = os.path.splitext(config_file)[0] + '.srf'

if os.path.exists(filename):
    os.remove(filename)

par.load_parameters(config_file)


surface = Surface()
surface.xvals=[0.,1.,2.,1.,1.5,3.,4.,5.,4.,5.,6.,7.,8.,7.,7.5,8.,9.]
surface.yvals=[10.,10.,10.,15.,17.,18.,18.,18.,12.,13.,13.,12.,11.,10.,9.,8.,8.]

plt.title('Eliminate Overhangs Test')
plt.ylabel('Surface Y values')
plt.xlabel('Surface X values')
plt.plot(surface.xvals, surface.yvals, 'b-', label='With Overhangs')

surface.eliminate_overhangs()

plt.plot(surface.xvals, surface.yvals, 'r-', label='Without Overhangs')
plt.legend()
plt.show()
