from typing import Callable
from state import *

def simulate(
    initial_state: BodyState,
    dt: float,
    steps: int,
    integration_step: Callable[[BodyState, float, Callable[[Vector2, BodyState], Vector2], list], BodyState],
    acceleration_model: Callable[[Vector2, BodyState], Vector2],
    acceleration_args: list,
    collision_check: Callable[[BodyState, BodyState], bool] | None = None,
    collision_time_estimator: Callable[[BodyState, BodyState, BodyState, float], float] | None = None,
    collision_body: BodyState | None = None
) -> list[BodyState]:
    """Simulate the motion of a body for a given number of steps using specified integration method."""
    
    states: list[BodyState] = [initial_state]
    current_state = initial_state
    if collision_check and collision_body and collision_check(current_state, collision_body):
        return states
    for _ in range(steps):
        next_state = integration_step(current_state, dt, acceleration_model, acceleration_args)
        if collision_check and collision_body and collision_check(next_state, collision_body):
            if collision_time_estimator:
                t_colission = collision_time_estimator(current_state, next_state, collision_body, dt)
                next_state = integration_step(current_state, t_colission, acceleration_model, acceleration_args)
            states.append(next_state)
            return states
        current_state = next_state
        states.append(current_state)
    return states