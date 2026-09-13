from constants import GRAVITATIONAL_CONSTANT
from state import *

def gravitational_acceleration(
    position: Vector2,
    source: BodyState
) -> Vector2:
    """Calculate the gravitational acceleration at a given position vector and source in m/s^2."""
    
    r = (position - source.position).magnitude()
    if abs(r) < (10 ** -10):
        raise ValueError("Position is too close to the center of the source. Gravitational acceleration is undefined.")
    return ((position - source.position) * (-(GRAVITATIONAL_CONSTANT * source.body.mass) / (r ** 3)))

def system_gravitational_accelerations(
    system: SystemState
) -> tuple[Vector2, ...]:
    """Calculate the gravitational acceleration of a system in m/s^2."""

    body_states = system.body_states
    accelerations = [Vector2(0, 0) for _ in body_states]
    for body_index in range(len(body_states) - 1):
        body = body_states[body_index]
        for target_body_index in range(body_index + 1, len(body_states)):
            target_body = body_states[target_body_index]
            displacement = target_body.position - body.position
            distance = displacement.magnitude()
            if distance < 1e-10:
                raise ValueError("Position is too close to the center of another object. Gravitational acceleration is undefined.")
            gravity = (displacement * GRAVITATIONAL_CONSTANT / (distance ** 3))
            accelerations[body_index] += (gravity * target_body.body.mass)
            accelerations[target_body_index] -= (gravity * body.body.mass)
    return tuple(accelerations)