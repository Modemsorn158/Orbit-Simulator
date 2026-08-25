from constants import EARTH_MU
from simulation import simulate
from diagnostics import specific_energy_history, relative_change_percent
from math import sqrt

def circular_orbit_max_energy_drift(radius, total_time, dt, integration_step):
    """Simulate a circular orbit and return the maximum percentage energy drift over the simulation."""
    
    if (total_time % dt) != 0:
        raise ValueError("Total time must be an integer multiple of dt.")
    vc = sqrt(EARTH_MU / radius)
    states = simulate(radius, 0, 0, vc, dt, (total_time // dt), integration_step)
    energy_history = specific_energy_history(states)
    relative_change = relative_change_percent(energy_history)
    return max(abs(change) for change in relative_change)