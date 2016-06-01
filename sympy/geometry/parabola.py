"""Parabolic geometrical entity.

Contains
* Parabola

"""

from __future__ import division, print_function

from sympy.core import S, pi, sympify
from sympy.core.logic import fuzzy_bool
from sympy.core.numbers import Rational, oo
from sympy.core.compatibility import range
from sympy.core.symbol import Dummy
from sympy.simplify import simplify, trigsimp
from sympy.functions.elementary.miscellaneous import sqrt
from sympy.functions.elementary.trigonometric import cos, sin
from sympy.geometry.exceptions import GeometryError
from sympy.polys import DomainError, Poly, PolynomialError
from sympy.polys.polyutils import _not_a_coeff, _nsort
from sympy.solvers import solve
from sympy.utilities.iterables import uniq
from sympy.utilities.misc import filldedent
from sympy.utilities.decorator import doctest_depends_on

from sympy.geometry.entity import GeometryEntity, GeometrySet
from sympy.geometry.point import Point
from sympy.geometry.line import Line, LinearEntity
from sympy.geometry.util import _symbol, idiff

import random


class Parabola(GeometrySet):
    """A parabolic GeometryEntity.

    A parabola is declared with a point, that is called 'focus', and
    a line, that is called 'directrix'.

    Parameters
    ==========

    focus : Point
        Default value is Point(0, 0)
    directrix : Line

    Attributes
    ==========

    focus
    directrix
    axis of symmetry
    vertex
    focal length
    eccentricity

    Raises
    ======
    TypeError
        When `focus` is not a Point.
    ValueError
        When `focus` is not a two dimensional point.
        When `directrix` is neither horizontal nor vertical.

    Examples
    ========

    >>> from sympy import Parabola, Point, Line
    >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7,8)))
    >>> p1.focus
    Point2D(0, 0)
    >>> p1.directrix
    Line(Point2D(5, 8), Point2D(7, 8))
    
    """

    def __new__(cls, focus=None, directrix=None, **kwargs):
        
        if focus is None:
            focus = Point(0, 0)
        else:
            focus = Point(focus)

        if len(focus) != 2:
            raise ValueError('The focus of "{0}" must be a two dimensional point'.format(cls))

        directrix = Line(directrix)

        if (directrix.slope != 0 and directrix.slope != S.Infinity):
            raise ValueError('The directrix must be a horizontal or vertical line'.format(cls))
            
        return GeometryEntity.__new__(cls, focus, directrix, **kwargs)

    @property
    def ambient_dimension(self):
        return 2

    @property
    def focus(self):
        """The focus of the parabola.

        Returns
        =======

        focus : Point

        See Also
        ========

        sympy.geometry.point.Point

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> f1 = Point(0, 0)
        >>> p1 = Parabola(f1, Line(Point(5, 8), Point(7, 8)))
        >>> p1.focus
        Point2D(0, 0)
        
        """
        return self.args[0]

    @property
    def directrix(self):
        """The directrix of the parabola.

        Returns
        =======

        directrix : Line

        See Also
        ========

        sympy.geometry.line.Line
        
        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> l1 = Line(Point(5, 8), Point(6, 8))
        >>> p1 = Parabola(Point(0, 0), l1)
        >>> p1.directrix
        Line(Point2D(5, 8), Point2D(7, 8))
        
        """
        return self.args[1]

    @property
    def axis_of_symmetry(self):
        """The axis of symmetry of the parabola.

        Returns
        =======

        axis_of_symmetry : Line

        See Also
        ========

        sympy.geometry.line.Line

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.axis_of_symmetry
        Line(Point2D(0, 0), Point2D(0, 8))
        
        """

        axis_of_symmetry = self.args[1].perpendicular_line(self.args[0])
        
        return axis_of_symmetry

    @property
    def vertex(self):
        """The vertex of the parabola.

        Returns
        =======

        vertex : Point

        See Also
        ========

        sympy.geometry.point.Point

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.vertex
        Point2D(0, 4)       
        
        """

        axis = self.axis_of_symmetry
        focus = self.args[0]
        directrix = self.args[1]
        distance = directrix.distance(focus)
        if (axis.slope == 0):
            x = -(directrix.coefficients[2])
            if (x < focus.args[0]):
                vertex = Point(x + (distance/2), focus.args[1])
            else:
                vertex = Point(x - (distance/2), focus.args[1])
        else:
            y = -(directrix.coefficients[2])
            if (y > focus.args[1]):
                vertex = Point(focus.args[0], y - (distance/2))
            else:
                vertex = Point(focus.args[0], y + (distance/2))
                
        return vertex

    @property
    def focal_length(self):
        """The focal length of the parabola.

        Returns
        =======

        focal_lenght : number or symbolic expression


        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))
        >>> p1.focal_length
        4
        
        """

        return self.args[0].distance(self.vertex)
        
    @property
    def eccentricity(self):
        """The eccentricity of the parabola.

        Returns
        =======

        eccentricity : number

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))        
        >>> p1.eccentricity
        1

        Notes
        -----
        The eccentricity for every Parabola is 1 by definition.
        
        """       
        return 1

    def equation(self, x='x', y='y'):
        """The equation of the parabola.

        Parameters
        ==========
        x : str, optional
            Label for the x-axis. Default value is 'x'.
        y : str, optional
            Label for the y-axis. Default value is 'y'.
            
        Returns
        =======
        equation : sympy expression

        Examples
        ========

        >>> from sympy import Parabola, Point, Line
        >>> p1 = Parabola(Point(0, 0), Line(Point(5, 8), Point(7, 8)))        
        >>> p1.equation()
        -x**2 + 16*y - 64      
        
        """
        x = _symbol(x)
        y = _symbol(y)
        
        axis = self.axis_of_symmetry

        if (axis.slope == 0):
            t1 = 4*(self.focal_length)*(x-self.vertex.x)
            t2 = (y-self.vertex.y)**2
        else:
            t1 = 4*(self.focal_length)*(y-self.vertex.y)
            t2 = (x-self.vertex.x)**2
        return t1 - t2
        
