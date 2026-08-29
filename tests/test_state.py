import unittest
from state import *

class TestState(unittest.TestCase):
    # Vector manipulation
    def test_vector_operation(self):
        self.assertTrue(Vector2(1, 2) + Vector2(3, 4) == Vector2(4, 6))
        self.assertTrue(Vector2(3, 4).magnitude() == 5)
        self.assertTrue(Vector2(1, 2) * 3 == Vector2(3, 6))
        self.assertTrue(3 * Vector2(1, 2) == Vector2(3, 6))