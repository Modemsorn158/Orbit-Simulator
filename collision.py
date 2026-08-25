from constants import EARTH_RADIUS
from math import sqrt

def has_collision_with_earth(x, y):
    r = sqrt((x ** 2) + (y ** 2))
    collision = (r <= EARTH_RADIUS)
    return collision