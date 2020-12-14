#import pytest
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import mini_topsim.plot as srfplt
from mini_topsim.surface import Surface
from mini_topsim.main import mini_topsim
import mini_topsim.parameters as par

config_file = os.path.join(filedir,'cosine_2.cfg')

mini_topsim(config_file)



def test_calc_distance():
    """
    calculates distance between surfaces and tests it with treshold value
    
    calculates distance between cosine_2.srf andcosine.srf_save and
    tests it with treshold value calculated in calc_distance
    
    """
  
    srf_filename1 = os.path.join(filedir,'cosine_2.srf')
    srf_filename2 = os.path.join(filedir,'cosine.srf_save')
    srfplotter = srfplt._SurfacePlotter(srf_filename1, srf_filename2)
    
    srf1 = Surface()
    srf1.xvals = srfplotter.xpoints_list[-1]
    srf1.yvals = srfplotter.ypoints_list[-1]
    
    srf2 = Surface()
    srf2.xvals = srfplotter.refsrf.xpoints_list[-1]
    srf2.yvals = srfplotter.refsrf.ypoints_list[-1]

    dist = srf1.distance(srf2)
   
    
    assert dist <= 1e-9

