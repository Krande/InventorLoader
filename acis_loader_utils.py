import logging
import traceback
from dataclasses import dataclass
from struct import Struct, unpack_from

from importerConstants import CENTER

UINT8 = Struct("<B").unpack_from
UINT16 = Struct("<H").unpack_from
SINT32 = Struct("<l").unpack_from
UINT32 = Struct("<L").unpack_from
FLOAT32 = Struct("<f").unpack_from
FLOAT64 = Struct("<d").unpack_from
SINT16 = Struct("<h").unpack_from
SINT64 = Struct("<q").unpack_from
UINT64 = Struct("<Q").unpack_from
_colorDefault = ""


def getUInt8(data, offset):
    """
    Returns a single unsingned 8-Bit value (byte).
    Args:
            data
                    A binary string.
            offset
                    The zero based offset of the byte.
    Returns:
            The unsigned 8-Bit value at offset.
            The new position in the 'stream'.
    """
    (val,) = UINT8(data, offset)
    return val, offset + 1


def getUInt16(data, offset):
    """
    Returns a single unsingned 16-Bit value.
    Args:
            data
                    A binary string.
            offset
                    The zero based offset of the unsigned 16-Bit value.
    Returns:
            The unsigned 16-Bit value at offset.
            The new position in the 'stream'.
    """
    (val,) = UINT16(data, offset)
    return val, offset + 2


def getSInt16(data, offset):
    """
    Returns a single signed 16-Bit value.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the signed 16-Bit value.
    Returns:
        The signed 16-Bit value at offset.
        The new position in the 'stream'.
    """
    (val,) = SINT16(data, offset)
    return val, offset + 2


def getSInt64(data, offset):
    """
    Returns a single signed 64-Bit value.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the signed 32-Bit value.
    Returns:
        The signed 32-Bit value at offset.
        The new position in the 'stream'.
    """
    (val,) = SINT64(data, offset)
    return val, offset + 8


def getFloat32(data, offset):
    """
    Returns a double precision float value from a single one.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the array.
    Returns:
        The double precision float value at offset from a single one.
        The new position in the 'stream'.
    """
    (val,) = FLOAT32(data, offset)
    val = float(val)
    return val, offset + 4


def getFloat64A(data, offset, size):
    """
    Returns an array of double precision float values.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the array.
        size
            The size of the array.
    Returns:
        The array of double precision float values at offset.
        The new position in the 'stream'.
    """
    val = unpack_from("<" + "d" * int(size), data, offset)
    return val, int(offset + 8 * size)


def isEqual(a, b, e=0.0001):
    if a is None:
        return isEqual(b, CENTER)
    if b is None:
        return isEqual(a, CENTER)
    return (a - b).Length < e


def isString(value):
    if type(value) is str:
        return True
    return False


def isEqual1D(a, b, e=0.0001):
    if a is None:
        return isEqual1D(b, 0.0)
    if b is None:
        return isEqual1D(a, 0.0)
    return abs(a - b) < e


def getSInt32(data, offset):
    """
    Returns a single signed 32-Bit value.
    Args:
            data
                    A binary string.
            offset
                    The zero based offset of the signed 32-Bit value.
    Returns:
            The signed 32-Bit value at offset.
            The new position in the 'stream'.
    """
    (val,) = SINT32(data, offset)
    return val, offset + 4


def getUInt32(data, offset):
    """
    Returns a single unsingned 32-Bit value.
    Args:
            data
                    A binary string.
            offset
                    The zero based offset of the unsigned 32-Bit value.
    Returns:
            The unsigned 32-Bit value at offset.
            The new position in the 'stream'.
    """
    (val,) = UINT32(data, offset)
    return val, offset + 4


def getFloat64(data, offset):
    """
    Returns a double precision float value.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the array.
    Returns:
        The double precision float value at offset.
        The new position in the 'stream'.
    """
    (val,) = FLOAT64(data, offset)
    return val, offset + 8


def getUInt64(data, offset):
    """
    Returns a single unsingned 64-Bit value.
    Args:
        data
            A binary string.
        offset
            The zero based offset of the unsigned 64-Bit value.
    Returns:
        The unsigned 64-Bit value at offset.
        The new position in the 'stream'.
    """
    (val,) = UINT64(data, offset)
    return val, offset + 8


def logWarning(msg, *args):
    logging.warning(msg)


def logError(msg, *args):
    logging.error(msg)


def long(x):
    return float(x)


def createBSplinesPCurve(*args):
    ...


def createBSplinesSurface(spline):
    ...


def createLine(*args):
    ...


def reshape(a, d):
    ...


def createEllipse():
    ...


def createCircle():
    ...


def getColorDefault():
    global _colorDefault
    return _colorDefault


def createBSplinesCurve(nubs, sense):
    from acis_loader_base import Part

    if nubs is None:
        return None
    number_of_poles = len(nubs.poles)
    if number_of_poles == 2:  # if there are only two poles we can simply draw a line
        shape = createLine(nubs.poles[0], nubs.poles[1])
    else:
        shape = None
        try:
            bsc = Part.BSplineCurve()
            if nubs.rational:
                bsc.buildFromPolesMultsKnots(
                    poles=nubs.poles,
                    mults=nubs.uMults,
                    knots=nubs.uKnots,
                    periodic=False,
                    degree=nubs.uDegree,
                    weights=nubs.weights,
                )
            else:
                bsc.buildFromPolesMultsKnots(
                    poles=nubs.poles, mults=nubs.uMults, knots=nubs.uKnots, periodic=False, degree=nubs.uDegree
                )
            # periodic = nubs.uPeriodic
            shape = bsc.toShape()
        except Exception as e:
            logError(traceback.format_exc())
    if shape is not None:
        shape.Orientation = str("Reversed") if (sense == "reversed") else str("Forward")
    return shape


# Dummy Classes


@dataclass
class V2D:
    x: float
    y: float


@dataclass
class PLC:
    center: object = None
    axis: object = None
    angle: float = None


class MAT:
    def __init__(self, *args):
        self.args = args
