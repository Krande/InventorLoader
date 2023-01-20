from dataclasses import dataclass, field

import numpy as np


@dataclass
class VEC:
    x: float
    y: float
    z: float
    _vec: np.array = field(init=False)

    def __post_init__(self):
        self._vec = np.array([self.x, self.y, self.z])

    def __mul__(self, other):
        if isinstance(other, float):
            return VEC(*(self._vec * other))
        else:
            raise NotImplemented()


@dataclass
class Part:
    ...

    @staticmethod
    def BSplineSurface():
        ...

    @staticmethod
    def BSplineCurve():
        return BSplineCurve()


@dataclass
class BSplineCurve:
    def buildFromPolesMultsKnots(self, poles, mults, knots, periodic, degree, weights):
        ...

    def toShape(self):
        ...
