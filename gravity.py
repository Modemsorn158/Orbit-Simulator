from constants import EARTH_MU
from state import *

def gravitational_acceleration(
    position: Vector2
) -> Vector2:
    """Calculate the gravitational acceleration at a given position vector in m/s^2."""
    
    r = position.magnitude()
    if abs(r) < (10 ** -10):
        raise ValueError("Position is too close to the center of the Earth. Gravitational acceleration is undefined.")
    return (position * (-EARTH_MU / (r ** 3)))