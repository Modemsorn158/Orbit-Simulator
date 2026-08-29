from constants import GRAVITATIONAL_CONSTANT
from state import *
from math import sqrt, pi

def apply_delta_v(
    velocity: Vector2,
    delta_velocity: Vector2
) -> Vector2:
    """Apply a delta-v to the current velocity."""
    
    velocity = velocity + delta_velocity
    return velocity

def apply_prograde_delta_v(
    velocity: Vector2,
    source_velocity: Vector2,
    delta_velocity: float
) -> Vector2:
    """Apply a prograde delta-v to the current velocity components."""
    
    relative_velocity = (velocity - source_velocity)
    speed = relative_velocity.magnitude()
    if speed == 0:
        raise ValueError("Current velocity is zero; cannot apply prograde delta-v.")
    unit_velocity = relative_velocity / speed
    return apply_delta_v(velocity, (delta_velocity * unit_velocity))

def hohmann_transfer(
    r1: float,
    r2: float,
    source: BodyState
):
    """Calculate the delta-v required for a Hohmann transfer between two circular orbits."""
    
    if r1 <= 0 or r2 <= 0:
        raise ValueError("Orbit radii must be positive.")
    if r1 == r2:
        raise ValueError("Orbit radii must be different for a Hohmann transfer.")
    vc1 = sqrt((GRAVITATIONAL_CONSTANT * source.body.mass) / r1)
    vc2 = sqrt((GRAVITATIONAL_CONSTANT * source.body.mass) / r2)
    a_transfer = (r1 + r2) / 2
    v_transfer_periapsis = sqrt((GRAVITATIONAL_CONSTANT * source.body.mass) * ((2 / r1) - (1 / a_transfer)))
    v_transfer_apoapsis = sqrt((GRAVITATIONAL_CONSTANT * source.body.mass) * ((2 / r2) - (1 / a_transfer)))
    delta_v1 = v_transfer_periapsis - vc1
    delta_v2 = vc2 - v_transfer_apoapsis
    t = pi * sqrt((a_transfer ** 3) / (GRAVITATIONAL_CONSTANT * source.body.mass))
    return delta_v1, delta_v2, t