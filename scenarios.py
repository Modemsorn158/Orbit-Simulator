from constants import GRAVITATIONAL_CONSTANT
from gravity import gravitational_acceleration, system_gravitational_accelerations
from integrators import forward_euler_step, semi_implicit_euler_step, velocity_verlet_step, system_velocity_verlet_step
from simulation import simulate, simulate_system
from plotter import plot_trajectory, plot_integrator_comparison, plot_diagnostic_comparison, plot_table, plot_system_trajectory
from diagnostics import altitude, eccentricity, semi_major_axis, specific_energy_history, relative_change_percent, specific_angular_momentum_history, orbital_period, apsides, find_apsis_events, escape_velocity
from system_diagnostics import pair_diagnostics_history, pair_semi_major_axis, pair_eccentricity
from validation import circular_orbit_max_energy_drift
from maneuvers import apply_prograde_delta_v, hohmann_transfer
from collision import has_collision_with_body, estimate_body_impact_time
from presets import solar_system
from state import *
from math import sqrt

earth = BodyState(
    body = Body(
        name = "Earth",
        mass = 5.972 * (10 ** 24),
        radius = 6.371 * (10 ** 6)
    ),
    position = Vector2(
        x = 0,
        y = 0
    ),
    velocity = Vector2(
        x = 0,
        y = 0
    )
)
spacecraft_body = Body(
    name = "Spacecraft",
    mass = 0,
    radius = 0
)
earth_mu = GRAVITATIONAL_CONSTANT * earth.body.mass

def _positions_from_states(states):
    """Extract positions from a list of states."""
    
    return [(state.position.x, state.position.y) for state in states]

def run_integrator_validation():
    # Figure 1: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using forward Euler integration.
    dt = 10
    r = 7000000
    vc = sqrt(earth_mu / r)
    body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = vc
        )
    )
    states_forward = simulate(body, dt, 600, forward_euler_step, gravitational_acceleration, [earth])
    positions_forward = _positions_from_states(states_forward)
    plot_trajectory(dt, positions_forward, earth, "Trajectory Plot; Forward Euler Integration")

    # Figure 2: Simulate and plot the trajectory of a satellite in a circular orbit around Earth using semi-implicit Euler integration.
    states_semi_implicit = simulate(body, dt, 600, semi_implicit_euler_step, gravitational_acceleration, [earth])
    positions_semi_implicit = _positions_from_states(states_semi_implicit)
    plot_trajectory(dt, positions_semi_implicit, earth, "Trajectory Plot; Semi-Implicit Euler Integration")

    # Figure 3: Compare the trajectories of the two integrators.
    plot_integrator_comparison(dt, positions_forward, positions_semi_implicit, earth, "Forward Euler", "Semi-Implicit Euler", "Integrator Comparison")

    # Figure 4: Compare the relative change in specific orbital energy for the two integrators.
    energy_forward = specific_energy_history(states_forward, earth)
    energy_semi_implicit = specific_energy_history(states_semi_implicit, earth)
    relative_change_forward = relative_change_percent(energy_forward)
    relative_change_semi_implicit = relative_change_percent(energy_semi_implicit)
    plot_diagnostic_comparison(dt, relative_change_forward, relative_change_semi_implicit, "Forward Euler", "Semi-Implicit Euler", "Relative Change in Specific Orbital Energy", "Relative Change (%)")
    
    # Figure 5: Compare the relative change in specific angular momentum for the two integrators.
    h_forward = specific_angular_momentum_history(states_forward, earth)
    h_semi_implicit = specific_angular_momentum_history(states_semi_implicit, earth)
    relative_change_h_forward = relative_change_percent(h_forward)
    relative_change_h_semi_implicit = relative_change_percent(h_semi_implicit)
    plot_diagnostic_comparison(dt, relative_change_h_forward, relative_change_h_semi_implicit, "Forward Euler", "Semi-Implicit Euler", "Relative Change in Specific Angular Momentum", "Relative Change (%)")
    
    # Figure 6: Compare the maximum percentage energy drift for different time steps using all integrators.
    t = 6000
    dt_list = [1, 10, 30]
    plot_table_data = []
    for dt in dt_list:
        forward_drift = circular_orbit_max_energy_drift(body, earth, dt, t, forward_euler_step)
        semi_implicit_drift = circular_orbit_max_energy_drift(body, earth, dt, t, semi_implicit_euler_step)
        velocity_verlet_drift = circular_orbit_max_energy_drift(body, earth, dt, t, velocity_verlet_step)
        plot_table_data.append([f"dt={dt}", f"{forward_drift:.12f}", f"{semi_implicit_drift:.12f}", f"{velocity_verlet_drift:.12f}"])
    plot_table(["Time Step (s)", "Forward Euler Max Energy Drift (%)", "Semi-Implicit Euler Max Energy Drift (%)", "Velocity Verlet Max Energy Drift (%)"], plot_table_data, "Maximum Percentage Energy Drift for Different Time Steps")
    
