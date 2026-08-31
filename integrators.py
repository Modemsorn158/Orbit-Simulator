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
    
def system_forward_euler_step(
    system: SystemState,
    dt: float,
    accelerations_model: Callable[[SystemState], tuple[Vector2, ...]],
    acceleration_args: list
) -> SystemState:
    """Perform a single time step on a system using the Forward Euler method."""
    
    accelerations = accelerations_model(system, *acceleration_args)
    body_states = []
    for i in range(len(system.body_states)):
        state = system.body_states[i]
        a = accelerations[i]
        position = state.position + (state.velocity * dt)
        velocity = state.velocity + (a * dt)
        new_state = BodyState(
            body = state.body,
            position = position,
            velocity = velocity
        )
        body_states.append(new_state)
    return SystemState(
        body_states = tuple(body_states),
        time = (system.time + dt)
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
    
def system_semi_implicit_euler_step(
    system: SystemState,
    dt: float,
    accelerations_model: Callable[[SystemState], tuple[Vector2, ...]],
    acceleration_args: list
) -> SystemState:
    """Perform a single time step on a system using the Semi-Implicit Euler method."""
    
    accelerations = accelerations_model(system, *acceleration_args)
    body_states = []
    for i in range(len(system.body_states)):
        state = system.body_states[i]
        a = accelerations[i]
        velocity = state.velocity + (a * dt)
        position = state.position + (velocity * dt)
        new_state = BodyState(
            body = state.body,
            position = position,
            velocity = velocity
        )
        body_states.append(new_state)
    return SystemState(
        body_states = tuple(body_states),
        time = (system.time + dt)
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
    
def system_velocity_verlet_step(
    system: SystemState,
    dt: float,
    accelerations_model: Callable[[SystemState], tuple[Vector2, ...]],
    acceleration_args: list
) -> SystemState:
    """Perform a single time step on a system using the Velocity Verlet method."""
    
    accelerations = accelerations_model(system, *acceleration_args)
    temp_system_body = []
    for i in range(len(system.body_states)):
        a = accelerations[i]
        state = system.body_states[i]
        position = state.position + (state.velocity * dt) + (a * (0.5 * (dt ** 2)))
        new_state = BodyState(
            body = state.body,
            position = position,
            velocity = state.velocity
        )
        temp_system_body.append(new_state)
    temp_system_state = SystemState(
        body_states = tuple(temp_system_body),
        time = (system.time + dt)
    )
    new_accelerations = accelerations_model(temp_system_state, *acceleration_args)
    body_states = []
    for i in range(len(system.body_states)):
        a0 = accelerations[i]
        a1 = new_accelerations[i]
        state = temp_system_state.body_states[i]
        velocity = state.velocity + ((a0 + a1) * (0.5 * dt))
        new_state = BodyState(
            body = state.body,
            position = state.position,
            velocity = velocity
        )
        body_states.append(new_state)
    return SystemState(
        body_states = tuple(body_states),
        time = (temp_system_state.time)
    )