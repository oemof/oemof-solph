# -*- coding: utf-8 -*-
"""

@author: Simon Hilpert
"""

#Tools to override slow Pyomo problem building



from pyomo.environ import Constraint
from pyomo.environ import Var

import pyomo


def l_constraint(model, name, constraints, *args):
    r"""A replacement for pyomo's Constraint that quickly builds linear
    constraints.

    Instead of:
    model.constraint_name = Constraint(index1,index2,...,rule=f)

    Call:
    l_constraint(model, constraint_name, constraints, index1, index2,...)

    This is a copy of the code from the python module pypsa. Thanks to
    Tom Brown / Jonas Hoersch for implementing it!

    Parameters
    ----------

    model : pyomo.ConcreteModel() / SimpleBlock() instance
        pyomo model or block with constructed components
    name : string
       Name of constraint to be constructed
    constraints: dict
        Constraints is a dictionary of constraints of the form:

        constraints[i] = [[(coeff1, var1), (coeff2, var2),...], sense,
                          constant_term]

        sense is one of "==","<=",">=".

        constant_term is constant rhs of equation

        I.e. variable coefficients are stored as a list of tuples.

    \*args :
       arguments passed to the pyomo.Constraint() class.


    """

    setattr(model, name, Constraint(*args, noruleinit=True))

    v = getattr(model, name)

    for i in v._index:
        c = constraints[i]
        v._data[i] = pyomo.core.base.constraint._GeneralConstraintData(None, v)
        v._data[i]._body = pyomo.core.base.expr_coopr3._SumExpression()
        v._data[i]._body._args = [item[1] for item in c[0]]
        v._data[i]._body._coef = [item[0] for item in c[0]]
        v._data[i]._body._const = 0.
        if c[1] == "==":
            v._data[i]._equality = True
            v._data[i]._lower = pyomo.core.base.numvalue.NumericConstant(c[2])
            v._data[i]._upper = pyomo.core.base.numvalue.NumericConstant(c[2])
        elif c[1] == "<=":
            v._data[i]._equality = False
            v._data[i]._lower = None
            v._data[i]._upper = pyomo.core.base.numvalue.NumericConstant(c[2])
        elif c[1] == ">=":
            v._data[i]._equality = False
            v._data[i]._lower = pyomo.core.base.numvalue.NumericConstant(c[2])
            v._data[i]._upper = None
    #v.construct()


def mutate_variable(var=None, value=None, bounds=(0, None), fix=False,
                    index=None):
    r""" Mutates existing pyomo variable, could be used to extend an emtpy
    Var() object or an existing indexed pyomo variable.
    It's possible to overwrite information for existing indices.

    Parameters
    ----------
    var : pyomo.core.base.var.Var() object
       pyomo variable to be extended
    value : list
       values of variable in list
    bounds : list
       lower and upper bounds of variable as tuples in list
    index : type of var._index elements (most likely tuple)
       list of indices for extension (Warning: if existing indices are used,
       data for for these indices will be overwritten.)
    fix : list
       list with boolean elements, if true, variable value is fixed, i.e.
       converted to parameter in opt-problem

    Example
    -------
    extend_variable(om.w, value=[10], bounds=[(0,10)], fix=[True],
                    index=[('bel','sink',155)])
    """

    bounds = dict(zip(index, bounds))
    value = dict(zip(index, value))
    fix = dict(zip(index, fix))

    for i in index:
        var._data[i] = pyomo.core.base.var._VarData(var)
        var._data[i].value = value[i]
        var._data[i].setlb(bounds[i][0])
        var._data[i].setub(bounds[i][1])

        if fix[i]:
            var._data[i].fix()
