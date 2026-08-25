import unittest
from constants import EARTH_RADIUS
from collision import has_collision_with_earth

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