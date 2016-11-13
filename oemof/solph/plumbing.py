# -*- coding: utf-8 -*-
"""

"""
from collections import abc, UserList
from pyomo.core import Constraint, Objective
import pyomo.core.base as po_base


def Sequence(sequence_or_scalar):
    """ Tests if an object is sequence (except string) or scalar and returns
    a the original sequence if object is a sequence and a 'emulated' sequence
    object of class _Sequence if object is a scalar or string.

    Parameters
    ----------
    sequence_or_scalar : array-like or scalar (None, int, etc.)

    Examples
    --------
    >>> Sequence([1,2])
    [1, 2]

    >>> x = Sequence(10)
    >>> x[0]
    10

    >>> x[10]
    10
    >>> print(x)
    [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    """
    if (isinstance(sequence_or_scalar, abc.Iterable) and not
            isinstance(sequence_or_scalar, str)):
        return sequence_or_scalar
    else:
        return _Sequence(default=sequence_or_scalar)


class _Sequence(UserList):
    """ Emulates a list whose length is not known in advance.

    Parameters
    ----------
    source:
    default:


    Examples
    --------
    >>> s = _Sequence(default=42)
    >>> len(s)
    0
    >>> s[2]
    42
    >>> len(s)
    3
    >>> s[0] = 23
    >>> s
    [23, 42, 42]

    """
    def __init__(self, *args, **kwargs):
        self.default = kwargs["default"]
        super().__init__(*args)

    def __getitem__(self, key):
        try:
            return self.data[key]
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            return self.data[key]

    def __setitem__(self, key, value):
        try:
            self.data[key] = value
        except IndexError:
            self.data.extend([self.default] * (key - len(self.data) + 1))
            self.data[key] = value



class LExpression(object):
    """Affine linear expression of optimisation variables.

    Affine expression of the form:

    constant + coeff1*var1 + coeff2*var2 + ....

    Parameters
    ----------
    variables : list
        List of tuples of coefficients and variables
        e.g. [(coeff1,var1),(coeff2,var2),...]
    constant : float

    Note
    ----
    Code has been taken and adapted from pyPSA
    (https://github.com/FRESNA/PyPSA), Copyright 2015-2016
    Tom Brown (FIAS), Jonas Hoersch (FIAS), GNU GPL 3
    """

    def __init__(self, variables=None, constant=0.):

        if variables is None:
            self.variables = []
        else:
            self.variables = variables

        self.constant = constant

    def __repr__(self):
        return "{} + {}".format(self.variables, self.constant)


    def __mul__(self, constant):
        try:
            constant = float(constant)
        except:
            print("Can only multiply an LExpression with a float!")
            return None
        return LExpression([(constant * item[0], item[1])
                                 for item in self.variables],
                            constant * self.constant)

    def __rmul__(self, constant):
        return self.__mul__(constant)

    def __add__(self, other):
        if type(other) is LExpression:
            return LExpression(self.variables + other.variables,
                               self.constant + other.constant)
        else:
            try:
                constant = float(other)
            except:
                print("Can only add an LExpression to another \
                       LExpression or a constant!")
                return None
            return LExpression(self.variables[:], self.constant+constant)


    def __radd__(self,other):
        return self.__add__(other)

    def __pos__(self):
        return self

    def __neg__(self):
        return -1*self

class LConstraint(object):
    """Constraint of optimisation variables.

    Linear constraint of the form:

        lhs sense rhs

    Parameters
    ----------
    lhs : LExpression
        Left-hand-side expression constraint
    sense : string
        Sense of constraint, one of: '==', '<=', '>='. Default is '=='.
    rhs : LExpression
        Right-hand-side expression of constraint

    Note
    ------
    Code has been taken and adapted from pyPSA
    (https://github.com/FRESNA/PyPSA), Copyright 2015-2016
    Tom Brown (FIAS), Jonas Hoersch (FIAS), GNU GPL 3
    """

    def __init__(self, lhs=None, sense="==", rhs=None):

        if lhs is None:
            self.lhs = LExpression()
        else:
            self.lhs = lhs

        self.sense = sense

        if rhs is None:
            self.rhs = LExpression()
        else:
            self.rhs = rhs

    def __repr__(self):
        return "{} {} {}".format(self.lhs, self.sense, self.rhs)


