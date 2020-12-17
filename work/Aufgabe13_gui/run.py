import os, sys

current_dir = os.path.dirname(__file__)
codedir = os.path.join(current_dir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

from gui import main

command_line = [codedir, 'Initial', 'Conditions']
#command_line = [codedir, 'Setup']

window = main(command_line)
