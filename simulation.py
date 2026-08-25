def simulate(x, y, vx, vy, dt, steps, integration_step):
    """Simulate the motion of an object under gravity for a given number of steps using specified integration method."""
    
    states = [(x, y, vx, vy)]
    for i in range(steps):
        x, y, vx, vy = integration_step(x, y, vx, vy, dt)
        states.append((x, y, vx, vy))
    return states