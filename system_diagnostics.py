from constants import GRAVITATIONAL_CONSTANT
from state import *

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