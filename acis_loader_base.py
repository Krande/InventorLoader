from dataclasses import dataclass, field

import numpy as np


@dataclass
class VEC:
    x: float
    y: float
    z: float
    _vec: np.array = field(init=False, repr=False)

    def __post_init__(self):
        self._vec = np.array([self.x, self.y, self.z])

    def __mul__(self, other):
        if isinstance(other, float):
            return VEC(*(self._vec * other))
        else:
            raise NotImplemented()


@dataclass
class Part:
    @staticmethod
    def BSplineSurface():
        raise NotImplemented()

    @staticmethod
    def BSplineCurve():
        return BSplineCurve()


@dataclass
class BSplineCurve:
    poles: list[VEC] = field(init=False)
    mults: list[int] = field(init=False)
    knots: list[float] = field(init=False)
    periodic: bool = field(init=False)
    degree: int = field(init=False)
    weights: list[float] = field(init=False)

    def buildFromPolesMultsKnots(self, poles: list[VEC], mults, knots, periodic, degree, weights=None):
        self.poles = poles
        self.mults = mults
        self.knots = knots
        self.periodic = periodic
        self.degree = degree
        self.weights = weights

    def toShape(self):
        return Shape(self, "forward")


@dataclass
class Shape:
    bspline: BSplineCurve
    Orientation: str

    def reversed(self):
        self.Orientation = "reversed" if self.Orientation == "forward" else "forward"
