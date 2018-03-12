# -*- coding: utf-8 -

"""Regression tests.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/regression_tests.py

SPDX-License-Identifier: GPL-3.0-or-later
"""

import logging

from nose.tools import eq_, ok_
import unittest

import pandas as pd

from oemof.energy_system import EnergySystem as ES
from oemof.network import Bus
from oemof.solph import (Flow, Model as OM, Sink, Source as FS)
from oemof.solph.components import GenericStorage as Storage
import oemof


def test_version_metadata():
    ok_(oemof.__version__)


class TestSolphAndItsResults:
    def setup(self):
        logging.disable(logging.CRITICAL)

        self.failed = False

        tix = pd.period_range('1970-01-01', periods=1, freq='H')
        self.es = ES(timeindex=tix)

    # TODO: Fix this test so that it works with the new solph and can be
    #       re-enabled.
    @unittest.skip("'test_issue_74' will soon be fixed by @gnn.")
    def test_issue_74(self):
        Storage.optimization_options.update({'investment': True})
        bus = Bus(uid="bus")
        store = Storage(uid="store", inputs=[bus], outputs=[bus],
                        c_rate_out=0.1, c_rate_in=0.1)
        sink = Sink(uid="sink", inputs=[bus], val=[1])

        es = self.es
        om = OM(es)
        om.objective.set_value(-1)
        es.results = om.results()

        try:
            es.dump()
        except AttributeError as ae:
            self.failed = ae
        if self.failed:
            ok_(False,
                "EnergySystem#dump should not raise `AttributeError`: \n" +
                " Error message: " + str(self.failed))

    # TODO: Fix this test so that it works with the new solph and can be
    #       re-enabled.
    @unittest.skip("Result tests will soon be fixed by @gnn.")
    def test_bus_to_sink_outputs_in_results_dataframe(self):
        bus = Bus(uid="bus")
        source = FS(label="source", outputs={bus: Flow(
            nominal_value=1, actual_value=0.5, fixed=True)})
        sink = Sink(label="sink", inputs={bus: Flow(
            nominal_value=1)})

        es = self.es
        om = OM(es)
        es.results = om.results()
        es.results[bus][sink] = [0.7]
        rdf = RDF(energy_system=es)
        try:
            eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"), :
                        ].val[0],
                0.7,
                "Output from bus to sink does not have the correct value.")
        except KeyError:
            self.failed = True
        if self.failed:
            ok_(False,
                "Output from bus to sink does not appear in results dataframe.")

        es.results[bus][bus] = [-1]
        rdf = RDF(energy_system=es)
        try:
            eq_(rdf.loc[(slice(None), slice(None), slice(None), "sink"), :
                       ].val[0],
                0.7,
                "Output from bus to sink does not have the correct value.")
        except KeyError:
            self.failed = True
        if self.failed:
            ok_(False,
                "Output from bus (with duals) to sink " +
                "does not appear in results dataframe.")
