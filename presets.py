from state import *
from constants import *

solar_system = SystemState(
    body_states = (
        BodyState(
            body = Body(
                name = "Sun",
                mass = SUN_MASS,
                radius = SUN_RADIUS
            ),
            position = Vector2(
                x = 0,
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = -16
            )
        ),
        BodyState(
            body = Body(
                name = "Mercury",
                mass = MERCURY_MASS,
                radius = MERCURY_RADIUS
            ),
            position = Vector2(
                x = 5.79 * (10 ** 10),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 4.787 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Venus",
                mass = VENUS_MASS,
                radius = VENUS_RADIUS
            ),
            position = Vector2(
                x = 1.082 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 3.502 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Earth",
                mass = EARTH_MASS,
                radius = EARTH_RADIUS
            ),
            position = Vector2(
                x = 1.496 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 2.9785 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Moon",
                mass = MOON_MASS,
                radius = MOON_RADIUS
            ),
            position = Vector2(
                x = 1.49984 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 3.078 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Mars",
                mass = MARS_MASS,
                radius = MARS_RADIUS
            ),
            position = Vector2(
                x = 2.279 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 2.4077 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Jupiter",
                mass = JUPITER_MASS,
                radius = JUPITER_RADIUS
            ),
            position = Vector2(
                x = 7.785 * (10 ** 11),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 1.307 * (10 ** 4)
            )
        ),
        BodyState(
            body = Body(
                name = "Saturn",
                mass = SATURN_MASS,
                radius = SATURN_RADIUS
            ),
            position = Vector2(
                x = 1.4335 * (10 ** 12),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 9.689 * (10 ** 3)
            )
        ),
        BodyState(
            body = Body(
                name = "Uranus",
                mass = URANUS_MASS,
                radius = URANUS_RADIUS
            ),
            position = Vector2(
                x = 2.871 * (10 ** 12),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 6.8 * (10 ** 3)
            )
        ),
        BodyState(
            body = Body(
                name = "Neptune",
                mass = NEPTUNE_MASS,
                radius = NEPTUNE_RADIUS
            ),
            position = Vector2(
                x = 4.503443661 * (10 ** 12),
                y = 0
            ),
            velocity = Vector2(
                x = 0,
                y = 5.43 * (10 ** 3)
            )
        )
    ),
    time = 0
)