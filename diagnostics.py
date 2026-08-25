from constants import EARTH_MU
from math import sqrt

def specific_orbital_energy(x, y, vx, vy):
    """Calculate the specific orbital energy of an object in orbit."""
    
    r = sqrt((x ** 2) + (y ** 2))
    v2 = (vx ** 2) + (vy ** 2)
    energy = (v2 / 2) - (EARTH_MU / r)
    return energy