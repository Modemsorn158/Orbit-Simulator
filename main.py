from constants import EARTH_MU
from integrators import forward_euler_step, semi_implicit_euler_step, velocity_verlet_step
from simulation import simulate
from plotter import plot_trajectory, plot_integrator_comparison, plot_diagnostic_comparison, plot_table
from diagnostics import specific_energy_history, relative_change_percent, specific_angular_momentum_history, orbital_period, find_apsis_events
from validation import circular_orbit_max_energy_drift
from math import sqrt

if __name__ == "__main__":
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    dt = 10
    r = 7000000
    vc = sqrt(EARTH_MU / r)  # m/s
    states_forward = simulate(r, 0, 0, vc, dt, 600, forward_euler_step)
    positions_forward = [(x, y) for x, y, vx, vy in states_forward]
    plot_trajectory(dt, positions_forward, "Trajectory Plot; Forward Euler Integration")

    # Figure 2: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using semi-implicit Euler integration.
    states_semi_implicit = simulate(r, 0, 0, vc, dt, 600, semi_implicit_euler_step)
    positions_semi_implicit = [(x, y) for x, y, vx, vy in states_semi_implicit]
    plot_trajectory(dt, positions_semi_implicit, "Trajectory Plot; Semi-Implicit Euler Integration")

    # Figure 3: Compare the trajectories of the two integrators.
    plot_integrator_comparison(dt, positions_forward, positions_semi_implicit, "Forward Euler", "Semi-Implicit Euler", "Integrator Comparison")

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
    
    # Figure 6: Compare the maximum percentage energy drift for different time steps using all integrators.
    t = 6000
    dt_list = [1, 10, 30]
    plot_table_data = []
    for dt in dt_list:
        forward_drift = circular_orbit_max_energy_drift(r, t, dt, forward_euler_step)
        semi_implicit_drift = circular_orbit_max_energy_drift(r, t, dt, semi_implicit_euler_step)
        velocity_verlet_drift = circular_orbit_max_energy_drift(r, t, dt, velocity_verlet_step)
        plot_table_data.append([f"dt={dt}", f"{forward_drift:.12f}", f"{semi_implicit_drift:.12f}", f"{velocity_verlet_drift:.12f}"])
    plot_table(["Time Step (s)", "Forward Euler Max Energy Drift (%)", "Semi-Implicit Euler Max Energy Drift (%)", "Velocity Verlet Max Energy Drift (%)"], plot_table_data, "Maximum Percentage Energy Drift for Different Time Steps")
    
    # Figure 7: Simulate an eliptical orbit and plot the trajectory using semi-implicit Euler integration.
    r_elliptical = 10000000
    vc_elliptical = sqrt(EARTH_MU / r_elliptical)
    states = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, semi_implicit_euler_step) 
    positions = [(x, y) for x, y, vx, vy in states]
    plot_trajectory(10, positions, "Trajectory Plot; Elliptical Orbit; Semi-Implicit Euler Integration")
    
    # Figure 8: Test phase accuracy on elliptical orbit using both semi-implicit Euler and velocity Verlet integration methods.
    states_semi_implicit = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, semi_implicit_euler_step)
    states_velocity_verlet = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, velocity_verlet_step)
    apsis_events_semi_implicit = find_apsis_events(states_semi_implicit, 10)
    apsis_events_velocity_verlet = find_apsis_events(states_velocity_verlet, 10)
    T = orbital_period(r_elliptical, 0, (0.9 * vc_elliptical), 0)
    plot_table_data = []
    plot_table_data.append(["Analytical", f"{(T / 2):.2f}", f"{T:.2f}"])
    plot_table_data.append(["Semi-Implicit Euler", f"{apsis_events_semi_implicit[0][1]:.2f}", f"{apsis_events_semi_implicit[1][1]:.2f}"])
    plot_table_data.append(["Velocity Verlet", f"{apsis_events_velocity_verlet[0][1]:.2f}", f"{apsis_events_velocity_verlet[1][1]:.2f}"])
    plot_table(["Method", "Periapsis Time (s)", "Apoapsis Time (s)"], plot_table_data, "Apsis Event Times for Elliptical Orbit; Semi-Implicit Euler vs Velocity Verlet")