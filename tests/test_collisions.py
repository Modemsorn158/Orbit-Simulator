import unittest
from diagnostics import altitude
from gravity import gravitational_acceleration
from simulation import simulate
from constants import GRAVITATIONAL_CONSTANT
from collision import has_collision_with_body, estimate_body_impact_time
from integrators import velocity_verlet_step
from state import *
from math import sqrt

class TestCollisions(unittest.TestCase):
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
    
    # Earth collisions
    def test_earth_collision(self):
        position1 = Vector2(self.earth.body.radius, 0)
        position2 = Vector2(self.earth.body.radius + 1, 0)
        position3 = Vector2(0, 0)
        c1 = has_collision_with_body(
            BodyState(
                body = self.spacecraft_body,
                position = position1,
                velocity = Vector2(
                    x = 0, 
                    y = 0
                )
            ),
            self.earth
        )
        c2 = has_collision_with_body(
            BodyState(
                body = self.spacecraft_body,
                position = position2,
                velocity = Vector2(
                    x = 0, 
                    y = 0
                )
            ), 
            self.earth
        )
        c3 = has_collision_with_body(
            BodyState(
                body = self.spacecraft_body,
                position = position3,
                velocity = Vector2(
                    x = 0, 
                    y = 0
                )
            ),
            self.earth
        )
        self.assertTrue(c1)
        self.assertFalse(c2)
        self.assertTrue(c3)
        
    # Simulation test
    def test_collision_simulation(self):
        position1 = Vector2(self.earth.body.radius, 0)
        position2 = Vector2(7000000, 0)
        vc1 = sqrt(self.earth_mu / position1.x)
        vc2 = sqrt(self.earth_mu / position2.x)
        states1 = simulate(
            BodyState(
                body = self.spacecraft_body,
                position = position1,
                velocity = Vector2(
                    x = 0,
                    y = vc1
                )
            ),
            10,
            500,
            velocity_verlet_step,
            gravitational_acceleration,
            [self.earth],
            has_collision_with_body,
            estimate_body_impact_time,
            self.earth
        )
        states2 = simulate(
            BodyState(
                body = self.spacecraft_body,
                position = position2,
                velocity = Vector2(
                    x = 0,
                    y = vc2
                )
            ),
            10,
            500,
            velocity_verlet_step,
            gravitational_acceleration,
            [self.earth],
            has_collision_with_body,
            estimate_body_impact_time,
            self.earth
        )
        self.assertEqual(len(states1), 1)
        self.assertEqual(len(states2), 501)
        
    # Collision altitude estimation test
    def test_collision_altitude(self):
        state1 = BodyState(
            body = self.spacecraft_body,
            position = Vector2(
                x = 1000 + self.earth.body.radius,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        state2 = BodyState(
            body = self.spacecraft_body,
            position = Vector2(
                x = -1000 + self.earth.body.radius,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        t = estimate_body_impact_time(state1, state2, self.earth, 2)
        self.assertEqual(t, 1)
        state = BodyState(
            body = self.spacecraft_body,
            position = Vector2(
                x = self.earth.body.radius + 1,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        with self.assertRaises(ValueError):
            estimate_body_impact_time(state, state, self.earth, 1)
            
    # Impact test
    def test_impact(self):
        r = 7000000
        vc = sqrt(self.earth_mu / r)
        initial_state = BodyState(
            body = self.spacecraft_body,
            position = Vector2(
                x = r,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0.9 * vc
            )
        )
        states1 = simulate(
            initial_state,
            1,
            10000,
            velocity_verlet_step,
            gravitational_acceleration,
            [self.earth],
            has_collision_with_body,
            estimate_body_impact_time,
            self.earth
        )
        alt1 = altitude(states1[-1].position, self.earth)
        states2 = simulate(
            initial_state,
            1,
            10000,
            velocity_verlet_step,
            gravitational_acceleration,
            [self.earth],
            has_collision_with_body,
            None,
            self.earth
        )
        alt2 = altitude(states2[-1].position, self.earth)
        self.assertLess(abs(alt1), 1)
        self.assertLess(alt2, 0)