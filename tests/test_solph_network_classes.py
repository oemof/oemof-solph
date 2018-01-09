# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

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
