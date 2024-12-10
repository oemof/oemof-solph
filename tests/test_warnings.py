# -*- coding: utf-8 -

"""Test debugging warning.

This file is part of project oemof (github.com/oemof/oemof). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location oemof/tests/tool_tests.py

SPDX-License-Identifier: MIT
"""

import warnings

import pandas as pd
import pytest
from oemof.tools.debugging import SuspiciousUsageWarning

from oemof import solph


@pytest.fixture()
def warning_fixture():
    """Explicitly activate the warnings."""
    warnings.filterwarnings("always", category=SuspiciousUsageWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)

    # FutureWarning is i.e. emitted by network Entity registry
    warnings.simplefilter(action="ignore", category=FutureWarning)


def test_that_the_converter_warnings_actually_get_raised(warning_fixture):
    """Converter doesn't warn about potentially erroneous usage."""
    look_out = solph.Bus()
    msg = (
        "Attribute <inputs> is missing in Node <no input> of <class"
        " 'oemof.solph.components._converter.Converter'>."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.components.Converter(
            label="no input", outputs={look_out: "No inputs!"}
        )
        assert len(w) == 1
        assert msg in str(w[-1].message)
    msg = (
        "Attribute <outputs> is missing in Node <no output> of <class"
        " 'oemof.solph.components._converter.Converter'>."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.components.Converter(
            label="no output", inputs={look_out: "No outputs!"}
        )
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_storage_without_outputs(warning_fixture):
    """GenericStorage doesn't warn correctly about missing outputs."""
    look_out = solph.Bus()
    msg = (
        "Attribute <outputs> is missing in Node <storage without outputs>"
        " of <class 'oemof.solph.components._generic_storage.GenericStorage'>."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.components.GenericStorage(
            label="storage without outputs", inputs={look_out: "No outputs!"}
        )
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_storage_without_inputs(warning_fixture):
    """GenericStorage doesn't warn correctly about missing inputs."""
    look_out = solph.Bus()
    msg = (
        "Attribute <inputs> is missing in Node <storage without inputs>"
        " of <class 'oemof.solph.components._generic_storage.GenericStorage'>."
    )
    with warnings.catch_warnings(record=True) as w:
        solph.components.GenericStorage(
            label="storage without inputs", outputs={look_out: "No inputs!"}
        )
        assert len(w) == 1
        assert msg in str(w[-1].message)


def test_nonconvex_investment_without_maximum_raises_warning(warning_fixture):
    """
    <class 'solph.flows.Flow'> without specifying
    the maximum attribute of the <class 'solph.Investment'>
    """

    with pytest.raises(AttributeError):
        solph.flows.Flow(
            variable_costs=25,
            min=0.2,
            max=0.8,
            nominal_capacity=solph.Investment(
                ep_costs=500,  # no maximum is provided here
            ),
            nonconvex=solph.NonConvex(),
        )


def test_link_to_warn_about_not_matching_number_of_flows(warning_fixture):
    """Link warns about missing parameters and not matching number of flows."""

    msg = (
        "Component `Link` should have exactly "
        + "2 inputs, 2 outputs, and 2 "
        + "conversion factors connecting these. You are initializing "
        + "a `Link`without obeying this specification. "
        + "If this is intended and you know what you are doing you can "
        + "disable the SuspiciousUsageWarning globally."
    )

    with warnings.catch_warnings(record=True) as w:
        solph.components.Link(
            label="empty_link",
        )
        assert len(w) == 4
        # Check  number of raised warnings:
        # 1. empty inputs, 2. empty outputs 3. empty conversion_factors
        # 4. unmatched number of flows
        # Check warning for unmatched number of flows
        assert msg in str(w[-1].message)


def test_link_raise_key_error_in_Linkblock(warning_fixture):
    """Link raises KeyError if conversion factors don't match the connected
    busses."""

    date_time_index = pd.date_range("1/1/2012", periods=3, freq="h")
    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=True,
    )
    bel0 = solph.buses.Bus(label="el0")
    bel1 = solph.buses.Bus(label="el1")
    look_out = solph.buses.Bus(label="look_out")
    link = solph.components.Link(
        label="transshipment_link",
        inputs={
            bel0: solph.flows.Flow(nominal_capacity=4),
            bel1: solph.flows.Flow(nominal_capacity=2),
        },
        outputs={bel0: solph.flows.Flow(), look_out: solph.flows.Flow()},
        conversion_factors={(bel0, bel1): 0.8, (bel1, bel0): 0.7},
    )

    energysystem.add(bel0, bel1, link)

    msg = (
        "Error in constraint creation from: el0, to: el1, via: "
        "transshipment_link. Check if all connected buses match the "
        "conversion factors."
    )
    with pytest.raises(KeyError, match=msg):
        solph.Model(energysystem)
