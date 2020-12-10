import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

from mini_topsim.main import mini_topsim
import mini_topsim.plot as srfplt

config_filename = None

if len(sys.argv) == 2:
    config_filename = sys.argv[1]
else:
    config_filename = 'config1.cfg'

config_file = os.path.join(filedir, config_filename)

if not config_file.endswith('.cfg'):
    print('Error: Config-file 1 does not end with .cfg')
    sys.exit()  
    
mini_topsim(config_file)


srf_filename1 = os.path.join(filedir,'etch_dx0_125.srf_save')
srf_filename2 = os.path.join(filedir,'etch_dx1.srf')
srfplotter = srfplt.plot(srf_filename1, srf_filename2)


