import unittest
from maneuvers import apply_delta_v, apply_prograde_delta_v, hohmann_transfer

class TestManeuvers(unittest.TestCase):
    # Delta v
    def test_apply_delta_v(self):
        vx1, vy1, delta_vx1, delta_vy1 = 0, 7500, 0, 100
        new_vx1, new_vy1 = apply_delta_v(vx1, vy1, delta_vx1, delta_vy1)
        expected_vx1, expected_vy1 = 0, 7600
        vx2, vy2, delta_vx2, delta_vy2 = 100, -50, -20, 70
        new_vx2, new_vy2 = apply_delta_v(vx2, vy2, delta_vx2, delta_vy2)
        expected_vx2, expected_vy2 = 80, 20
        self.assertAlmostEqual(new_vx1, expected_vx1, delta=1)
        self.assertAlmostEqual(new_vy1, expected_vy1, delta=1)
        self.assertAlmostEqual(new_vx2, expected_vx2, delta=1)
        self.assertAlmostEqual(new_vy2, expected_vy2, delta=1)
        
    # Prograde delta v
    def test_apply_prograde_delta_v(self):
        vx1, vy1, delta_v1 = 0, 7500, 100
        new_vx1, new_vy1 = apply_prograde_delta_v(vx1, vy1, delta_v1)
        expected_vx1, expected_vy1 = 0, 7600
        vx2, vy2, delta_v2 = 3, 4, 5
        new_vx2, new_vy2 = apply_prograde_delta_v(vx2, vy2, delta_v2)
        expected_vx2, expected_vy2 = 6, 8
        vx3, vy3, delta_v3 = 0, 0, 0
        self.assertAlmostEqual(new_vx1, expected_vx1, delta=1)
        self.assertAlmostEqual(new_vy1, expected_vy1, delta=1)
        self.assertAlmostEqual(new_vx2, expected_vx2, delta=1)
        self.assertAlmostEqual(new_vy2, expected_vy2, delta=1)
        with self.assertRaises(ValueError):
            apply_prograde_delta_v(vx3, vy3, delta_v3)
            
    # Hohmann transfer
    def test_hohmann_transfer(self):
        r1, r2 = 7000000, 10000000
        delta_v1, delta_v2, t = hohmann_transfer(r1, r2)
        expected_delta_v1 = 638.782
        expected_delta_v2 = 584.082
        expected_t = 3899.559
        self.assertAlmostEqual(delta_v1, expected_delta_v1, delta=1e-3)
        self.assertAlmostEqual(delta_v2, expected_delta_v2, delta=1e-3)
        self.assertAlmostEqual(t, expected_t, delta=1e-3)