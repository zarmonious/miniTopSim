import pytest
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import mini_topsim.plot as srfplt
from mini_topsim.surface import Surface
from mini_topsim.main import mini_topsim

config_file = os.path.join(filedir,'etch_dx1.cfg')
mini_topsim(config_file)

@pytest.fixture()
def calc_distance():
    """tests if distance between two surfaces is below 0.5*dist_treshold"""
        
    srf_filename1 = os.path.join(filedir,'etch_dx1.srf')
    srf_filename2 = os.path.join(filedir,'etch_dx1.srf_save')
    srfplotter = srfplt._SurfacePlotter(srf_filename1, srf_filename2)
    
    srf1 = Surface()
    srf1.xvals = srfplotter.xpoints_list[-1]
    srf1.yvals = srfplotter.ypoints_list[-1]
    
    srf2 = Surface()
    srf2.xvals = srfplotter.refsrf.xpoints_list[-1]
    srf2.yvals = srfplotter.refsrf.ypoints_list[-1]
    
    global dist
    dist = srf1.distance(srf2)

def test_calc_distance(calc_distance):
    """tests if distance between two surfaces is below 0.5*dist_treshold"""
  
    srf_filename1 = os.path.join(filedir,'etch_dx1.srf')
    srf_filename2 = os.path.join(filedir,'etch_dx1.srf_save')
    srfplotter = srfplt._SurfacePlotter(srf_filename1, srf_filename2)
    
    srf1 = Surface()
    srf1.xvals = srfplotter.xpoints_list[-1]
    srf1.yvals = srfplotter.ypoints_list[-1]
    
    srf2 = Surface()
    srf2.xvals = srfplotter.refsrf.xpoints_list[-1]
    srf2.yvals = srfplotter.refsrf.ypoints_list[-1]
    
    assert srf1.distance(srf2) <= 0.5 * dist

