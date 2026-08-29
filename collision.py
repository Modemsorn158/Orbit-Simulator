from state import BodyState

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