from constants import GRAVITATIONAL_CONSTANT
from state import *
from math import sqrt, pi

def specific_orbital_energy(
    state: BodyState,
    source: BodyState                            
) -> float:
    """Calculate the specific orbital energy of an object in orbit."""
    
    v = ((state.velocity - source.velocity).magnitude()) ** 2
    r = (state.position - source.position).magnitude()
    if r == 0:
        raise ValueError("Position is at the origin of the other body; Orbital energy undefined")
    energy = (v / 2) - ((GRAVITATIONAL_CONSTANT * source.body.mass) / r)
    return energy

def specific_energy_history(
    states: list[BodyState],
    source: BodyState
) -> list[float]:
    """Calculate the specific orbital energy for a list of states."""
    
    energy_history = []
    for state in states:
        energy = specific_orbital_energy(state, source)
        energy_history.append(energy)
    return energy_history

def relative_change_percent(
    values: list[float]
) -> list[float]:
    """Calculate the relative change percentage of a list of values compared to the initial value."""
    
    if values[0] == 0:
        raise ValueError("Initial value is zero; relative change percentage is undefined.")
    initial_value = values[0]
    reference_size = abs(initial_value)
    return [(value - initial_value) / reference_size * 100 for value in values]

def specific_angular_momentum(
    state: BodyState,
    source: BodyState
) -> float:
    """Calculate the specific angular momentum of an object in orbit."""
    
    position = state.position - source.position
    velocity = state.velocity - source.velocity
    h = (position.x * velocity.y) - (position.y * velocity.x)
    return h

def specific_angular_momentum_history(
    states: list[BodyState],
    source: BodyState
) -> list[float]:
    """Calculate the specific angular momentum for a list of states."""
    
    h_history = []
    for state in states:
        h = specific_angular_momentum(state, source)
        h_history.append(h)
    return h_history

def semi_major_axis(
    state: BodyState,
    source: BodyState                    
) -> float:
    """Calculate the semi-major axis of an orbit given position and velocity."""
    
    energy = specific_orbital_energy(state, source)
    if energy >= 0:
        raise ValueError("Orbit is not bound; semi-major axis is undefined.")
    a = -((GRAVITATIONAL_CONSTANT * source.body.mass) / (2 * energy))
    return a

def eccentricity(
    state: BodyState,
    source: BodyState
):
    """Calculate the eccentricity of an orbit given position and velocity."""
    
    energy = specific_orbital_energy(state, source)
    h = specific_angular_momentum(state, source)
    e0 = 1 + ((2 * energy * (h ** 2)) / ((GRAVITATIONAL_CONSTANT * source.body.mass) ** 2))
    e0 = max(e0, 0)
    e = sqrt(e0)
    return e

def apsides(
    state: BodyState,
    source: BodyState
) -> tuple[float, float]:
    """Calculate the periapsis and apoapsis distances of an orbit given position and velocity."""
    
    a = semi_major_axis(state, source)
    e = eccentricity(state, source)
    r_periapsis = a * (1 - e)
    r_apoapsis = a * (1 + e)
    return r_periapsis, r_apoapsis

def orbital_period(
    state: BodyState,
    source: BodyState
) -> float:
    """Calculate the orbital period of an orbit given position and velocity."""
    
    a = semi_major_axis(state, source)
    T = 2 * pi * sqrt((a ** 3) / (GRAVITATIONAL_CONSTANT * source.body.mass))
    return T

def altitude(
    position: Vector2,
    source: BodyState
) -> float:
    """Calculate the altitude of an object above a body's surface given its position."""
    
    r = (position - source.position).magnitude()
    altitude = r - source.body.radius
    return altitude

def speed(
    velocity: Vector2,
    source: BodyState
) -> float:
    """Calculate the speed of an object given its velocity relative to another object."""
    
    v = (velocity - source.velocity).magnitude()
    return v

def radial_velocity(
    state: BodyState,
    source: BodyState
) -> float:
    """Calculate the radial velocity of an object given its position and velocity relative to another object."""
    
    position = state.position - source.position
    velocity = state.velocity - source.velocity
    r = position.magnitude()
    if r == 0:
        raise ValueError("Position is at the origin of the other body; radial velocity is undefined.")
    vr = ((position.x * velocity.x) + (position.y * velocity.y)) / r
    return vr

def find_apsis_events(
    states: list[BodyState],
    source: BodyState,
    dt: float
) -> list:
    """Find the event, time and states of periapsis and apoapsis events in a list of states."""
    
    events = []
    previous_radial_velocity = radial_velocity(states[0], source)
    for i in range(1, len(states)):
        state = states[i]
        current_radial_velocity = radial_velocity(state, source)
        if previous_radial_velocity < 0 and current_radial_velocity >= 0:
            event_time = i * dt
            events.append(("Periapsis", event_time, state))
        if previous_radial_velocity > 0 and current_radial_velocity <= 0:
            event_time = i * dt
            events.append(("Apoapsis", event_time, state))
        previous_radial_velocity = current_radial_velocity
    return events

def escape_velocity(
    position: Vector2,
    source: BodyState
) -> float:
    """Calculate the escape velocity at a given position."""
    
    r = (position - source.position).magnitude()
    if r == 0:
        raise ValueError("Position is at the origin of the other body; escape velocity is undefined.")
    ve = sqrt((2 * (GRAVITATIONAL_CONSTANT * source.body.mass)) / r)
    return ve