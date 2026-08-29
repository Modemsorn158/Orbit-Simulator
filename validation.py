from typing import Callable
from constants import GRAVITATIONAL_CONSTANT
from simulation import simulate
from diagnostics import specific_energy_history, relative_change_percent
from gravity import gravitational_acceleration
from state import *
from math import sqrt

def circular_orbit_max_energy_drift(
    state: BodyState,
    source: BodyState,
    dt: float,
    total_time: int,
    integration_step: Callable[[BodyState, float, Callable[[Vector2, BodyState], Vector2], list], BodyState]
) -> float:
    """Simulate a circular orbit and return the maximum percentage energy drift over the simulation."""
    
    if (total_time % dt) != 0:
        raise ValueError("Total time must be an integer multiple of dt.")
    position = (state.position - source.position)
    r = position.magnitude()
    if r == 0:
        raise ValueError("Position is at the origin of the other body.")
    vc = sqrt((GRAVITATIONAL_CONSTANT * source.body.mass) / r)
    unit_radius = position / r
    vcx = -(unit_radius.y * vc)
    vcy = unit_radius.x * vc
    new_state = BodyState(
        body = state.body,
        position = state.position,
        velocity = Vector2(
            x = vcx + source.velocity.x,
            y = vcy + source.velocity.y
        )
    )
    states = simulate(new_state, dt, int(total_time // dt), integration_step, gravitational_acceleration, [source])
    energy_history = specific_energy_history(states, source)
    relative_change = relative_change_percent(energy_history)
    return max(abs(change) for change in relative_change)