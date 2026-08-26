from constants import EARTH_MU
from integrators import forward_euler_step, semi_implicit_euler_step, velocity_verlet_step
from simulation import simulate
from plotter import plot_trajectory, plot_integrator_comparison, plot_diagnostic_comparison, plot_table
from diagnostics import altitude, specific_energy_history, relative_change_percent, specific_angular_momentum_history, orbital_period, apsides, find_apsis_events, escape_velocity
from validation import circular_orbit_max_energy_drift
from maneuvers import apply_prograde_delta_v, hohmann_transfer
from collision import has_collision_with_earth, estimate_earth_impact_time
from math import sqrt

def _positions_from_states(states):
    """Extract positions (x, y) from a list of states."""
    
    return [(x, y) for x, y, vx, vy in states]

def run_integrator_validation():
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    dt = 10
    r = 7000000
    vc = sqrt(EARTH_MU / r)  # m/s
    states_forward = simulate(r, 0, 0, vc, dt, 600, forward_euler_step)
    positions_forward = _positions_from_states(states_forward)
    plot_trajectory(dt, positions_forward, "Trajectory Plot; Forward Euler Integration")

    # Figure 2: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using semi-implicit Euler integration.
    states_semi_implicit = simulate(r, 0, 0, vc, dt, 600, semi_implicit_euler_step)
    positions_semi_implicit = _positions_from_states(states_semi_implicit)
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
    
def run_orbit_examples():
    # Figure 1: Simulate an eliptical orbit and plot the trajectory using semi-implicit Euler integration.
    r_elliptical = 10000000
    vc_elliptical = sqrt(EARTH_MU / r_elliptical)
    states = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, semi_implicit_euler_step) 
    positions = _positions_from_states(states)
    plot_trajectory(10, positions, "Trajectory Plot; Elliptical Orbit; Semi-Implicit Euler Integration")
    
    # Figure 2: Test phase accuracy on elliptical orbit using both semi-implicit Euler and velocity Verlet integration methods.
    states_semi_implicit = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, semi_implicit_euler_step)
    states_velocity_verlet = simulate(r_elliptical, 0, 0, (0.9 * vc_elliptical), 10, 800, velocity_verlet_step)
    apsis_events_semi_implicit = find_apsis_events(states_semi_implicit, 10)
    apsis_events_velocity_verlet = find_apsis_events(states_velocity_verlet, 10)
    T = orbital_period(r_elliptical, 0, 0, (0.9 * vc_elliptical))
    plot_table_data = []
    plot_table_data.append(["Analytical", f"{(T / 2):.2f}", f"{T:.2f}"])
    plot_table_data.append(["Semi-Implicit Euler", f"{apsis_events_semi_implicit[0][1]:.2f}", f"{apsis_events_semi_implicit[1][1]:.2f}"])
    plot_table_data.append(["Velocity Verlet", f"{apsis_events_velocity_verlet[0][1]:.2f}", f"{apsis_events_velocity_verlet[1][1]:.2f}"])
    plot_table(["Method", "Periapsis Time (s)", "Apoapsis Time (s)"], plot_table_data, "Apsis Event Times for Elliptical Orbit; Semi-Implicit Euler vs Velocity Verlet")
    
    # Figure 3: Hyperbolic escape trajectory simulation and plot the trajectory using velocity Verlet integration.
    r = 7000000
    ve = escape_velocity(r, 0)
    states_escape = simulate(r, 0, 0, (1.01 * ve), 10, 2000, velocity_verlet_step)
    positions_escape = _positions_from_states(states_escape)
    plot_trajectory(10, positions_escape, "Trajectory Plot; Hyperbolic Escape Trajectory; Velocity Verlet Integration")
    
def run_maneuver_examples():
    # Figure 1: Circular orbit with prograde burn applied and plot the trajectory using velocity Verlet integration.
    r = 7000000
    vc = sqrt(EARTH_MU / r)
    vx, vy = apply_prograde_delta_v(0, vc, 500)
    states_burn = simulate(r, 0, vx, vy, 10, 800, velocity_verlet_step)
    positions_burn = _positions_from_states(states_burn)
    plot_trajectory(10, positions_burn, "Trajectory Plot; Circular Orbit with Prograde Burn; Velocity Verlet Integration")
    
    # Figure 2, 3: Simulate a Hohmann transfer from a low Earth orbit to a higher orbit and plot the trajectory in multiple parts.
    transfer_dt = 1
    r1 = 7000000
    vc1 = sqrt(EARTH_MU / r1)
    delta_v1, delta_v2, t_transfer = hohmann_transfer(r1, 10000000)
    transfer_vx, transfer_vy = apply_prograde_delta_v(0, vc1, delta_v1)
    states_transfer1 = simulate(r1, 0, transfer_vx, transfer_vy, transfer_dt, round(t_transfer / transfer_dt), velocity_verlet_step)
    positions_transfer1 = _positions_from_states(states_transfer1)
    plot_trajectory(1, positions_transfer1, "Trajectory Plot; Transfer Trajectory with Prograde Burn; Velocity Verlet Integration")
    x2, y2, vx2, vy2 = states_transfer1[-1]
    transfer_vx2, transfer_vy2 = apply_prograde_delta_v(vx2, vy2, delta_v2)
    periapsis, apoapsis = apsides(x2, y2, transfer_vx2, transfer_vy2)
    plot_table_data = [["Periapsis", periapsis], ["Apoapsis", apoapsis]]
    plot_table(["Apside", "Value"], plot_table_data, "Periapsis and Apoapsis Post Transfer Burn")
    
def run_collision_example():
    # Figure 1, 2: Simulate sub-orbital collision into Earth's surface and plot the trajectory using velocity Verlet integration
    r = 7000000
    vc = sqrt(EARTH_MU / r)
    states = simulate(r, 0, 0, (0.9 * vc), 1, 10000, velocity_verlet_step, has_collision_with_earth, estimate_earth_impact_time)
    positions = _positions_from_states(states)
    plot_trajectory(1, positions, "Trajectory Plot; Sub-Orbital Collision Into Earth's Surface; Velocity Verlet Integration")
    collision_step_index = (len(states) - 1)
    x, y = positions[-1]
    alt = altitude(x, y)
    plot_table_data = [["Collision step index", collision_step_index], ["Altitude", alt]]
    plot_table(["Key", "Value"], plot_table_data, "Sub-Orbital Collision Data")