from constants import EARTH_MU
from math import sqrt

def gravitational_acceleration(x, y):
    """Calculate the gravitational acceleration at a given position (x, y) and returns acceleration in both vectors (ax, ay) in meters."""
    
    r = sqrt((x ** 2) + (y ** 2))
    if abs(r) < 1e-10:
        raise ValueError("Position is too close to the center of the Earth. Gravitational acceleration is undefined.")
    ax = -(EARTH_MU * x) / (r ** 3)
    ay = -(EARTH_MU * y) / (r ** 3)
    return ax, ay