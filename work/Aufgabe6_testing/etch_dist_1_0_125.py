import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import mini_topsim.plot as srfplt
from mini_topsim.surface import Surface
from mini_topsim.main import par

srf_filename1 = os.path.join(filedir,'etch_dx0_125.srf')
srf_filename2 = os.path.join(filedir,'etch_dx1.srf')

srfplotter = srfplt._SurfacePlotter(srf_filename1, srf_filename2)

par.load_parameters(os.path.join(filedir,'etch_dx0_125.cfg'))
srf1 = Surface()
srf1.xvals = srfplotter.xpoints_list[-1]
srf1.yvals = srfplotter.ypoints_list[-1]

par.load_parameters(os.path.join(filedir,'etch_dx1.cfg'))
srf2 = Surface()
srf2.xvals = srfplotter.refsrf.xpoints_list[-1]
srf2.yvals = srfplotter.refsrf.ypoints_list[-1]

print('Surface distance dx0_125 to dx1 = %.5f' % srf1.distance(srf2))
print('Surface distance dx1 to dx0_125 = %.5f' % srf2.distance(srf1))
