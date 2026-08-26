def simulate(x, y, vx, vy, dt, steps, integration_step, collision_check=None, collision_time_estimator=None):
    """Simulate the motion of an object under gravity for a given number of steps using specified integration method."""
    
    states = [(x, y, vx, vy)]
    if collision_check:
        if collision_check(x, y):
            return states
    for i in range(steps):
        x, y, vx, vy = integration_step(x, y, vx, vy, dt)
        if collision_check:
            if collision_check(x, y):
                if collision_time_estimator:
                    last_state = states[-1]
                    collision_time = collision_time_estimator(last_state, [x, y, vx, vy], dt)
                    x, y, vx, vy = integration_step(last_state[0], last_state[1], last_state[2], last_state[3], collision_time)
                states.append((x, y, vx, vy))
                return states
            else:
                states.append((x, y, vx, vy))
        else:
            states.append((x, y, vx, vy))
        
    return states