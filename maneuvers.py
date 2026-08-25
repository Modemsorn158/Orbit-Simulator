from constants import EARTH_MU
from math import sqrt, pi

def apply_delta_v(vx, vy, delta_vx, delta_vy):
    """Apply a delta-v to the current velocity components."""
    
    new_vx = vx + delta_vx
    new_vy = vy + delta_vy
    return new_vx, new_vy

def apply_prograde_delta_v(vx, vy, delta_v):
    """Apply a prograde delta-v to the current velocity components."""
    
    speed = sqrt((vx ** 2) + (vy ** 2))
    if speed == 0:
        raise ValueError("Current velocity is zero; cannot apply prograde delta-v.")
    unit_vx = vx / speed
    unit_vy = vy / speed
    return apply_delta_v(vx, vy, (delta_v * unit_vx), (delta_v * unit_vy))

def hohmann_transfer(r1, r2):
    """Calculate the delta-v required for a Hohmann transfer between two circular orbits."""
    
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbit radii must be positive.")
    if r1 == r2:
        raise ValueError("Orbit radii must be different for a Hohmann transfer.")
    vc1 = sqrt(EARTH_MU / r1)
    vc2 = sqrt(EARTH_MU / r2)
    a_transfer = (r1 + r2) / 2
    v_transfer_periapsis = sqrt(EARTH_MU * ((2 / r1) - (1 / a_transfer)))
    v_transfer_apoapsis = sqrt(EARTH_MU * ((2 / r2) - (1 / a_transfer)))
    delta_v1 = v_transfer_periapsis - vc1
    delta_v2 = vc2 - v_transfer_apoapsis
    t = pi * sqrt((a_transfer ** 3) / EARTH_MU)
    return delta_v1, delta_v2, t