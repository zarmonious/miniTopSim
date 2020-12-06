import parameters as par
import numpy as np



def init_sputtering():
    global get_sputter_yield
    if par.SPUTTER_YIELD_FILE is "":
        get_sputter_yield = Sputter_yield_Yamamura(par.SPUTTER_YIELD_0,
            par.SPUTTER_YIELD_F, par.SPUTTER_YIELD_B)
    else:
        get_sputter_yield = Sputter_yield_table(par.SPUTTER_YIELD_FILE)

class Sputter_yield_Yamamura():
    def __init__(self, Y0,f, b):
        self.Y0 = Y0
        self.f = f
        self.b = b
    
    def __call__(self, costheta):
        Y=self.Y0*costheta**(-self.f) * np.exp(self.b*(1-1/costheta))
        Y[np.isnan(Y)]=0
        return Y

class Sputter_yield_table():
    def __init__(self, File):
        self.File = File

    def __call__(self):
        return None
