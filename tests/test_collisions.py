import unittest
from simulation import simulate
from constants import EARTH_RADIUS, EARTH_MU
from collision import has_collision_with_earth
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