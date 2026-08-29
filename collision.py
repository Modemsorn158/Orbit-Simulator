from constants import EARTH_RADIUS
from state import BodyState

def has_collision_with_earth(
    state: BodyState
) -> bool:
    """Check if the body collides with Earth, accounting for body radius."""
    
    r = state.position.magnitude()
    return (r <= (EARTH_RADIUS + state.body.radius))

def estimate_earth_impact_time(
    state1: BodyState,
    state2: BodyState,
    dt: float
) -> float:
    """Returns the estimated collision time within the timestep."""
    
    alt1 = state1.position.magnitude() - (EARTH_RADIUS + state1.body.radius)
    alt2 = state2.position.magnitude() - (EARTH_RADIUS + state2.body.radius)
    if alt1 <= 0:
        raise ValueError("Previous altitude must be > 0")
    if alt2 > 0:
        raise ValueError("Current altitude must be <= 0")
    return ((alt1 / (alt1 - alt2)) * dt)