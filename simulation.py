def simulate(x, y, vx, vy, dt, steps, integration_step, collision_check=None):
    """Simulate the motion of an object under gravity for a given number of steps using specified integration method."""
    
    if collision_check:
        states = [(x, y, vx, vy)]
        if collision_check(x, y):
            return states
    else:
        states = [(x, y, vx, vy)]
    for i in range(steps):
        x, y, vx, vy = integration_step(x, y, vx, vy, dt)
        if collision_check:
            states.append((x, y, vx, vy))
            if collision_check(x, y):
                return states
        else:
            states.append((x, y, vx, vy))
        
    return states