from constants import EARTH_RADIUS
from diagnostics import altitude
from math import sqrt

def has_collision_with_earth(x, y):
    r = sqrt((x ** 2) + (y ** 2))
    collision = (r <= EARTH_RADIUS)
    return collision

def estimate_earth_impact_time(state1, state2, dt):
    """Returns the estimated collision time within the timestep."""
    
    position1 = [state1[0], state1[1]]
    position2 = [state2[0], state2[1]]
    alt1 = altitude(position1[0], position1[1])
    alt2 = altitude(position2[0], position2[1])
    if alt1 <= 0:
        raise ValueError("Previous altitude must be > 0")
    elif alt2 > 0:
        raise ValueError("Current altitude must be <= 0")
    t = (alt1 / (alt1 - alt2)) * dt
    return t