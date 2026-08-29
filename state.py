from dataclasses import dataclass
from math import sqrt

@dataclass(frozen = True)
class Vector2:
    x: float
    y: float
    
    def magnitude(self) -> float:
        return sqrt((self.x ** 2) + (self.y ** 2))
    
    def __add__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2":
        return self.__mul__(scalar)
    
@dataclass(frozen = True)
class Body:
    name: str
    mass: float
    radius: float
    
@dataclass(frozen = True)
class BodyState:
    body: Body
    position: Vector2
    velocity: Vector2
    
@dataclass(frozen = True)
class SystemState:
    bodies: tuple[BodyState, ...]
    time: float = 0.0