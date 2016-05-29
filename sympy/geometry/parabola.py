"""Parabolic geometrical entities.

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

from .entity import GeometryEntity, GeometrySet
from .point import Point
from .line import Line, LinearEntity
from .util import _symbol, idiff

import random


class Parabola(GeometrySet):
    """A parabolic GeometryEntity.

    Parameters
    ==========



    Attributes
    ==========


    Raises
    ======




    Examples
    ========



    Plotting:


    """

