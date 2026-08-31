import unittest
from integrators import system_forward_euler_step, system_semi_implicit_euler_step, system_velocity_verlet_step
from state import *

class TestIntegrators(unittest.TestCase):
    @staticmethod
    def system_force_acceleration(
        system: SystemState,
        accelerations = list[Vector2]
    ) -> list[Vector2]:
        return accelerations
    
    # System integrators test
    def test_system_integrators(self):
        body = BodyState(
            body = Body(
                name = "Planet",
                mass = (10 ** 20),
                radius = (10 ** 6)
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
        system = SystemState(
            body_states = tuple([body]),
            time = 0
        )
        dt = 1
        acceleration = [Vector2((10 ** 4), (10 ** 2))]
        forward_system = system_forward_euler_step(system, dt, self.system_force_acceleration, [acceleration])
        forward_velocity = forward_system.body_states[0].velocity
        forward_position = forward_system.body_states[0].position
        semi_implicit_system = system_semi_implicit_euler_step(system, dt, self.system_force_acceleration, [acceleration])
        semi_implicit_velocity = semi_implicit_system.body_states[0].velocity
        semi_implicit_position = semi_implicit_system.body_states[0].position
        velocity_verlet_system = system_velocity_verlet_step(system, dt, self.system_force_acceleration, [acceleration])
        velocity_verlet_velocity = velocity_verlet_system.body_states[0].velocity
        velocity_verlet_position = velocity_verlet_system.body_states[0].position
        expected_velocity = Vector2(
            x = (10 ** 4),
            y = (10 ** 2)
        )
        self.assertAlmostEqual(forward_velocity.x, expected_velocity.x)
        self.assertAlmostEqual(forward_velocity.y, expected_velocity.y)
        self.assertAlmostEqual(forward_position.x, 0)
        self.assertAlmostEqual(forward_position.y, 0)
        self.assertAlmostEqual(forward_system.time, 1)
        self.assertTrue(forward_system.body_states[0].body.name == body.body.name)
        self.assertTrue(forward_system.body_states[0].body.mass == body.body.mass)
        self.assertTrue(forward_system.body_states[0].body.radius == body.body.radius)
        self.assertAlmostEqual(semi_implicit_velocity.x, expected_velocity.x)
        self.assertAlmostEqual(semi_implicit_velocity.y, expected_velocity.y)
        self.assertAlmostEqual(semi_implicit_position.x, 10000)
        self.assertAlmostEqual(semi_implicit_position.y, 100)
        self.assertAlmostEqual(semi_implicit_system.time, 1)
        self.assertTrue(semi_implicit_system.body_states[0].body.name == body.body.name)
        self.assertTrue(semi_implicit_system.body_states[0].body.mass == body.body.mass)
        self.assertTrue(semi_implicit_system.body_states[0].body.radius == body.body.radius)
        self.assertAlmostEqual(velocity_verlet_velocity.x, expected_velocity.x)
        self.assertAlmostEqual(velocity_verlet_velocity.y, expected_velocity.y)
        self.assertAlmostEqual(velocity_verlet_position.x, 5000)
        self.assertAlmostEqual(velocity_verlet_position.y, 50)
        self.assertAlmostEqual(velocity_verlet_system.time, 1)
        self.assertTrue(velocity_verlet_system.body_states[0].body.name == body.body.name)
        self.assertTrue(velocity_verlet_system.body_states[0].body.mass == body.body.mass)
        self.assertTrue(velocity_verlet_system.body_states[0].body.radius == body.body.radius)