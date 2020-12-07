import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

#import pytest
from mini_topsim.main import mini_topsim
import mini_topsim.plot as srfplt

config_filename1 = None
config_filename2 = None

if len(sys.argv) == 2:
    config_filename1 = sys.argv[1]
elif len(sys.argv) == 3:
    config_filename1 = sys.argv[1]
    config_filename2 = sys.argv[2]
else:
    config_filename1 = 'config1.cfg'

config_file1 = os.path.join(os.path.dirname(__file__), config_filename1)

if not config_file1.endswith('.cfg'):
    print('Error: Config-file 1 does not end with .cfg')
    sys.exit() 

if config_filename2 != None:
    config_file2 = os.path.join(os.path.dirname(__file__), config_filename2)
    if not config_file2.endswith('.cfg'):
        print('Error: Config-file 2 does not end with .cfg')
        sys.exit()   
    
#mini_topsim(config_filename1)

srf_filename1 = 'etch_dx0_125.srf'
srf_filename2 = 'etch_dx1.srf' #None

srfplt.plot(srf_filename1, srf_filename2)
#srfplt.plot(srf_filename1)



# def test_run(): 
#     """Test running miniTopSim."""
#     success = mini_topsim()
#     assert success, 'Error during executing miniTopSim.'


# @pytest.fixture()
# def set_param():
#     """Set parameter value."""
#     par.TestParameter = 56

# def test_set_param(set_param):
#     """Test setting a parameter value."""
#     assert par.TestParameter == 56
