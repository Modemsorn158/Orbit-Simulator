from typing import final
import unittest
from constants import GRAVITATIONAL_CONSTANT
from integrators import system_velocity_verlet_step
from gravity import system_gravitational_accelerations
from simulation import simulate_system
from system_diagnostics import total_linear_momentum, center_of_mass, total_angular_momentum, total_mechanical_energy
from state import *
from math import sqrt

class TestSystem(unittest.TestCase):
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