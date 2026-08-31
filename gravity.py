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
    
    a = []
    for body_index in range(len(system.body_states)):
        body = system.body_states[body_index]
        a_body = Vector2(0, 0)
        for target_body_index in range(len(system.body_states)):
            target_body = system.body_states[target_body_index]
            if not (body_index == target_body_index):
                displacement = (target_body.position - body.position)
                distance = displacement.magnitude()
                if abs(distance) < (10 ** -10):
                    raise ValueError("Position is too close to the center of the another object. Gravitational acceleration is undefined.")
                a_body += (displacement * GRAVITATIONAL_CONSTANT * target_body.body.mass) / (distance ** 3)
        a.append(a_body)
    return tuple(a)