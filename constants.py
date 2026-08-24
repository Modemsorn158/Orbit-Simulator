"""Physical constants for the simulator, expressed in SI units."""

GRAVITATIONAL_CONSTANT = 6.67430e-11  # m^3 kg^-1 s^-2
EARTH_MASS = 5.972e24  # kg
EARTH_RADIUS = 6.371e6  # m
EARTH_MU = (GRAVITATIONAL_CONSTANT * EARTH_MASS)  # m^3 s^-2
EARTH_SURFACE_GRAVITY = (EARTH_MU / (EARTH_RADIUS ** 2))  # m s^-2