def linear_constraint(block, name, constraints, *args, **kwargs):
    """A replacement for pyomo's Constraint class that quickly builds linear
    constraints.

    Instead of pyomo standard call:

    model.name = Constraint(index1, index2, ..., rule=f)

    call instead:

    linear_constraint(model, name, constraints, index1, index2,...)

    where constraints is a dictionary of constraints of the form:

    constraints[i] = LConstraint object

    Parameters
    ----------
    block : pyomo.environ.Block
        A pyomo block to which the constraint is added
    name : string
        Name of constraint that is added to the block
    constraints : dict
        A dictionary of constraints (see format above)
    *args :
        Indices of the constraints
    **kwargs : possible keys: 'indices'
        Own indices, if 'indices' exist in kwargs do not pass index1, index2 etc.
        They will be overwritten.

    Note
    ------
    Code has been taken and adapted from pyPSA
    (https://github.com/FRESNA/PyPSA), Copyright 2015-2016
    Tom Brown (FIAS), Jonas Hoersch (FIAS), GNU GPL 3
    """

    # if 'keys' exist use this as constraint keys, otherwise construct
    # passed index *args: e.g. idx1,idx2....
    if kwargs.get('indices') is not None:
        keys = kwargs.get('indices')
        setattr(block, name,
                po_base.constraint.IndexedConstraint(noruleinit=True))
        v = getattr(block, name)
        v._index = keys
    else:
        # first we create a constraint with nothin in it
        setattr(block, name, Constraint(*args, noruleinit=True))
        # v is our constraint object
        v = getattr(block, name)


    for i in v._index:
        c = constraints[i]
        if type(c) is LConstraint:
            variables = c.lhs.variables + [(-item[0],item[1])
                                           for item in c.rhs.variables]
            sense = c.sense
            constant = c.rhs.constant - c.lhs.constant
        else:
            raise ValueError(('Argument `constraint` must be of type \
                               LConstraint!'))

        v._data[i] = po_base.constraint._GeneralConstraintData(None, v)
        v._data[i]._body = po_base.expr_coopr3._SumExpression()
        v._data[i]._body._args = [item[1] for item in variables]
        v._data[i]._body._coef = [item[0] for item in variables]
        v._data[i]._body._const = 0.
        if sense == "==":
            v._data[i]._equality = True
            v._data[i]._lower = po_base.numvalue.NumericConstant(constant)
            v._data[i]._upper = po_base.numvalue.NumericConstant(constant)
        elif sense == "<=":
            v._data[i]._equality = False
            v._data[i]._lower = None
            v._data[i]._upper = po_base.numvalue.NumericConstant(constant)
        elif sense == ">=":
            v._data[i]._equality = False
            v._data[i]._lower = po_base.numvalue.NumericConstant(constant)
            v._data[i]._upper = None
        elif sense == "><":
            v._data[i]._equality = False
            v._data[i]._lower = po_base.numvalue.NumericConstant(constant[0])
            v._data[i]._upper = po_base.numvalue.NumericConstant(constant[1])
        else:
            raise KeyError(
                '`Sense` must be one of "==","<=",">=","><"; got: {}'.format(
                                                                        sense))

def linear_objective(model, objective=None):
    """
    A replacement for pyomo's Objective that quickly builds linear
    objectives.

    Instead of

    model.objective = Objective(expr=sum(vars[i]*coeffs[i] for i in index)
                      + constant)

    call instead

    linear_objective(model, objective)

    where objective is an LExpression.

    Variables may be repeated with different coefficients, which pyomo
    will sum up.


    Parameters
    ----------
    model : pyomo.core.Block
        The pyomo block / model to which the objective expression is added.
    objective : LExpression
        Linear expression of the objective function.

     Note
    ------
    Code has been taken and adapted from pyPSA
    (https://github.com/FRESNA/PyPSA), Copyright 2015-2016
    Tom Brown (FIAS), Jonas Hoersch (FIAS), GNU GPL 3
    """

    if objective is None:
        objective = LExpression()

    #initialise with a dummy
    model.objective = Objective(expr = 0.)

    model.objective._expr = po_base.expr_coopr3._SumExpression()
    model.objective._expr._args = [item[1] for item in objective.variables]
    model.objective._expr._coef = [item[0] for item in objective.variables]
    model.objective._expr._const = objective.constant
