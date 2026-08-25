from gravity import gravitational_acceleration

def forward_euler_step(x, y, vx, vy, dt):
    """Perform a single time step using the Forward Euler method."""
    
    ax, ay = gravitational_acceleration(x, y)
    x_new = x + (vx * dt)
    y_new = y + (vy * dt)
    vx_new = vx + (ax * dt)
    vy_new = vy + (ay * dt)
    return x_new, y_new, vx_new, vy_new

def semi_implicit_euler_step(x, y, vx, vy, dt):
    """Perform a single time step using the Semi-Implicit Euler method."""
    
    ax, ay = gravitational_acceleration(x, y)
    vx_new = vx + (ax * dt)
    vy_new = vy + (ay * dt)
    x_new = x + (vx_new * dt)
    y_new = y + (vy_new * dt)
    return x_new, y_new, vx_new, vy_new

def velocity_verlet_step(x, y, vx, vy, dt):
    """Perform a single time step using the Velocity Verlet method."""
    
    ax, ay = gravitational_acceleration(x, y)
    x_new = x + (vx * dt) + (0.5 * ax * (dt ** 2))
    y_new = y + (vy * dt) + (0.5 * ay * (dt ** 2))
    ax_new, ay_new = gravitational_acceleration(x_new, y_new)
    vx_new = vx + (0.5 * (ax + ax_new) * dt)
    vy_new = vy + (0.5 * (ay + ay_new) * dt)
    return x_new, y_new, vx_new, vy_new