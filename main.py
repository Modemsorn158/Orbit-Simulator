from constants import EARTH_MU
from integrators import forward_euler_step, semi_implicit_euler_step
from simulation import simulate
from plotter import plot_trajectory, plot_integrator_comparison, plot_energy_comparison
from diagnostics import specific_energy_history, relative_change_percent
from math import sqrt

if __name__ == "__main__":
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    dt = 10
    r = 7000000
    vc = sqrt(EARTH_MU / r)  # m/s
    states_forward = simulate(r, 0, 0, vc, dt, 600, forward_euler_step)
    positions_forward = [(x, y) for x, y, vx, vy in states_forward]
    plot_trajectory(dt, positions_forward)

    # Figure 2: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using semi-implicit Euler integration.
    states_semi_implicit = simulate(r, 0, 0, vc, dt, 600, semi_implicit_euler_step)
    positions_semi_implicit = [(x, y) for x, y, vx, vy in states_semi_implicit]
    plot_trajectory(dt, positions_semi_implicit)

    # Figure 3: Compare the trajectories of the two integrators.
    plot_integrator_comparison(dt, positions_forward, positions_semi_implicit, "Forward Euler", "Semi-Implicit Euler")
    
    # Figure 4: Compare the relative change in specific orbital energy for the two integrators.
    energy_forward = specific_energy_history(states_forward)
    energy_semi_implicit = specific_energy_history(states_semi_implicit)
    relative_change_forward = relative_change_percent(energy_forward)
    relative_change_semi_implicit = relative_change_percent(energy_semi_implicit)
    plot_energy_comparison(dt, relative_change_forward, relative_change_semi_implicit, "Forward Euler", "Semi-Implicit Euler")