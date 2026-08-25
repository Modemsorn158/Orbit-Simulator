from constants import EARTH_MU
from integrators import forward_euler_step, semi_implicit_euler_step
from simulation import simulate
from plotter import plot_trajectory, plot_integrator_comparison, plot_diagnostic_comparison, plot_table
from diagnostics import specific_energy_history, relative_change_percent, specific_angular_momentum_history
from validation import circular_orbit_max_energy_drift
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
    plot_diagnostic_comparison(dt, relative_change_forward, relative_change_semi_implicit, "Forward Euler", "Semi-Implicit Euler", "Relative Change in Specific Orbital Energy", "Relative Change (%)")
    
    # Figure 5: Compare the relative change in specific angular momentum for the two integrators.
    h_forward = specific_angular_momentum_history(states_forward)
    h_semi_implicit = specific_angular_momentum_history(states_semi_implicit)
    relative_change_h_forward = relative_change_percent(h_forward)
    relative_change_h_semi_implicit = relative_change_percent(h_semi_implicit)
    plot_diagnostic_comparison(dt, relative_change_h_forward, relative_change_h_semi_implicit, "Forward Euler", "Semi-Implicit Euler", "Relative Change in Specific Angular Momentum", "Relative Change (%)")
    
    # Figure 6: Compare the maximum percentage energy drift for different time steps using both integrators.
    t = 6000
    dt_list = [1, 10, 30]
    plot_table_data = []
    for dt in dt_list:
        d1 = circular_orbit_max_energy_drift(r, t, dt, forward_euler_step)
        d2 = circular_orbit_max_energy_drift(r, t, dt, semi_implicit_euler_step)
        plot_table_data.append([f"dt={dt}", f"{d1:.6f}", f"{d2:.6f}"])
    plot_table(["Time Step (s)", "Forward Euler Max Energy Drift (%)", "Semi-Implicit Euler Max Energy Drift (%)"], plot_table_data, "Maximum Percentage Energy Drift for Different Time Steps")