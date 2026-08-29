from constants import GRAVITATIONAL_CONSTANT
from state import *

def gravitational_acceleration(
    position: Vector2,
    source: BodyState
) -> Vector2:
    """Calculate the gravitational acceleration at a given position vector and source in m/s^2."""
    
    r = (position - source.position).magnitude()
    if abs(r) < (10 ** -10):
        raise ValueError("Position is too close to the center of the source. Gravitational acceleration is undefined.")
    return ((position - source.position) * (-(GRAVITATIONAL_CONSTANT * source.body.mass) / (r ** 3)))