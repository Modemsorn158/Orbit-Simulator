import unittest
from maneuvers import apply_delta_v, apply_prograde_delta_v, hohmann_transfer
from state import *

class TestManeuvers(unittest.TestCase):
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
    
    # Delta v
    def test_apply_delta_v(self):
        velocity1 = Vector2(0, 7500)
        delta_velocity1 = Vector2(0, 100)
        velocity2 = Vector2(100, -50)
        delta_velocity2 = Vector2(-20, 70)
        new_velocity1 = apply_delta_v(velocity1, delta_velocity1)
        expected_new_velocity1 = Vector2(0, 7600)
        new_velocity2 = apply_delta_v(velocity2, delta_velocity2)
        expected_new_velocity2 = Vector2(80, 20)
        self.assertTrue(new_velocity1 == expected_new_velocity1)
        self.assertTrue(new_velocity2 == expected_new_velocity2)
        
    # Prograde delta v
    def test_apply_prograde_delta_v(self):
        source_velocity = Vector2(0, 0)
        velocity1, delta_v1 = Vector2(0, 7500), 100
        new_velocity1 = apply_prograde_delta_v(velocity1, source_velocity, delta_v1)
        expected_new_velocity1 = Vector2(0, 7600)
        velocity2, delta_v2 = Vector2(3, 4), 5
        new_velocity2 = apply_prograde_delta_v(velocity2, source_velocity, delta_v2)
        expected_new_velocity2 = Vector2(6, 8)
        velocity3, delta_v3 = Vector2(0, 0), 0
        self.assertTrue(new_velocity1 == expected_new_velocity1)
        self.assertTrue(new_velocity2 == expected_new_velocity2)
        with self.assertRaises(ValueError):
            apply_prograde_delta_v(velocity3, source_velocity, delta_v3)
            
    # Hohmann transfer
    def test_hohmann_transfer(self):
        r1, r2 = 7000000, 10000000
        delta_v1, delta_v2, t = hohmann_transfer(r1, r2, self.earth)
        expected_delta_v1 = 638.782
        expected_delta_v2 = 584.082
        expected_t = 3899.559
        self.assertAlmostEqual(delta_v1, expected_delta_v1, delta=1e-3)
        self.assertAlmostEqual(delta_v2, expected_delta_v2, delta=1e-3)
        self.assertAlmostEqual(t, expected_t, delta=1e-3)