def run_orbit_examples():
    # Figure 1: Simulate an eliptical orbit and plot the trajectory using semi-implicit Euler integration.
    r_elliptical = 10000000
    vc_elliptical = sqrt(earth_mu / r_elliptical)
    body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r_elliptical,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = 0.9 * vc_elliptical
        )
    )
    states = simulate(body, 10, 800, semi_implicit_euler_step, gravitational_acceleration, [earth]) 
    positions = _positions_from_states(states)
    plot_trajectory(10, positions, earth, "Trajectory Plot; Elliptical Orbit; Semi-Implicit Euler Integration")
    
    # Figure 2: Test phase accuracy on elliptical orbit using both semi-implicit Euler and velocity Verlet integration methods.
    states_semi_implicit = simulate(body, 10, 800, semi_implicit_euler_step, gravitational_acceleration, [earth])
    states_velocity_verlet = simulate(body, 10, 800, velocity_verlet_step, gravitational_acceleration, [earth])
    apsis_events_semi_implicit = find_apsis_events(states_semi_implicit, earth, 10)
    apsis_events_velocity_verlet = find_apsis_events(states_velocity_verlet, earth, 10)
    T = orbital_period(body, earth)
    plot_table_data = []
    plot_table_data.append(["Analytical", f"{(T / 2):.2f}", f"{T:.2f}"])
    plot_table_data.append(["Semi-Implicit Euler", f"{apsis_events_semi_implicit[0][1]:.2f}", f"{apsis_events_semi_implicit[1][1]:.2f}"])
    plot_table_data.append(["Velocity Verlet", f"{apsis_events_velocity_verlet[0][1]:.2f}", f"{apsis_events_velocity_verlet[1][1]:.2f}"])
    plot_table(["Method", "Periapsis Time (s)", "Apoapsis Time (s)"], plot_table_data, "Apsis Event Times for Elliptical Orbit; Semi-Implicit Euler vs Velocity Verlet")
    
    # Figure 3: Hyperbolic escape trajectory simulation and plot the trajectory using velocity Verlet integration.
    r = 7000000
    ve = escape_velocity(Vector2(r, 0), earth)
    escape_body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = 1.01 * ve
        )
    )
    states_escape = simulate(escape_body, 10, 2000, velocity_verlet_step, gravitational_acceleration, [earth])
    positions_escape = _positions_from_states(states_escape)
    plot_trajectory(10, positions_escape, earth, "Trajectory Plot; Hyperbolic Escape Trajectory; Velocity Verlet Integration")
    
def run_maneuver_examples():
    # Figure 1: Circular orbit with prograde burn applied and plot the trajectory using velocity Verlet integration.
    r = 7000000
    vc = sqrt(earth_mu / r)
    velocity = Vector2(0, vc)
    prograde_velocity = apply_prograde_delta_v(velocity, earth.velocity, 500)
    body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r,
            y = 0
        ),
        velocity = prograde_velocity
    )
    states_burn = simulate(body, 10, 800, velocity_verlet_step, gravitational_acceleration, [earth])
    positions_burn = _positions_from_states(states_burn)
    plot_trajectory(10, positions_burn, earth, "Trajectory Plot; Circular Orbit with Prograde Burn; Velocity Verlet Integration")
    
    # Figure 2, 3: Simulate a Hohmann transfer from a low Earth orbit to a higher orbit and plot the trajectory in multiple parts.
    transfer_dt = 1
    r1 = 7000000
    vc1 = sqrt(earth_mu / r1)
    delta_v1, delta_v2, t_transfer = hohmann_transfer(r1, 10000000, earth)
    transfer_velocity = apply_prograde_delta_v(Vector2(0, vc1), earth.velocity, delta_v1)
    body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r1,
            y = 0
        ),
        velocity = transfer_velocity
    )
    states_transfer1 = simulate(body, transfer_dt, round(t_transfer / transfer_dt), velocity_verlet_step, gravitational_acceleration, [earth])
    positions_transfer1 = _positions_from_states(states_transfer1)
    plot_trajectory(1, positions_transfer1, earth, "Trajectory Plot; Transfer Trajectory with Prograde Burn; Velocity Verlet Integration")
    final_state = states_transfer1[-1]
    final_velocity = apply_prograde_delta_v(final_state.velocity, earth.velocity, delta_v2)
    final_body = BodyState(
        body = spacecraft_body,
        position = final_state.position,
        velocity = final_velocity
    )
    periapsis, apoapsis = apsides(final_body, earth)
    plot_table_data = [["Periapsis", periapsis], ["Apoapsis", apoapsis]]
    plot_table(["Apside", "Value"], plot_table_data, "Periapsis and Apoapsis Post Transfer Burn")
    
