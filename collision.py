from state import *

def has_collision_with_body(
    state: BodyState,
    body_state: BodyState
) -> bool:
    """Check if the body collides with target body, accounting for body radius."""
    
    r = (state.position - body_state.position).magnitude()
    return (r <= (body_state.body.radius + state.body.radius))

def estimate_body_impact_time(
    state1: BodyState,
    state2: BodyState,
    body_state: BodyState,
    dt: float
) -> float:
    """Returns the estimated collision time within the timestep for a static object and moving object."""
    
    alt1 = (state1.position - body_state.position).magnitude() - (body_state.body.radius + state1.body.radius)
    alt2 = (state2.position - body_state.position).magnitude() - (body_state.body.radius + state2.body.radius)
    if alt1 <= 0:
        raise ValueError("Previous altitude must be > 0")
    if alt2 > 0:
        raise ValueError("Current altitude must be <= 0")
    return ((alt1 / (alt1 - alt2)) * dt)

def system_check_collision(
    system: SystemState
) -> list[tuple[int, int]]:
    """Returns all colliding objects and its pair in the system"""
    
    collisions = []
    for i in range(len(system.body_states)):
        for j in range(len(system.body_states)):
            if i < j:
                state1 = system.body_states[i]
                state2 = system.body_states[j]
                r = (state1.position - state2.position).magnitude()
                if (r <= (state1.body.radius + state2.body.radius)):
                    collisions.append(tuple([i, j]))
    return collisions

def estimate_system_impact_time(
    system1: SystemState,
    system2: SystemState,
    pair: tuple[int, int],
    dt: float
) -> float:
    """Return the estimated collision time within the timestep for a system."""
    
    body1_system1 = system1.body_states[pair[0]]
    body2_system1 = system1.body_states[pair[1]]
    body1_system2 = system2.body_states[pair[0]]
    body2_system2 = system2.body_states[pair[1]]
    d0 = (body1_system1.position - body2_system1.position).magnitude() - (body1_system1.body.radius + body2_system1.body.radius)
    d1 = (body1_system2.position - body2_system2.position).magnitude() - (body1_system2.body.radius + body2_system2.body.radius)
    if d0 <= 0:
        raise ValueError("Previous distance must be > 0 subtracting radius")
    if d1 > 0:
        raise ValueError("Current distance must be <= 0 subtracting radius")
    t = (d0 / (d0 - d1)) * dt
    return t