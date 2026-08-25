from gravity import gravitational_acceleration

def forward_euler_step(x, y, vx, vy, dt):
    """Perform a single time step using the Forward Euler method."""
    
    ax, ay = gravitational_acceleration(x, y)
    x_new = x + (vx * dt)
    y_new = y + (vy * dt)
    vx_new = vx + (ax * dt)
    vy_new = vy + (ay * dt)
    return x_new, y_new, vx_new, vy_new