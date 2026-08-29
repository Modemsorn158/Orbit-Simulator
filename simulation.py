from typing import Callable
from state import *

def simulate(
    initial_state: BodyState,
    dt: float,
    steps: int,
    integration_step: Callable[[BodyState, float], BodyState],
    collision_check: Callable[[BodyState], bool] | None = None,
    collision_time_estimator: Callable[[BodyState, BodyState, float], float] | None = None    
) -> list[BodyState]:
    """Simulate the motion of a body for a given number of steps using specified integration method."""
    
    states: list[BodyState] = [initial_state]
    current_state = initial_state
    if collision_check and collision_check(current_state):
        return states
    for _ in range(steps):
        next_state = integration_step(current_state, dt)
        if collision_check and collision_check(next_state):
            if collision_time_estimator:
                t_colission = collision_time_estimator(current_state, next_state, dt)
                next_state = integration_step(current_state, t_colission)
            states.append(next_state)
            return states
        current_state = next_state
        states.append(current_state)
    return states