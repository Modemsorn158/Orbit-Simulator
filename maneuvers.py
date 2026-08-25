def apply_delta_v(vx, vy, delta_vx, delta_vy):
    """Apply a delta-v to the current velocity components."""
    
    new_vx = vx + delta_vx
    new_vy = vy + delta_vy
    return new_vx, new_vy