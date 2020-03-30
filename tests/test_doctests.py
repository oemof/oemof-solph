import doctest

from nose import main
from nose.suite import LazySuite

from oemof.solph import components
from oemof.solph import constraints
from oemof.solph import custom
from oemof.solph import network
from oemof.solph import plumbing


def run_my_tests():
    """Collect doctest and integrate them in nose's test run."""
    modules = [components, constraints, custom, network, plumbing]
    suite = LazySuite([doctest.DocTestSuite(x) for x in modules])
    main(suite=suite)
