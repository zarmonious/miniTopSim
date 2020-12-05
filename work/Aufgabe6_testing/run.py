import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import pytest
from mini_topsim.main import mini_topsim
import mini_topsim.parameters as par

mini_topsim()

def test_run():
    """Test running miniTopSim."""
    success = mini_topsim()
    assert success, 'Error during executing miniTopSim.'


@pytest.fixture()
def set_param():
    """Set parameter value."""
    par.TestParameter = 56

def test_set_param(set_param):
    """Test setting a parameter value."""
    assert par.TestParameter == 56
