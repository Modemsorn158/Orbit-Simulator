import unittest
from constants import GRAVITATIONAL_CONSTANT
from diagnostics import specific_orbital_energy, specific_angular_momentum, semi_major_axis, eccentricity, apsides, orbital_period, radial_velocity, escape_velocity
from state import *
from math import sqrt

class TestDiagnostics(unittest.TestCase):
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
    
    # Circular
    circular_r = 7000000
    circular_vc = sqrt(earth_mu / circular_r)
    circular_state = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = circular_r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = circular_vc
        )
    )
    def test_circular_specific_energy(self):
        energy = specific_orbital_energy(self.circular_state, self.earth)
        expected_energy = -(self.earth_mu / (2 * self.circular_r))
        self.assertAlmostEqual(energy, expected_energy, delta=1e-6)
    def test_circular_eccentricity(self):
        e = eccentricity(self.circular_state, self.earth)
        self.assertAlmostEqual(e, 0.0, delta=1e-12)
        
    # Ellipse
    ellipse_r = 10000000
    ellipse_vc = 0.9 * sqrt(earth_mu / ellipse_r)
    ellipse_state = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = ellipse_r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = ellipse_vc
        )
    )
    def test_elliptical_eccentricity(self):
        e = eccentricity(self.ellipse_state, self.earth)
        expected_e = 0.19
        self.assertAlmostEqual(e, expected_e, delta=1e-6)
    def test_elliptical_apsides(self):
        periapsis, apoapsis = apsides(self.ellipse_state, self.earth)
        expected_periapsis = 6806723
        expected_apoapsis = 10000000
        self.assertAlmostEqual(periapsis, expected_periapsis, delta=1)
        self.assertAlmostEqual(apoapsis, expected_apoapsis, delta=1)
    
    # Invalid input
    escape_r = 7000000
    escape_ve = sqrt((2 * earth_mu) / escape_r)
    escape_state = BodyState(
        body = spacecraft_body,
        position = Vector2(
            x = escape_r,
            y = 0
        ),
        velocity = Vector2(
            x = 0,
            y = escape_ve
        )
    )
    def test_escape_orbit_has_no_bound_semi_major_axis(self):
        with self.assertRaises(ValueError):
            semi_major_axis(self.escape_state, self.earth)
            
    # Escape velocity
    def test_escape_velocity(self):
        position1 = Vector2(self.earth.body.radius, 0)
        position2 = Vector2(7000000, 0)
        position3 = Vector2(0, 0)
        ve1 = escape_velocity(position1, self.earth)
        ve2 = escape_velocity(position2, self.earth)
        expected_ve1 = 11185.98
        expected_ve2 = 10671.58
        self.assertAlmostEqual(ve1, expected_ve1, delta=0.01)
        self.assertAlmostEqual(ve2, expected_ve2, delta=0.01)
        with self.assertRaises(ValueError):
            escape_velocity(position3, self.earth)
            
    # Reference body
    def test_reference_body(self):
        far_earth = BodyState(
            body = Body(
                name = "Far Earth",
                mass = 5.972 * (10 ** 24),
                radius = 6.371 * (10 ** 6)
            ),
            position = Vector2(
                x = 10000000,
                y = 500000
            ),
            velocity = Vector2(
                x = 0,
                y = 0
            )
        )
        r = 7000000
        vc = sqrt(self.earth_mu / r)
        spacecraft = BodyState(
            body = Body(
                name = "Spacecraft",
                mass = 0,
                radius = 0
            ),
            position = far_earth.position + Vector2(
                x = r,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = vc
            )
        )
        self.assertAlmostEqual(specific_orbital_energy(spacecraft, far_earth), -28470656.857142854)
        self.assertAlmostEqual(specific_angular_momentum(spacecraft, far_earth), 52821627881.01102)
        self.assertAlmostEqual(semi_major_axis(spacecraft, far_earth), r)
        self.assertAlmostEqual(eccentricity(spacecraft, far_earth), 0)
        self.assertAlmostEqual(apsides(spacecraft, far_earth)[0], r)
        self.assertAlmostEqual(apsides(spacecraft, far_earth)[1], r)
        self.assertAlmostEqual(orbital_period(spacecraft, far_earth), 5828.598860022619)
        self.assertAlmostEqual(radial_velocity(spacecraft, far_earth), 0)