import doctest

from nose import run
from nose.tools import eq_
from nose.suite import LazySuite

from oemof.solph import components
from oemof.solph import constraints
from oemof.solph import custom
from oemof.solph import network
from oemof.solph import plumbing


def test_doctests_in_components_module():
    """
    Doctest in components module failed. See nose protocol for more
    information.
    """
    module = components
    status = run(suite=LazySuite(doctest.DocTestSuite(module)))
    eq_((module.__name__, status), (module.__name__, True))


def test_doctests_in_constraints_module():
    """
    Doctest in constraints module failed. See nose protocol for more
    information.
    """
    module = constraints
    status = run(suite=LazySuite(doctest.DocTestSuite(module)))
    eq_((module.__name__, status), (module.__name__, True))


def test_doctests_in_custom_module():
    """
    Doctest in custom module failed. See nose protocol for more information.
    """
    module = custom
    status = run(suite=LazySuite(doctest.DocTestSuite(module)))
    eq_((module.__name__, status), (module.__name__, True))


def test_doctests_in_network_module():
    """
    Doctest in network module failed. See nose protocol for more information.
    """
    module = network
    status = run(suite=LazySuite(doctest.DocTestSuite(module)))
    eq_((module.__name__, status), (module.__name__, True))


def test_doctests_in_plumbing_module():
    """
    Doctest in plumbing module failed. See nose protocol for more information.
    """
    module = plumbing
    status = run(suite=LazySuite(doctest.DocTestSuite(module)))
    eq_((module.__name__, status), (module.__name__, True))
