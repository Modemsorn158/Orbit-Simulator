import unittest
from diagnostics import altitude
from simulation import simulate
from constants import EARTH_RADIUS, EARTH_MU
from collision import has_collision_with_earth, estimate_earth_impact_time
from integrators import velocity_verlet_step
from math import sqrt

class TestCollisions(unittest.TestCase):
    # Earth collisions
    def test_earth_collision(self):
        x1, y1 = EARTH_RADIUS, 0
        x2, y2 = EARTH_RADIUS + 1, 0
        x3, y3 = 0, 0
        c1 = has_collision_with_earth(x1, y1)
        c2 = has_collision_with_earth(x2, y2)
        c3 = has_collision_with_earth(x3, y3)
        self.assertTrue(c1)
        self.assertFalse(c2)
        self.assertTrue(c3)
        
    # Simulation test
    def test_collision_simulation(self):
        x1, y1 = EARTH_RADIUS, 0
        x2, y2 = 7000000, 0
        vc1 = sqrt(EARTH_MU / EARTH_RADIUS)
        vc2 = sqrt(EARTH_MU / x2)
        states1 = simulate(x1, y1, 0, vc1, 10, 500, velocity_verlet_step, has_collision_with_earth)
        states2 = simulate(x2, y2, 0, vc2, 10, 500, velocity_verlet_step, has_collision_with_earth)
        self.assertEqual(len(states1), 1)
        self.assertEqual(len(states1[0]), 4)
        self.assertEqual(len(states2), 501)
        
    # Collision altitude estimation test
    def test_collision_altitude(self):
        t = estimate_earth_impact_time([1000 + EARTH_RADIUS, 0, 0, 0], [-1000 + EARTH_RADIUS, 0, 0, 0], 2)
        self.assertEqual(t, 1)
        with self.assertRaises(ValueError):
            estimate_earth_impact_time([EARTH_RADIUS + 1, 0, 0, 0], [EARTH_RADIUS + 1, 0, 0, 0], 1)
            
    # Impact test
    def test_impact(self):
        r = 7000000
        vc = sqrt(EARTH_MU / r)
        states1 = simulate(r, 0, 0, (0.9 * vc), 1, 10000, velocity_verlet_step, has_collision_with_earth, estimate_earth_impact_time)
        state1_final = states1[-1]
        alt1 = altitude(state1_final[0], state1_final[1])
        states2 = simulate(r, 0, 0, (0.9 * vc), 1, 10000, velocity_verlet_step, has_collision_with_earth)
        state2_final = states2[-1]
        alt2 = altitude(state2_final[0], state2_final[1])
        self.assertLess(abs(alt1), 1)
        self.assertLess(alt2, 0)