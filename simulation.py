from integrators import forward_euler_step, semi_implicit_euler_step

def simulate_forward_euler(x, y, vx, vy, dt, steps):
    """Simulate the motion of an object under gravity for a given number of steps using Forward Euler."""
    
    positions = [(x, y)]
    for i in range(steps):
        x, y, vx, vy = forward_euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
    return positions

def simulate_semi_implicit_euler(x, y, vx, vy, dt, steps):
    """Simulate the motion of an object under gravity for a given number of steps using Semi-Implicit Euler."""
    
    positions = [(x, y)]
    for i in range(steps):
        x, y, vx, vy = semi_implicit_euler_step(x, y, vx, vy, dt)
        positions.append((x, y))
    return positions