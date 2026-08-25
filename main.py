from constants import EARTH_MU
from simulation import simulate
from plotter import plot_trajectory
from math import sqrt

if __name__ == "__main__":
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    r = 7000000
    vc = sqrt(EARTH_MU / r)  # m/s
    positions = simulate(r, 0, 0, vc, 10, 600)
    plot_trajectory(positions)