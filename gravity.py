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

    states = system.body_states
    n = len(states)
    ax = [0.0] * n
    ay = [0.0] * n
    for i in range(n - 1):
        body_i = states[i]
        xi = body_i.position.x
        yi = body_i.position.y
        mi = body_i.body.mass
        for j in range(i + 1, n):
            body_j = states[j]
            dx = body_j.position.x - xi
            dy = body_j.position.y - yi
            r2 = dx * dx + dy * dy
            inverted_r3 = 1.0 / (r2 * sqrt(r2))
            scale = GRAVITATIONAL_CONSTANT * inverted_r3
            gx = dx * scale
            gy = dy * scale
            mj = body_j.body.mass
            ax[i] += gx * mj
            ay[i] += gy * mj
            ax[j] -= gx * mi
            ay[j] -= gy * mi
    return tuple(Vector2(ax[i], ay[i]) for i in range(n))