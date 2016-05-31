from __future__ import division

from sympy import Dummy, Rational, S, Symbol, pi, sqrt, oo
from sympy.core.compatibility import range
from sympy.geometry import (Circle, Ellipse, GeometryError, Line, Point, Polygon, Ray, RegularPolygon, Segment,
                            Triangle, intersection, Parabola)
from sympy.integrals.integrals import Integral
from sympy.utilities.pytest import raises, slow

@slow
def test_parabola_geom():
    
