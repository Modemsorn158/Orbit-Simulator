from gravity import gravitational_acceleration
from state import *

def forward_euler_step(
    state: BodyState,
    dt: float
) -> BodyState:
    """Perform a single time step using the Forward Euler method."""
    
    a = gravitational_acceleration(state.position)
    position = state.position + (state.velocity * dt)
    velocity = state.velocity + (a * dt)
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )
    
def semi_implicit_euler_step(
    state: BodyState,
    dt: float
) -> BodyState:
    """Perform a single time step using the Semi-Implicit Euler method."""
    
    a = gravitational_acceleration(state.position)
    velocity = state.velocity + (a * dt)
    position = state.position + (velocity * dt)
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )
    
def velocity_verlet_step(
    state: BodyState,
    dt: float
) -> BodyState:
    """Perform a single time step using the Velocity Verlet method."""
    
    a = gravitational_acceleration(state.position)
    position = state.position + (state.velocity * dt) + (a * (0.5 * (dt ** 2)))
    velocity = state.velocity + ((a + gravitational_acceleration(position)) * (0.5 * dt))
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )