import os
filedir = os.path.dirname(__file__)

import mini_topsim.plot as srfplt

srf_filename1 = os.path.join(filedir,'etch_dx0_125.srf')
srf_filename2 = os.path.join(filedir,'etch_dx1.srf')

srfplt.plot(srf_filename1, srf_filename2)
srfplotter = srfplt._SurfacePlotter(srf_filename1, srf_filename2)