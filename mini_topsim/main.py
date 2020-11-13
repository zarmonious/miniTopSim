"""
Main script and function to run miniTopSim.
"""
from . import parameters as par

def mini_topsim():
   print('Running miniTopSim ...')
   print('TestParameter={}'.format(par.TestParameter))
   return True
   
if __name__ == '__main__':
   mini_topsim()
