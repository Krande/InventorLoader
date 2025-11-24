import math

class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        if isinstance(x, (list, tuple)):
            self.x, self.y, self.z = map(float, x[:3])
        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)

    @property
    def Length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def length(self):
        return self.Length

    def normalize(self):
        l = self.Length
        if l > 0:
            self.x /= l
            self.y /= l
            self.z /= l
        return self

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector):
             return self.dot(other)
        raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise TypeError("Unsupported operand type for /")
    
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def negative(self): # Saw this in Acis2Step: axis.negative()
        return -self

    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
        
    def __getitem__(self, idx):
        if idx == 0: return self.x
        if idx == 1: return self.y
        if idx == 2: return self.z
        raise IndexError

class Matrix:
    def __init__(self, *args):
        self.A = [[1.0, 0.0, 0.0, 0.0] for _ in range(4)]
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
             # assume flattening or row based
             pass
             
    def unity(self):
        self.A = [[1.0 if i==j else 0.0 for j in range(4)] for i in range(4)]
        
    def rotateX(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        rot = Matrix()
        rot.A[1][1] = c; rot.A[1][2] = -s
        rot.A[2][1] = s; rot.A[2][2] = c
        self.multiply(rot)
        
    def rotateY(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        rot = Matrix()
        rot.A[0][0] = c; rot.A[0][2] = s
        rot.A[2][0] = -s; rot.A[2][2] = c
        self.multiply(rot)

    def rotateZ(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)
        rot = Matrix()
        rot.A[0][0] = c; rot.A[0][1] = -s
        rot.A[1][0] = s; rot.A[1][1] = c
        self.multiply(rot)

    def move(self, vec):
        self.A[0][3] += vec.x
        self.A[1][3] += vec.y
        self.A[2][3] += vec.z

    def multiply(self, other):
        if isinstance(other, Vector):
            x = self.A[0][0]*other.x + self.A[0][1]*other.y + self.A[0][2]*other.z + self.A[0][3]
            y = self.A[1][0]*other.x + self.A[1][1]*other.y + self.A[1][2]*other.z + self.A[1][3]
            z = self.A[2][0]*other.x + self.A[2][1]*other.y + self.A[2][2]*other.z + self.A[2][3]
            return Vector(x, y, z)
        elif isinstance(other, Matrix):
            res = Matrix()
            for i in range(4):
                for j in range(4):
                    res.A[i][j] = sum(self.A[i][k] * other.A[k][j] for k in range(4))
            self.A = res.A

    def inverse(self):
        # Simplified inverse for rigid body transform
        # TODO: Implement proper inverse if needed
        pass

class Placement:
    def __init__(self, base=None, rotation=None):
        self.Base = base if base else Vector()
        self.Rotation = rotation if rotation else Matrix() # FreeCAD uses Quaternion, but let's use Matrix for now or ignore if not critical

    def toMatrix(self):
        m = Matrix()
        # apply rotation
        # apply translation
        return m

    def inverse(self):
        return Placement()

class Base:
    class Vector2d:
        def __init__(self, x=0.0, y=0.0):
            self.x = float(x)
            self.y = float(y)
        def __repr__(self):
            return f"Vector2d({self.x}, {self.y})"
