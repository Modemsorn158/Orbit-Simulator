from typing import Callable
from state import *

def forward_euler_step(
    state: BodyState,
    dt: float,
    acceleration_model: Callable[[Vector2, BodyState], Vector2],
    acceleration_args: list
) -> BodyState:
    """Perform a single time step using the Forward Euler method."""
    
    a = acceleration_model(state.position, *acceleration_args)
    position = state.position + (state.velocity * dt)
    velocity = state.velocity + (a * dt)
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )
    
def semi_implicit_euler_step(
    state: BodyState,
    dt: float,
    acceleration_model: Callable[[Vector2, BodyState], Vector2],
    acceleration_args: list
) -> BodyState:
    """Perform a single time step using the Semi-Implicit Euler method."""
    
    a = acceleration_model(state.position, *acceleration_args)
    velocity = state.velocity + (a * dt)
    position = state.position + (velocity * dt)
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )
    
def velocity_verlet_step(
    state: BodyState,
    dt: float,
    acceleration_model: Callable[[Vector2, BodyState], Vector2],
    acceleration_args: list
) -> BodyState:
    """Perform a single time step using the Velocity Verlet method."""
    
    a = acceleration_model(state.position, *acceleration_args)
    position = state.position + (state.velocity * dt) + (a * (0.5 * (dt ** 2)))
    velocity = state.velocity + ((a + acceleration_model(position, *acceleration_args)) * (0.5 * dt))
    return BodyState(
        body = state.body,
        position = position,
        velocity = velocity
    )