import unittest
from constants import EARTH_MU, EARTH_RADIUS
from diagnostics import specific_orbital_energy, semi_major_axis, eccentricity, apsides, escape_velocity
from math import sqrt

class TestDiagnostics(unittest.TestCase):
    # Circular
    circular_r = 7000000
    circular_vc = sqrt(EARTH_MU / circular_r)
    def test_circular_specific_energy(self):
        energy = specific_orbital_energy(self.circular_r, 0, 0, self.circular_vc)
        expected_energy = -(EARTH_MU / (2 * self.circular_r))
        self.assertAlmostEqual(energy, expected_energy, delta=1e-6)
    def test_circular_eccentricity(self):
        e = eccentricity(self.circular_r, 0, 0, self.circular_vc)
        self.assertAlmostEqual(e, 0.0, delta=1e-12)
        
    # Ellipse
    ellipse_r = 10000000
    ellipse_vc = 0.9 * sqrt(EARTH_MU / ellipse_r)
    def test_elliptical_eccentricity(self):
        e = eccentricity(self.ellipse_r, 0, 0, self.ellipse_vc)
        expected_e = 0.19
        self.assertAlmostEqual(e, expected_e, delta=1e-6)
    def test_elliptical_apsides(self):
        periapsis, apoapsis = apsides(self.ellipse_r, 0, 0, self.ellipse_vc)
        expected_periapsis = 6806723
        expected_apoapsis = 10000000
        self.assertAlmostEqual(periapsis, expected_periapsis, delta=1)
        self.assertAlmostEqual(apoapsis, expected_apoapsis, delta=1)
    
    # Invalid input
    escape_r = 7000000
    escape_ve = sqrt((2 * EARTH_MU) / escape_r)
    def test_escape_orbit_has_no_bound_semi_major_axis(self):
        with self.assertRaises(ValueError):
            semi_major_axis(self.escape_r, 0, 0, self.escape_ve)
            
    # Escape velocity
    def test_escape_velocity(self):
        x1, y1 = EARTH_RADIUS, 0
        x2, y2 = 7000000, 0
        x3, y3 = 0, 0
        ve1 = escape_velocity(x1, y1)
        ve2 = escape_velocity(x2, y2)
        expected_ve1 = 11185.98
        expected_ve2 = 10671.58
        self.assertAlmostEqual(ve1, expected_ve1, delta=0.01)
        self.assertAlmostEqual(ve2, expected_ve2, delta=0.01)
        with self.assertRaises(ValueError):
            escape_velocity(x3, y3)