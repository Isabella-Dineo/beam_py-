#!/usr/bin/env python 

import numpy as np
from scipy import constants
import emission_height

def rho(P, hmin, hmax):
    """Function to determine the opening angle rho given the rotational period and emission height.
    
       Args:
       -----
       P   : rotational period (seconds)
       H   : emission height (km)
       
       Returns:
       --------
       rho : the opening angle (degrees)

    """

    H = emission_height(P, hmin, hmax)
    rho = np.degrees(np.sqrt((9 * np.pi * H) / (2 * constants.c * P)))
    
    return rho

############ simple test #########################################
if __name__ == "__main__":
    H = np.linspace(950,1000, num=10, endpoint=True)
    P = 0.15
    rhos = rho(P, H)