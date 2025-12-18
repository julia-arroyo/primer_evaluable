"""
En este script debes hacer la clase necesaria para resolver los ejercicios
"""
import math
igual_float = 1e-15

class Point:
    def __init__(self, x=None, y=None, z=None, vector=None):
        """Un punto puede definirse por coordenadas o por un vector afín"""
        if vector is not None:
            self.x = vector[0]
            self.y = vector[1]
            self.z = vector[2]

        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
    
    def __str__(self):
        return f"point({self.x},{self.y},{self.z})"
    
    def __add__(self, other):
        """Punto + Vector -> Punto"""
        if isinstance(other, Vector):
            return Point(self.x + other.x, self.y + other.y, self.z + other.z)
        
        raise TypeError("No se puede sumar un punto con ese objeto")

    def __sub__(self, other):
        """
        Punto - Punto obtengo un vector
        Punto - Vector obtengo otro punto (Q = P +(-V))
        """
        if isinstance(other, Point):
            return Vector(p1=other, p2=self)
        
        if isinstance(other, Vector):
            return Point(self.x - other.x, self.y - other.y, self.z - other.z)
        
        raise TypeError("Resta no definida")
    
    def __or__(self, other):
        if isinstance(other, Point):
            if self == other:
                return self
            return Line(p1=self, p2=other)

        if isinstance(other, Vector):
            return Line(p=self, v=other)

        if isinstance(other, Line):
            v = Vector(p1=other.point, p2=self)
            if abs(other.vector * v) < igual_float:
                return other
            return Plane(p=other.point, v=other.vector * v)

        if isinstance(other, Plane):
            v = Vector(p1=other.point, p2=self)
            if abs(other.vector.escalar(v)) < igual_float:
                return other
            return None
        raise TypeError("Unión no definida")
    
    def __eq__(self, other):
        return isinstance(other, Point) and abs(self.x - other.x) < igual_float and abs(self.y - other.y) < igual_float and abs(self.z - other.z) < igual_float
    
    def get(self):
        return (self.x, self.y, self.z)
    
    def distance(self, other):
        """Distancia entre dos puntos"""
        if isinstance(other, Point):
            return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
        
        raise TypeError("Distancia no definida")

