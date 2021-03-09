# -*- coding: utf-8 -*-

"""Classes used to model energy supply systems within solph.

Classes are derived from oemof core network classes and adapted for specific
optimization tasks. An energy system is modelled as a graph/network of nodes
with very specific constraints on which types of nodes are allowed to be
connected.

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Simon Hilpert
SPDX-FileCopyrightText: Cord Kaldemeyer
SPDX-FileCopyrightText: Stephan Günther
SPDX-FileCopyrightText: Birgit Schachler

SPDX-License-Identifier: MIT

"""

from oemof.network import network as on

from oemof.solph import blocks
from oemof.solph.plumbing import sequence

from ._helpers import check_node_object_for_missing_attribute


class Transformer(on.Transformer):
    """A linear Transformer object with n inputs and n outputs.

    Parameters
    ----------
    conversion_factors : dict
        Dictionary containing conversion factors for conversion of each flow.
        Keys are the connected bus objects.
        The dictionary values can either be a scalar or an iterable with length
        of time horizon for simulation.

    Examples
    --------
    Defining an linear transformer:

    >>> from oemof import solph
    >>> bgas = solph.Bus(label='natural_gas')
    >>> bcoal = solph.Bus(label='hard_coal')
    >>> bel = solph.Bus(label='electricity')
    >>> bheat = solph.Bus(label='heat')

    >>> trsf = solph.Transformer(
    ...    label='pp_gas_1',
    ...    inputs={bgas: solph.Flow(), bcoal: solph.Flow()},
    ...    outputs={bel: solph.Flow(), bheat: solph.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5,
    ...                        bgas: 0.8, bcoal: 0.2})
    >>> print(sorted([x[1][5] for x in trsf.conversion_factors.items()]))
    [0.2, 0.3, 0.5, 0.8]

    >>> type(trsf)
    <class 'oemof.solph.network.transformer.Transformer'>

    >>> sorted([str(i) for i in trsf.inputs])
    ['hard_coal', 'natural_gas']

    >>> trsf_new = solph.Transformer(
    ...    label='pp_gas_2',
    ...    inputs={bgas: solph.Flow()},
    ...    outputs={bel: solph.Flow(), bheat: solph.Flow()},
    ...    conversion_factors={bel: 0.3, bheat: 0.5})
    >>> trsf_new.conversion_factors[bgas][3]
    1

    Notes
    -----
    The following sets, variables, constraints and objective parts are created
     * :py:class:`~oemof.solph.blocks.transformer.Transformer`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        check_node_object_for_missing_attribute(self, "inputs")
        check_node_object_for_missing_attribute(self, "outputs")

        self.conversion_factors = {
            k: sequence(v)
            for k, v in kwargs.get("conversion_factors", {}).items()
        }

        missing_conversion_factor_keys = (
            set(self.outputs) | set(self.inputs)
        ) - set(self.conversion_factors)

        for cf in missing_conversion_factor_keys:
            self.conversion_factors[cf] = sequence(1)

    def constraint_group(self):
        return blocks.Transformer
