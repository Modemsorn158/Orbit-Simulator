from typing import Callable
from state import *
from math import inf

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

def simulate_system(
    initial_system: SystemState,
    dt: float,
    steps: int,
    system_integration_step: Callable[[SystemState, float, Callable[[SystemState], tuple[Vector2, ...]], list], SystemState],
    accelerations_model: Callable[[SystemState], tuple[Vector2, ...]],
    acceleration_args: list,
    collisions_check: Callable[[SystemState], list[tuple[int, int]]] | None = None,
    collisions_time_estimator: Callable[[SystemState, SystemState, tuple[int, int], float], float] | None = None
) -> list[SystemState]:
    """Simulate the motion of a system for a given number of steps using specified integration method."""
    
    systems = [initial_system]
    current_system = initial_system
    if collisions_check and collisions_check(current_system):
        return systems
    for _ in range(steps):
        next_system = system_integration_step(current_system, dt, accelerations_model, acceleration_args)
        if collisions_check:
            collisions = collisions_check(next_system)
            if collisions:
                if collisions_time_estimator:
                    t = inf
                    for pair in collisions:
                        t_calculated = collisions_time_estimator(current_system, next_system, pair, dt)
                        if t_calculated < t:
                            t = t_calculated
                    next_system = system_integration_step(current_system, t, accelerations_model, acceleration_args)                    
                systems.append(next_system)
                return systems
        current_system = next_system
        systems.append(current_system)
    return systems