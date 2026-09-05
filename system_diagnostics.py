from constants import GRAVITATIONAL_CONSTANT
from state import *
from math import sqrt, pi

def total_linear_momentum(
    system: SystemState
) -> Vector2:
    """Calculate the total linear momentum of a system."""
    
    P = Vector2(0, 0)
    for state in system.body_states:
        P = P + (state.body.mass * state.velocity)
    return P

def center_of_mass(
    system: SystemState
) -> Vector2:
    """Calculate the center of mass of a system."""
    
    found_mass = False
    numerator = Vector2(0, 0)
    denominator = 0
    for state in system.body_states:
        if state.body.mass > 0:
            found_mass = True
        numerator = numerator + (state.body.mass * state.position)
        denominator = denominator + state.body.mass
    if not found_mass:
        raise ValueError("Center of mass can't be calculated: All bodies in system are massless.")
    return (numerator / denominator)

def total_angular_momentum(
    system: SystemState
) -> float:
    """Calculate the total angular momentum of a system."""
    
    L = 0
    for state in system.body_states:
        L = L + (state.body.mass * ((state.position.x * state.velocity.y) - (state.position.y * state.velocity.x)))
    return L

def total_mechanical_energy(
    system: SystemState
) -> float:
    """Calculate the total mechanical energy of a system."""
    
    K = 0
    U = 0
    for i in range(len(system.body_states)):
        state = system.body_states[i]
        K = K + ((1 / 2) * (state.body.mass * (state.velocity.magnitude() ** 2)))
        for j in range(len(system.body_states)):
            if i < j:
                state2 = system.body_states[j]
                U = U + ((GRAVITATIONAL_CONSTANT * state.body.mass * state2.body.mass) / (state.position - state2.position).magnitude())
    U = -U
    return (K + U)

def relative_position(
    system: SystemState,
    pair: tuple[int, int]
) -> Vector2:
    """Return positional difference in Vector2."""
    
    position1 = system.body_states[pair[0]].position
    position2 = system.body_states[pair[1]].position
    return (position2 - position1)

def relative_velocity(
    system: SystemState,
    pair: tuple[int, int]
) -> Vector2:
    """Return velocity difference in Vector2."""
    
    velocity1 = system.body_states[pair[0]].velocity
    velocity2 = system.body_states[pair[1]].velocity
    return (velocity2 - velocity1)

def pair_gravitational_parameter(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return gravitational parameter (mu) between 2 bodies."""
    
    mass1 = system.body_states[pair[0]].body.mass
    mass2 = system.body_states[pair[1]].body.mass
    return (GRAVITATIONAL_CONSTANT * (mass1 + mass2))

def pair_distance(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the distance between 2 bodies."""
    
    return relative_position(system, pair).magnitude()

def pair_speed(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the relative speed between 2 bodies."""
    
    return relative_velocity(system, pair).magnitude()

def pair_radial_velocity(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the radial velocity between 2 bodies."""
    
    position = relative_position(system, pair)
    distance = position.magnitude()
    velocity = relative_velocity(system, pair)
    if distance == 0:
        raise ValueError("Distance between the 2 bodies is zero; No radial velocity defined.")
    return ((position @ velocity) / distance)

def pair_specific_orbital_energy(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the relative specific orbital energy between 2 bodies."""
    
    position = relative_position(system, pair)
    distance = position.magnitude()
    if distance == 0:
        raise ValueError("Distance between the 2 bodies is zero.")
    velocity = relative_velocity(system, pair)
    speed = velocity.magnitude()
    mu = pair_gravitational_parameter(system, pair)
    return (((speed ** 2) / 2) - (mu / distance))

def pair_specific_angular_momentum(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the relative specific angular momentum between 2 bodies."""
    
    position = relative_position(system, pair)
    velocity = relative_velocity(system, pair)
    return ((position.x * velocity.y) - (position.y * velocity.x))

def pair_semi_major_axis(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the relative semi-major axis between 2 bodies."""
    
    energy = pair_specific_orbital_energy(system, pair)
    if energy >= 0:
        raise ValueError("Orbit is not bound.")
    mu = pair_gravitational_parameter(system, pair)
    return -(mu / (2 * energy))

def pair_eccentricity(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the relative eccentricity between 2 bodies."""
    
    energy = pair_specific_orbital_energy(system, pair)
    h = pair_specific_angular_momentum(system, pair)
    mu = pair_gravitational_parameter(system, pair)
    return sqrt(max((1 + ((2 * energy * (h ** 2)) / (mu**2))), 0))

def pair_apsides(
    system: SystemState,
    pair: tuple[int, int]
) -> tuple[float, float]:
    """Return the relative periapsis and apoapsis of the 2 bodies."""
    
    a = pair_semi_major_axis(system, pair)
    e = pair_eccentricity(system, pair)
    return ((a * (1 - e)), (a * (1 + e)))

def pair_period(
    system: SystemState,
    pair: tuple[int, int]
) -> float:
    """Return the orbital period of the 2 bodies relative to each other."""
    
    a = pair_semi_major_axis(system, pair)
    mu = pair_gravitational_parameter(system, pair)
    return ((2 * pi) * sqrt((a ** 3) / mu))