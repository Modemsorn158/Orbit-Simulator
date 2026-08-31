import unittest
from gravity import gravitational_acceleration, system_gravitational_accelerations
from state import *

class TestGravity(unittest.TestCase):
    # Multi-body gravitational acceleration
    def test_two_body(self):
        sun = BodyState(
            body = Body(
                name = "Sun",
                mass = 1.989 * (10 ** 30),
                radius = 6.9585 * (10 ** 8)
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
        earth = BodyState(
            body = Body(
                name = "Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = 1.496 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        system = SystemState(
            body_states = (
                sun, earth
            ),
            time = 0
        )
        a = system_gravitational_accelerations(system)
        self.assertAlmostEqual(a[0].x, 1.7809935049615373 * (10 ** -8))
        self.assertAlmostEqual(a[1].x, -0.005931674617160914)
        
    def test_equal_body(self):
        earth_negative = BodyState(
            body = Body(
                name = "Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = -(10 ** 10),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        earth_positive = BodyState(
            body = Body(
                name = "Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = (10 ** 10),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        system = SystemState(
            body_states = (
                earth_negative, earth_positive
            ),
            time = 0
        )
        a = system_gravitational_accelerations(system)
        self.assertAlmostEqual(a[0].x, -a[1].x)
        
    def test_massless_spacecraft(self):
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
        spacecraft = BodyState(
            body = Body(
                name = "Spacecraft",
                mass = 0,
                radius = 0
            ),
            position = Vector2(
                x = (10 ** 7),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        system = SystemState(
            body_states = (
                earth, spacecraft
            )
        )
        a = system_gravitational_accelerations(system)
        self.assertAlmostEqual(a[0].x, 0)
        self.assertAlmostEqual(a[1].x, gravitational_acceleration(spacecraft.position, earth).x)
        
    def test_three_body(self):
        sun = BodyState(
            body = Body(
                name = "Sun",
                mass = 1.989 * (10 ** 30),
                radius = 6.9585 * (10 ** 8)
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
        earth = BodyState(
            body = Body(
                name = "Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = 1.496 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        moon = BodyState(
            body = Body(
                name = "Moon",
                mass = 7.34767309 * (10 ** 22),
                radius = 1.7374 * (10 ** 6)
            ),
            position = Vector2(
                x = earth.position.x,
                y = 3.844 * (10 ** 8)
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        system = SystemState(
            body_states = (
                sun, earth, moon
            ),
            time = 0
        )
        a = system_gravitational_accelerations(system)
        a_earth = a[1]
        a_earth_sun = gravitational_acceleration(earth.position, sun)
        a_earth_moon = gravitational_acceleration(earth.position, moon)
        self.assertAlmostEqual(a_earth.x, (a_earth_sun + a_earth_moon).x)
        self.assertAlmostEqual(a_earth.y, (a_earth_sun + a_earth_moon).y)