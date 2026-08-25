from constants import EARTH_MU
from integrators import forward_euler_step, semi_implicit_euler_step
from simulation import simulate
from plotter import plot_trajectory, plot_integrator_comparison
from math import sqrt

if __name__ == "__main__":
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    r = 7000000
    vc = sqrt(EARTH_MU / r)  # m/s
    positions_forward = simulate(r, 0, 0, vc, 10, 600, forward_euler_step)
    plot_trajectory(positions_forward)

    # Figure 2: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using semi-implicit Euler integration.
    positions_semi_implicit = simulate(r, 0, 0, vc, 10, 600, semi_implicit_euler_step)
    plot_trajectory(positions_semi_implicit)

    # Figure 3: Compare the trajectories of the two integrators.
    plot_integrator_comparison(positions1=positions_forward, positions2=positions_semi_implicit, label1="Forward Euler", label2="Semi-Implicit Euler")