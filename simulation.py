from integrators import forward_euler_step

def simulate(x, y, vx, vy, dt, steps):
    """Simulate the motion of an object under gravity for a given number of steps."""
    
    positions = [(x, y)]
    for i in range(steps):
        x, y, vx, vy = forward_euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
    return positions