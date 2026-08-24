from constants import EARTH_MU
from math import sqrt

def gravitational_acceleration(x, y):
    """Calculate the gravitational acceleration at a given position (x, y) and returns acceleration in both vectors (ax, ay) in meters."""
    
    r = sqrt((x ** 2) + (y ** 2))
    ax = -(EARTH_MU * x) / (r ** 3)
    if abs(ax) < 1e-10:
        ax = ValueError("Gravitational acceleration is too small to be calculated accurately.")
    ay = -(EARTH_MU * y) / (r ** 3)
    if abs(ay) < 1e-10:
        ay = ValueError("Gravitational acceleration is too small to be calculated accurately.")
    return ax, ay