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
    p1 : Point, optional
    p2 : Point, optional
    slope : sympy expression, optional
        Two of `p1`, `p2` and `slope` must be supplied to
        find directrix's equation.

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
    """

    def __new__(
        cls, focus=None, p1=None, p2=None, slope=None,
            **kwargs):
        slope = sympify(slope)

        if focus is None:
            focus = Point(0, 0)
        else:
            focus = Point(focus)

        if len(focus) != 2:
            raise ValueError('The focus of "{0}" must be a two dimensional point'.format(cls))

        if len(list(filter(None, (p1, p2, slope)))) != 2:
            raise ValueError('Exactly two arguments of "p1", '
                '"p2", and "slope" must not be None."')

        if slope is not None:
            if p1 is None:
                directrix = Line(p2, slope=slope)
            elif p2 is None:
                directrix = Line(p1, slope=slope)
        else:
            directrix = Line(p1, p2)

        return GeometryEntity.__new__(cls, focus, directrix, **kwargs)

    @property
    def ambient_dimension(self):
        return 2

    @property
    def focus(self):
        """The focus of the parabola.

        Returns
        =======

        focus : number

        See Also
        ========

        sympy.geometry.point.Point
        
        """
        return self.args[0]

    @property
    def directrix(self):
        """The directrix of the parabola.

        Returns
        =======

        directrix : line

        See Also
        ========

        sympy.geometry.line.Line
        
        """
        if self.args[3] is not None:
            if self.args[1] is None:
                direc = Line(self.args[2], self.args[3])
            elif self.args[2] is None:
                direc = Line(self.args[1], self.args[3])
        else:
            direc = Line(self.args[1], self.args[2])        
        return direc
