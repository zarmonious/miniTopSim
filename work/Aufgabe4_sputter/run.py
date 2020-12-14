import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)
import mini_topsim.main as mtp

#Run minitopsim
mtp.mini_topsim()