class Vector:
    def __init__(self, x=None, y=None, z=None, p1=None, p2=None):
        """Vector por coordenadas o por dos puntos"""
        if p1 is not None and p2 is not None:
            self.x = p2.x - p1.x
            self.y = p2.y - p1.y
            self.z = p2.z - p1.z

        else:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
    
    def __str__(self):
        return f"vector({self.x},{self.y},{self.z})"
    
    def __add__(self, other):
        """
        Vector + Vector es un vector
        Vector + Punto es un punto
        """ 
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
        
        if isinstance(other, Point):
            return other + self
        
        raise TypeError("Suma no definida")
    
    def __sub__(self, other):
        """
        Vector - Vector es un vector
        """
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
        
        raise TypeError("Resta no definida")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        
        if isinstance(other, Vector):
            return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def __rmul__(self, other):
        if isinstance(other, (int, float)):
            return self * other
    
    def escalar(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z
    
    def angle(self, other):
        return math.acos(self.escalar(other) / (abs(self)*abs(other)))
    
    def mixto(self, v2, v3):
        """Producto mixto de tres vectores"""
        return self.escalar(v2 * v3)
    
    def __div__(self, other):
        if isinstance(other, (int, float)):
            if abs(other) < igual_float:
                raise ZeroDivisionError("División por cero")
            return Vector(self.x / other, self.y / other, self.z / other)
        raise TypeError("Un vector solo se puede dividir por un escalar")
    
    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def __eq__(self, other):
        if isinstance(other, Vector) and abs(self - other) < igual_float:
            return True
    
    def __eq__(self, other):
        return (isinstance(other, Vector) and abs(self.x - other.x) < igual_float and abs(self.y - other.y) < igual_float and abs(self.z - other.z) < igual_float)

class Line:
    def __init__(self, p1 = None, p2 = None, p = None, v = None):
        if p1 is not None and p2 is not None:
            if p1 == p2:
                raise ValueError("Dos puntos coincidentes no definen una recta")
            self.point = p1
            self.vector = Vector(p1=p1, p2=p2)
        else:
            self.point = p
            self.vector = v
            self.repr = 'vectorial'
    
    def __str__(self):
        return f"Line: r = {self.point} + t {self.vector}"
    
    def get_vector(self):
        return self.vector
    
    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.vector * other
        if isinstance(other, (Line, Plane)):
            return self.vector * other.get_vector()
        raise TypeError("Multiplicación no definida")
    
    def __and__(self, other):
        if isinstance(other, Line):
            v1 = self.vector
            v2 = other.vector
            p1 = self.point
            p2 = other.point

            # Caso 1: paralelas
            if abs(v1 * v2).__abs__() < igual_float:  # producto vectorial ≈ 0
                if abs((p2 - p1) * v1).__abs__() < igual_float:  # mismas líneas
                    return self
                else:  # paralelas distintas
                    return None

            # Caso 2: verificar si se cortan (coplanares)
            if abs((p2 - p1).mixto(v1, v2)) > igual_float:
                return None  # cruzadas

            # Caso 3: secantes → calculamos punto de intersección aproximado
            maxc = max(abs(v1.x), abs(v1.y), abs(v1.z))
            if maxc == abs(v1.x):
                t = (p2.x - p1.x) / v1.x
            elif maxc == abs(v1.y):
                t = (p2.y - p1.y) / v1.y
            else:
                t = (p2.z - p1.z) / v1.z

            x = p1.x + t*v1.x
            y = p1.y + t*v1.y
            z = p1.z + t*v1.z
            return Point(x, y, z)

        # Intersección con planos
        elif isinstance(other, Plane):
            v_line = self.vector
            n_plane = other.vector
            p_line = self.point
            p_plane = other.point

            denom = v_line.escalar(n_plane)
            if abs(denom) < igual_float:
                # paralela al plano
                if abs((p_line - p_plane).escalar(n_plane)) < igual_float:
                    return self  # la línea está contenida en el plano
                else:
                    return None  # paralela y fuera
            # t de la ecuación paramétrica
            t = -((p_line - p_plane).escalar(n_plane)) / denom
            x = p_line.x + t*v_line.x
            y = p_line.y + t*v_line.y
            z = p_line.z + t*v_line.z
            return Point(x, y, z)

        else:
            return None
    
    def __or__(self, other):
        """Unión con punto o recta"""
        if isinstance(other, Point):
            v = other - self.point
        
            # Si están alineados → el punto pertenece a la línea
            if abs(self.vector * v) < igual_float:   # antes usaba .mod()
                return self
        
            # Si no pertenece → forman un plano
            normal = self.vector * v
            return Plane(p=self.point, v=normal)

        raise TypeError("Unión no definida entre Line y este tipo")
    
    def get(self):
        """Devuelve una tupla con el punto y el vector director de la recta"""
        return (self.point, self.vector)
    
    def distance(self, point):
        if isinstance(point, Point):
            v = self.vector
            w = point - self.point
            cross = v * w
            return math.sqrt(cross.x**2 + cross.y**2 + cross.z**2) / math.sqrt(v.x**2 + v.y**2 + v.z**2)
        raise TypeError("La distancia solo está definida a un Point")
        
class Plane:
    def __init__(self, p=None, v=None, p1=None, p2=None, p3=None):
        """Plano definido por punto+vector o tres puntos"""
        if p is not None and v is not None:
            self.point = p
            self.vector = v
        elif p1 is not None and p2 is not None and p3 is not None:
            v1 = Vector(p1=p1, p2=p2)
            v2 = Vector(p1=p1, p2=p3)
            cross = v1 * v2
            if math.sqrt(cross.x**2 + cross.y**2 + cross.z**2) < igual_float:
                raise ValueError("Los tres puntos son colineales")
            self.point = p1
            self.vector = cross
        else:
            raise ValueError("Parámetros insuficientes para definir un plano")

    def __str__(self):
        return f"Plane: point={self.point}, normal={self.vector}"
    
    def __add__(self, other):
        if isinstance(other, Vector):
            return Plane(p=self.point + other, v=self.vector)
        raise TypeError("No se puede sumar")
    
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Plane(p=self.point - other, v=self.vector)
        raise TypeError("No se puede restar")
    
    def __mul__(self, other):
        """Multiplicación del vector director con un vector, línea o plano"""
        if isinstance(other, Vector):
            return self.vector * other
        if isinstance(other, Line):
            return self.vector * other.vector
        if isinstance(other, Plane):
            return self.vector * other.vector
        raise TypeError("Multiplicación no definida")
    
    def __div__(self, other):
        if isinstance(other, (int, float)):
            return Plane(p=self.point, v=Vector(self.vector.x / other, self.vector.y / other, self.vector.z / other))
        raise TypeError("Sólo se puede dividir por un escalar")
    
    def __abs__(self):
        """Devuelve el módulo del vector director del plano"""
        return abs(self.vector)
    
    def __and__(self, other):
        if isinstance(other, Line):
            v_line = other.vector
            p_line = other.point
            denom = v_line.escalar(self.vector)
            if abs(denom) < igual_float:
                val = (p_line - self.point).escalar(self.vector)
                if abs(val) < igual_float:
                    return other
                return None
            t = -((p_line - self.point).escalar(self.vector)) / denom
            return Point(p_line.x + t*v_line.x,
                         p_line.y + t*v_line.y,
                         p_line.z + t*v_line.z)
        if isinstance(other, Plane):
            n1 = self.vector
            n2 = other.vector
            cross = n1 * n2
            cross_mod = math.sqrt(cross.x**2 + cross.y**2 + cross.z**2)
            if cross_mod < igual_float:
                val = (other.point - self.point).escalar(n1)
                if abs(val) < igual_float:
                    return self
                return None
            p0 = self.point  # simplificación para el punto de la línea de intersección
            return Line(p=p0, v=cross)
        return None
    
    def __or__(self, other):
        if isinstance(other, Point):
            val = (other - self.point).escalar(self.vector)
            if abs(val) < igual_float:
                return self
            return None
        if isinstance(other, Line):
            v_line = other.vector
            p_line = other.point
            val = (p_line - self.point).escalar(self.vector)
            if abs(val) < igual_float and abs(v_line.escalar(self.vector)) < igual_float:
                return self
            return None
        if isinstance(other, Plane):
            n1 = self.vector
            n2 = other.vector
            cross = n1 * n2
            cross_mod = math.sqrt(cross.x**2 + cross.y**2 + cross.z**2)
            if cross_mod < igual_float and abs((other.point - self.point).escalar(n1)) < igual_float:
                return self
            return None
        return None
    
    def __eq__(self, other):
        if not isinstance(other, Plane):
            return False
        # vectores directores paralelos
        if abs(self.vector * other.vector).mod() > igual_float:
            return False
        # comprobar que un punto de self está en other
        v = self.point - other.point
        if abs(other.vector.escalar(v)) > igual_float:
            return False
        return True
    
    def get(self):
        return (self.point, self.vector)
    
    def distance(self, point):
        if isinstance(point, Point):
            num = abs((point - self.point).escalar(self.vector))
            den = math.sqrt(self.vector.x**2 + self.vector.y**2 + self.vector.z**2)
            return num / den
        raise TypeError("Sólo se puede calcular distancia a un punto")