"""
Template for testing miniTopSim using pytest.

Feel free to copy, but do not modify the original!
"""
import pytest
from mini_topsim.main import mini_topsim
import mini_topsim.parameters as par

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