def run_collision_example():
    # Figure 1, 2: Simulate sub-orbital collision into Earth's surface and plot the trajectory using velocity Verlet integration
    r = 7000000
    vc = sqrt(earth_mu / r)
    body = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = 0.9 * vc
        )
    )
    states = simulate(body, 1, 10000, velocity_verlet_step, gravitational_acceleration, [earth], has_collision_with_body, estimate_body_impact_time, earth)
    positions = _positions_from_states(states)
    plot_trajectory(1, positions, earth, "Trajectory Plot; Sub-Orbital Collision Into Earth's Surface; Velocity Verlet Integration")
    collision_step_index = (len(states) - 1)
    position = positions[-1]
    alt = altitude(Vector2(position[0], position[1]), earth)
    plot_table_data = [["Collision step index", collision_step_index], ["Altitude", alt]]
    plot_table(["Key", "Value"], plot_table_data, "Sub-Orbital Collision Data")
    
def run_nbody_example():
    # Figure 1, 1.1: Sun-Earth-Moon orbit system
    au = 1.496 * (10 ** 11)
    m_sun = 1.989 * (10 ** 30)
    r_sun = 6.9585 * (10 ** 8)
    m_earth = 5.972 * (10 ** 24)
    r_earth = 6.371 * (10 ** 6)
    m_moon = 7.34767309 * (10 ** 22)
    r_moon = 1.7374 * (10 ** 6)
    d_earth_moon = (3.84 * (10 ** 8))
    d_earth = d_earth_moon * (m_moon / (m_earth + m_moon))
    d_moon = d_earth_moon * (m_earth / (m_earth + m_moon))
    omega_earth_moon = sqrt((GRAVITATIONAL_CONSTANT * (m_earth + m_moon)) / (d_earth_moon ** 3))
    m_earth_moon = m_earth + m_moon
    d_sun = au * (m_earth_moon / (m_sun + m_earth_moon))
    d_barycenter = au * (m_sun / (m_sun + m_earth_moon))
    omega_year = sqrt((GRAVITATIONAL_CONSTANT * (m_sun + m_earth_moon)) / (au ** 3))
    sun = BodyState(
        body = Body(
            name = "Sun",
            mass = m_sun,
            radius = r_sun
        ),
        position = Vector2(
            x = -d_sun,
            y = 0
        ),
        velocity = (omega_year * Vector2(0, -d_sun)
        )
    )
    earth = BodyState(
        body = Body(
            name = "Earth",
            mass = m_earth,
            radius = r_earth
        ),
        position = Vector2(
            x = (d_barycenter - d_earth),
            y = 0
        ),
        velocity = (omega_year * Vector2(0, d_barycenter)) - (omega_earth_moon * Vector2(0, d_earth)
        )
    )
    moon = BodyState(
        body = Body(
            name = "Moon",
            mass = m_moon,
            radius = r_moon
        ),
        position = Vector2(
            x = (d_barycenter + d_moon),
            y = 0
        ),
        velocity = ((omega_year * Vector2(0, d_barycenter)) + (omega_earth_moon * Vector2(0, d_moon)))
    )
    system = SystemState(
        body_states = (
            sun, earth, moon
        ),
        time = 0
    )
    total_time = 365 * 24 * 60 * 60
    steps = 10000
    dt = total_time / steps
    system_states = simulate_system(system, dt, steps, system_velocity_verlet_step, system_gravitational_accelerations, [])
    plot_system_trajectory(dt, system_states, "Earth-Sun-Moon System Trajectory", 5)
    
    # Figure 2, 2.1, 2.2: Solar system
    system = solar_system
    total_time = 165 * 365 * 24 * 60 * 60
    steps = 100000
    dt = total_time / steps
    system_states = simulate_system(solar_system, dt, steps, system_velocity_verlet_step, system_gravitational_accelerations, [], None, None, True)
    plot_system_trajectory(dt, system_states, "Solar System Trajectory", 5)
    
    # Figure 3, 3.1, 3.2: Earth reference, Moon-Sun only
    plot_system_trajectory(dt, system_states, "Solar System Trajectory; Earth Reference Point; Earth-Moon-Sun", 5, 3, [0, 3, 4])
    
    # Figure 4, 5: Earth-Moon semi-major axis and eccentricity history
    pair = (3, 4)
    history_a = pair_diagnostics_history(system_states, pair, pair_semi_major_axis)
    static_a = [pair_semi_major_axis(solar_system, pair)] * len(history_a)
    history_e = pair_diagnostics_history(system_states, pair, pair_eccentricity)
    static_e = [pair_eccentricity(solar_system, pair)] * len(history_e)
    plot_diagnostic_comparison(dt, history_a, static_a, "N-body semi-major-axis", "2-body semi-major axis", "Semi-Major Axis Comparison; N-Body vs 2-Body", "a")
    plot_diagnostic_comparison(dt, history_e, static_e, "N-body eccentricity", "2-body eccentricity", "Eccentricity Comparison; N-Body vs 2-Body", "e")