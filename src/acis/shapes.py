class Shape:
    def toShape(self):
        return self

class Edge(Shape):
    def __init__(self, curve=None):
        self.Curve = curve

class Face(Shape):
    def __init__(self, surface=None):
        self.Surface = surface

class Wire(Shape):
    def __init__(self, edges=None):
        self.Edges = edges if edges else []

class Line(Shape):
    def __init__(self, start=None, end=None):
        self.Start = start
        self.End = end
        self.StartPoint = start
        self.EndPoint = end
        if start and end:
            self.Location = start
            self.Direction = (end - start).normalize()

class LineSegment(Line):
    pass

class Circle(Shape):
    def __init__(self, center=None, axis=None, radius=0.0):
        self.Center = center
        self.Axis = axis
        self.Radius = radius

class Ellipse(Shape):
    def __init__(self, center=None, axis=None, major=0.0, minor=0.0):
        self.Center = center
        self.Axis = axis
        self.MajorRadius = major
        self.MinorRadius = minor

class BSplineCurve(Shape):
    def __init__(self):
        self.Degree = 1
        self.Rational = False
        self.Closed = False
        self.Poles = []
        self.Weights = []
        self.Knots = []
        self.Mults = []

    def buildFromPolesMultsKnots(self, poles, mults, knots, periodic, degree, weights=None):
        self.Poles = poles
        self.Mults = mults
        self.Knots = knots
        self.Closed = periodic
        self.Degree = degree
        self.Weights = weights
        self.Rational = weights is not None

    def isRational(self):
        return self.Rational

    def isClosed(self):
        return self.Closed

    def getPoles(self):
        return self.Poles
    
    def getWeights(self):
        return self.Weights
    
    def getKnots(self):
        return self.Knots
    
    def getMultiplicities(self):
        return self.Mults
        
    def interpolate(self, points):
        # Mock interpolation: just store points as poles (linear)
        self.Poles = points
        self.Degree = 1
        self.Rational = False
        self.Closed = False
        # Generate dummy knots/mults
        self.Mults = [1] * len(points)
        self.Mults[0] = 2
        self.Mults[-1] = 2
        self.Knots = list(range(len(points))) # very dummy

class BSplineSurface(Shape):
    def __init__(self):
        self.UDegree = 1
        self.VDegree = 1
        self.URational = False
        self.VRational = False
        self.UClosed = False
        self.VClosed = False
        self.Poles = [] # 2D array
        self.Weights = [] # 2D array
        self.UKnots = []
        self.VKnots = []
        self.UMults = []
        self.VMults = []

    def buildFromPolesMultsKnots(self, poles, umults, vmults, uknots, vknots, uperiodic, vperiodic, udegree, vdegree, weights=None):
        self.Poles = poles
        self.UMults = umults
        self.VMults = vmults
        self.UKnots = uknots
        self.VKnots = vknots
        self.UClosed = uperiodic
        self.VClosed = vperiodic
        self.UDegree = udegree
        self.VDegree = vdegree
        self.Weights = weights
        self.URational = weights is not None # simplified

    def isUClosed(self): return self.UClosed
    def isVClosed(self): return self.VClosed
    def getUMultiplicities(self): return self.UMults
    def getVMultiplicities(self): return self.VMults
    def getUKnots(self): return self.UKnots
    def getVKnots(self): return self.VKnots
    def getPoles(self): return self.Poles
    def getWeights(self): return self.Weights

class Plane(Shape):
    def __init__(self, position=None, axis=None):
        self.Position = position
        self.Axis = axis

class Cylinder(Shape):
    def __init__(self, center=None, axis=None, radius=0.0):
        self.Center = center
        self.Axis = axis
        self.Radius = radius

class Cone(Shape):
    def __init__(self, center=None, axis=None, radius1=0.0, radius2=0.0):
        self.Center = center
        self.Axis = axis
        self.Radius1 = radius1
        self.Radius2 = radius2
        # Acis2Step checks instance but uses surface attributes for Cone, so we might not need attributes here

class Sphere(Shape):
    def __init__(self, center=None, radius=0.0):
        self.Center = center
        self.Radius = radius

class Toroid(Shape):
    def __init__(self, center=None, axis=None, majorRadius=0.0, minorRadius=0.0):
        self.Center = center
        self.Axis = axis
        self.MajorRadius = majorRadius
        self.MinorRadius = minorRadius

class SurfaceOfRevolution(Shape):
    def __init__(self, curve=None, center=None, direction=None):
        self.Curve = curve
        self.Center = center
        self.Direction = direction
        
class ArcOfCircle(Shape):
     pass

class ArcOfEllipse(Shape):
     pass

# Mocking module structure
class Geom2d:
    class BSplineCurve2d(BSplineCurve):
        pass

class Point(Shape):
    def __init__(self, location=None):
        self.X = location.x if location else 0.0
        self.Y = location.y if location else 0.0
        self.Z = location.z if location else 0.0
        self.Location = location

def makeLine(start, end):
    return Line(start, end)

def makePolygon(points):
    return Wire()

def makeFilledFace(edges):
    return Face()

def makeRuledSurface(c1, c2):
    return Face()

def show(shape, label=None):
    pass
