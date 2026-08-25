from constants import EARTH_MU
from math import sqrt

def specific_orbital_energy(x, y, vx, vy):
    """Calculate the specific orbital energy of an object in orbit."""
    
    r = sqrt((x ** 2) + (y ** 2))
    v2 = (vx ** 2) + (vy ** 2)
    energy = (v2 / 2) - (EARTH_MU / r)
    return energy

def specific_energy_history(states):
    """Calculate the specific orbital energy for a list of states."""
    
    energy_history = []
    for x, y, vx, vy in states:
        energy = specific_orbital_energy(x, y, vx, vy)
        energy_history.append(energy)
    return energy_history

def relative_change_percent(values):
    """Calculate the relative change percentage of a list of values compared to the initial value."""
    
    if values[0] == 0:
        raise ValueError("Initial value is zero; relative change percentage is undefined.")
    initial_value = values[0]
    reference_size = abs(initial_value)
    return [(value - initial_value) / reference_size * 100 for value in values]

def specific_angular_momentum(x, y, vx, vy):
    """Calculate the specific angular momentum of an object in orbit."""
    
    h = (x * vy) - (y * vx)
    return h

def specific_angular_momentum_history(states):
    """Calculate the specific angular momentum for a list of states."""
    
    h_history = []
    for x, y, vx, vy in states:
        h = specific_angular_momentum(x, y, vx, vy)
        h_history.append(h)
    return h_history

def semi_major_axis(x, y, vx, vy):
    """Calculate the semi-major axis of an orbit given position and velocity."""
    
    energy = specific_orbital_energy(x, y, vx, vy)
    if energy >= 0:
        raise ValueError("Orbit is not bound; semi-major axis is undefined.")
    a = -(EARTH_MU / (2 * energy))
    return a

def eccentricity(x, y, vx, vy):
    """Calculate the eccentricity of an orbit given position and velocity."""
    
    energy = specific_orbital_energy(x, y, vx, vy)
    h = specific_angular_momentum(x, y, vx, vy)
    e0 = 1 + ((2 * energy * (h ** 2)) / (EARTH_MU ** 2))
    e0 = max(e0, 0)
    e = sqrt(e0)
    return e

def apsides(x, y, vx, vy):
    """Calculate the periapsis and apoapsis distances of an orbit given position and velocity."""
    
    a = semi_major_axis(x, y, vx, vy)
    e = eccentricity(x, y, vx, vy)
    r_periapsis = a * (1 - e)
    r_apoapsis = a * (1 + e)
    return r_periapsis, r_apoapsis