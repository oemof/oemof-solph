# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/test_solph_network_classes.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

from oemof import solph
from nose.tools import assert_raises, eq_, ok_


def test_transformer_class():
    transf = solph.Transformer()
    ok_(isinstance(transf.conversion_factors, dict))
    eq_(len(transf.conversion_factors.keys()), 0)
    bus = solph.Bus()
    transf = solph.Transformer(inputs={bus: solph.Flow()})
    eq_(transf.conversion_factors[bus][2], 1)
    transf = solph.Transformer(inputs={bus: solph.Flow()},
                               conversion_factors={bus: 2})
    eq_(transf.conversion_factors[bus][6], 2)
    transf = solph.Transformer(inputs={bus: solph.Flow()},
                               conversion_factors={bus: [2]})
    eq_(len(transf.conversion_factors[bus]), 1)
    with assert_raises(IndexError):
        eq_(transf.conversion_factors[bus][6], 2)


def test_flow_classes():
    with assert_raises(ValueError):
        solph.Flow(fixed=True)
    with assert_raises(ValueError):
        solph.Flow(investment=solph.Investment(), nominal_value=4)
    with assert_raises(ValueError):
        solph.Flow(investment=solph.Investment(), nonconvex=solph.NonConvex())
    with assert_raises(AttributeError):
        solph.Flow(fixed_costs=34)
