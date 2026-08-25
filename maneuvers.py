from math import sqrt

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