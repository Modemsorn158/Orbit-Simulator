import unittest
from constants import GRAVITATIONAL_CONSTANT
from integrators import system_velocity_verlet_step
from gravity import system_gravitational_accelerations
from simulation import simulate_system
from system_diagnostics import total_linear_momentum, center_of_mass, total_angular_momentum, total_mechanical_energy
from collision import system_check_collision, estimate_system_impact_time
from plotter import plot_system_trajectory
from state import *
from math import sqrt, pi

class TestSystem(unittest.TestCase):
    @staticmethod
    def system_force_acceleration(
        system: SystemState,
        accelerations = list[Vector2]
    ) -> list[Vector2]:
        return accelerations
    
    # Earth-Sun system simulation
    def test_earth_sun_simulation(self):
        r = (1.496 * (10 ** 11))
        earth_mass = (5.972 * (10 ** 24))
        sun_mass = (1.989 * (10 ** 30))
        r1 = r * (earth_mass / (earth_mass + sun_mass))
        r2 = r * (sun_mass / (earth_mass + sun_mass))
        r3 = r1 + r2
        omega = sqrt((GRAVITATIONAL_CONSTANT * (earth_mass + sun_mass)) / (r3 ** 3))
        v_sun = omega * r1
        v_earth = omega * r2
        sun = BodyState(
            body = Body(
                name = "Sun",
                mass = 1.989 * (10 ** 30),
                radius = 6.9585 * (10 ** 8)
            ),
            position = Vector2(
                x = -r1,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = -v_sun
            )
        )
        earth = BodyState(
            body = Body(
                name = "Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = r2,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = v_earth
            )
        )
        system = SystemState(
            body_states = (
                sun, earth
            ),
            time = 0
        )
        half_year = (60 * 60 * 24 * 365) / 2
        dt = 3600
        steps = int(half_year / dt)
        system_states = simulate_system(system, dt, steps, system_velocity_verlet_step, system_gravitational_accelerations, [])
        final_system = system_states[-1]
        sun = final_system.body_states[0]
        earth = final_system.body_states[1]
        linear1 = total_linear_momentum(system)
        linear2 = total_linear_momentum(final_system)
        linear_scale = 0
        for state in final_system.body_states:
            linear_scale = linear_scale + (state.body.mass * state.velocity.magnitude())
        linear_epsilon = ((linear2 - linear1).magnitude() / linear_scale)
        center1 = center_of_mass(system)
        center2 = center_of_mass(final_system)
        angular1 = total_angular_momentum(system)
        angular2 = total_angular_momentum(final_system)
        angular_scale = 0
        for state in final_system.body_states:
            angular_scale = angular_scale + (state.body.mass * ((state.position.x * state.velocity.y) - (state.position.y * state.velocity.x)))
        angular_epsilon = ((angular2 - angular1) / angular_scale)
        energy1 = total_mechanical_energy(system)
        energy2 = total_mechanical_energy(final_system)
        K = 0
        U = 0
        for i in range(len(final_system.body_states)):
            state = final_system.body_states[i]
            K = K + ((1 / 2) * (state.body.mass * (state.velocity.magnitude() ** 2)))
            for j in range(len(final_system.body_states)):
                if i < j:
                    state2 = final_system.body_states[j]
                    U = U + ((GRAVITATIONAL_CONSTANT * state.body.mass * state2.body.mass) / (state.position - state2.position).magnitude())
        U = -U
        E = K + U
        energy_epsilon = ((energy2 - energy1) / E)
        self.assertFalse(sun.position.x == system.body_states[0].position.x)
        self.assertFalse(sun.position.y == system.body_states[0].position.y)
        self.assertTrue(earth.position.x < 0)
        self.assertTrue(len(system_states) == (steps + 1))
        self.assertTrue(final_system.time == (steps * dt))
        self.assertAlmostEqual(linear_epsilon, 0)
        self.assertAlmostEqual(center1.x, center2.x)
        self.assertAlmostEqual(center1.y, center2.y)
        self.assertAlmostEqual(angular_epsilon, 0)
        self.assertAlmostEqual(energy_epsilon, 0)
        
    # 3-body triangular orbit
    def test_equal_three_body(self):
        body = Body(
            name = "Planet",
            mass = (10 ** 10),
            radius = (10 ** 4)
        )
        r = 100000
        s = r * sqrt(3)
        omega = sqrt((GRAVITATIONAL_CONSTANT * body.mass) / (sqrt(3) * (r ** 3)))
        planet1 = BodyState(
            body = body,
            position = Vector2(
                x = r,
                y = 0
            ),
            velocity = omega * Vector2(0, r)
        )
        planet2 = BodyState(
            body = body,
            position = Vector2(
                x = -(r / 2),
                y = (r / 2) * sqrt(3)
            ),
            velocity = omega * Vector2(-((r / 2) * sqrt(3)), -(r / 2))
        )
        planet3 = BodyState(
            body = body,
            position = Vector2(
                x = -(r / 2),
                y = -(r / 2) * sqrt(3)
            ),
            velocity = omega * Vector2(((r / 2) * sqrt(3)), -(r / 2))
        )
        system = SystemState(
            body_states = (
                planet1, planet2, planet3
            ),
            time = 0
        )
        T = (2 * pi) / omega
        steps = 10000
        dt = (T / steps)
        system_states = simulate_system(system, dt, steps, system_velocity_verlet_step, system_gravitational_accelerations, [])
        final_system = system_states[-1]
        planet1_final = final_system.body_states[0]
        planet2_final = final_system.body_states[1]
        planet3_final = final_system.body_states[2]
        linear1 = total_linear_momentum(system)
        linear2 = total_linear_momentum(final_system)
        linear_scale = 0
        for state in final_system.body_states:
            linear_scale = linear_scale + (state.body.mass * state.velocity.magnitude())
        linear_epsilon = ((linear2 - linear1).magnitude() / linear_scale)
        center1 = center_of_mass(system)
        center2 = center_of_mass(final_system)
        angular1 = total_angular_momentum(system)
        angular2 = total_angular_momentum(final_system)
        angular_scale = 0
        for state in final_system.body_states:
            angular_scale = angular_scale + (state.body.mass * ((state.position.x * state.velocity.y) - (state.position.y * state.velocity.x)))
        angular_epsilon = ((angular2 - angular1) / angular_scale)
        energy1 = total_mechanical_energy(system)
        energy2 = total_mechanical_energy(final_system)
        K = 0
        U = 0
        for i in range(len(final_system.body_states)):
            state = final_system.body_states[i]
            K = K + ((1 / 2) * (state.body.mass * (state.velocity.magnitude() ** 2)))
            for j in range(len(final_system.body_states)):
                if i < j:
                    state2 = final_system.body_states[j]
                    U = U + ((GRAVITATIONAL_CONSTANT * state.body.mass * state2.body.mass) / (state.position - state2.position).magnitude())
        U = -U
        E = K + U
        energy_epsilon = ((energy2 - energy1) / E)
        self.assertAlmostEqual(planet1.position.x, planet1_final.position.x, 0)
        self.assertAlmostEqual(planet1.position.y, planet1_final.position.y, 0)
        self.assertAlmostEqual(planet2.position.x, planet2_final.position.x, 0)
        self.assertAlmostEqual(planet2.position.y, planet2_final.position.y, 0)
        self.assertAlmostEqual(planet3.position.x, planet3_final.position.x, 0)
        self.assertAlmostEqual(planet3.position.y, planet3_final.position.y, 0)
        self.assertAlmostEqual((planet1_final.position - planet2_final.position).magnitude(), s)
        self.assertAlmostEqual((planet1_final.position - planet3_final.position).magnitude(), s)
        self.assertAlmostEqual((planet2_final.position - planet3_final.position).magnitude(), s)
        self.assertAlmostEqual(linear_epsilon, 0)
        self.assertAlmostEqual(center1.x, center2.x)
        self.assertAlmostEqual(center1.y, center2.y)
        self.assertAlmostEqual(angular_epsilon, 0)
        self.assertAlmostEqual(energy_epsilon, 0)
        #plot_system_trajectory(dt, system_states, "Triangular 3-Body Orbit Trajectory;")
        
    # Test collision
    def test_collision(self):
        body1 = BodyState(
            body = Body(
                name = "Planet1",
                mass = 10,
                radius = 5
            ),
            position = Vector2(
                x = -10,
                y = 0
            ),
            velocity = Vector2(
                x = 1,
                y = 0
            )
        )
        body2 = BodyState(
            body = Body(
                name = "Planet2",
                mass = 10,
                radius = 5
            ),
            position = Vector2(
                x = 10,
                y = 0
            ),
            velocity = Vector2(
                x = -1,
                y = 0
            )
        )
        body3 = BodyState(
            body = Body(
                name = "Planet3",
                mass = 10,
                radius = 5
            ),
            position = Vector2(
                x = 0,
                y = 15
            ),
            velocity = Vector2(
                x = 0,
                y = 1
            )
        )
        body4 = BodyState(
            body = Body(
                name = "Planet4",
                mass = 10,
                radius = 5
            ),
            position = Vector2(
                x = -10,
                y = -15
            ),
            velocity = Vector2(
                x = 0.5,
                y = 0
            )
        )
        body5 = BodyState(
            body = Body(
                name = "Planet5",
                mass = 10,
                radius = 5
            ),
            position = Vector2(
                x = 10,
                y = -15
            ),
            velocity = Vector2(
                x = -0.5,
                y = 0
            )
        )
        system = SystemState(
            body_states = (
                body1, body2, body3, body4, body5
            ),
            time = 0
        )
        systems = simulate_system(system, 1, 10, system_velocity_verlet_step, self.system_force_acceleration, [[Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0), Vector2(0, 0)]], system_check_collision, estimate_system_impact_time)
        final_system = systems[-1]
        self.assertAlmostEqual(final_system.time, 5)
        self.assertAlmostEqual((final_system.body_states[0].position - final_system.body_states[1].position).magnitude(), (final_system.body_states[0].body.radius + final_system.body_states[1].body.radius))
        self.assertAlmostEqual(final_system.body_states[2].position.y, 20)