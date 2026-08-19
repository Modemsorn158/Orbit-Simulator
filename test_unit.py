from Physics import gravitational_acceleration, simulate
from Physics import mu_Earth, r_Earth, vc
from math import sqrt
import random
import pytest

def test_gravity_acceleration():
    n = 100
    min_value = 1
    max_value = 7000000

    for i in range(n):
        ax, ay = gravitational_acceleration(random.randint(min_value, max_value), 0)
        
        assert (ax < 0 and ay == 0)

def test_gravity_magnitude():
    g_Standard = 9.80665
    g_Calculated = mu_Earth/(r_Earth**2)

    assert g_Calculated == pytest.approx(expected=g_Standard, rel=0.0015) # Rounded Earth constants lead to a 0.139% error

def test_circular_velocity():
    vc_Earth_Radius = 7909.786939924
    vc_Calculated = sqrt(mu_Earth/r_Earth)

    assert vc_Calculated == pytest.approx(expected=vc_Earth_Radius)

def run_test(x, y, vx, vy, dt, steps):
    result, energies, angular_momenta = simulate(x, y, vx, vy, dt, steps)

    h1 = angular_momenta[0]
    hn = angular_momenta[-1]    
    ph = ((hn-h1)/abs(h1))*100

    return abs(ph)

def test_angular_momentum():
    tolerance = 1*(10**-12)

    differences = []
    differences.append(run_test(7000000, 0, 0, vc, 1, 9000))
    differences.append(run_test(7000000, 0, 0, vc, 5, 1800))
    differences.append(run_test(7000000, 0, 0, vc, 10, 900))
    differences.append(run_test(7000000, 0, 0, vc, 30, 300))

    for i in differences:
        assert (i < tolerance)