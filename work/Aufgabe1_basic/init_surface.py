#%%

import numpy as np
import math

def init_surface(xVals):
    return np.array([0 
                    if (x < -24 or x > 24) 
                    else (-50*(1+math.cos((2*math.pi*x)/50))) 
                    for x in xVals])
# %%
