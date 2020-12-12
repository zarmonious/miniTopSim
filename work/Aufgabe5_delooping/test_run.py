"""
Testing the functionality of the deloog method
"""
import sys
import os
import pytest
import numpy as np
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)
from mini_topsim.main import mini_topsim
import mini_topsim.surface as surface
import mini_topsim.parameters as par

#def test_run():
#    """Test running miniTopSim."""
#    success = mini_topsim()
#    assert success, 'Error during executing miniTopSim.'

#@pytest.fixture()
#def set_param():
#    """Set parameter value."""
#    par.XMIN = -50.
#    par.XMAX = 50
#    par.DELTA_X = 1.
#    par.INITIAL_SURFACE_TYPE = 'Cosine'
#    par.FUN_XMIN = -25.
#    par.FUN_XMAX = 25.

#def test_surface(set_param):
#
#    assert par.XMIN == -50.
#    newsurface = surface.Surface()
#    newsurface.xvals = np.array((0.0, 1.0, 2.0, 1.0, 1.3, 2.0, 6.0))
#    newsurface.yvals = np.array((5.0, 5.5, 5.3, 4.0, 5.0, 5.5, 6.0))
