from difflib import unified_diff
import logging
import os.path as ospath
import re

from nose.tools import eq_
import pandas as pd

from oemof.solph.network import Investment
from oemof.solph import OperationalModel

from oemof import energy_system as core_es
import oemof.solph as solph

from oemof.solph import (Bus, Source, Sink, Flow, LinearTransformer, Storage,
                         LinearN1Transformer, VariableFractionTransformer)
from oemof.tools import helpers

logging.disable(logging.INFO)


class Constraint_Tests:

    @classmethod
    def setup_class(self):
        self.objective_pattern = re.compile("^objective.*(?=s\.t\.)",
                                            re.DOTALL | re.MULTILINE)

        self.date_time_index = pd.date_range('1/1/2012', periods=3, freq='H')

        self.tmppath = helpers.extend_basic_path('tmp')
        logging.info(self.tmppath)

    def setup(self):
        self.energysystem = core_es.EnergySystem(groupings=solph.GROUPINGS,
                                                 timeindex=self.date_time_index)

    def compare_lp_files(self, filename, ignored=None):
        om = OperationalModel(self.energysystem,
                              timeindex=self.energysystem.timeindex)
        tmp_filename = filename.replace('.lp', '') + '_tmp.lp'
        new_filename = ospath.join(self.tmppath, tmp_filename)
        om.write(new_filename, io_options={'symbolic_solver_labels': True})
        logging.info("Comparing with file: {0}".format(filename))
        with open(ospath.join(self.tmppath, tmp_filename)) as generated_file:
            with open(ospath.join(ospath.dirname(ospath.realpath(__file__)),
                                  "lp_files",
                                  filename)) as expected_file:

                def chop_trailing_whitespace(lines):
                    return [re.sub("\s*$", '', l) for l in lines]

                def remove(pattern, lines):
                    if not pattern:
                        return lines
                    return re.subn(pattern, "",
                                   "\n".join(lines))[0].split("\n")

                expected = remove(ignored,
                                  chop_trailing_whitespace(
                                      expected_file.readlines()))
                generated = remove(ignored,
                                   chop_trailing_whitespace(
                                       generated_file.readlines()))
                eq_(generated, expected,
                    "Failed matching expected with generated lp file:\n" +
                    "\n".join(unified_diff(expected, generated,
                                           fromfile=ospath.relpath(
                                               expected_file.name),
                                           tofile=ospath.basename(
                                               generated_file.name),
                                           lineterm="")))

    def test_linear_transformer(self):
        """Constraint test of a LinearTransformer without Investment.
        """
        bgas = Bus(label='gas')

        bel = Bus(label='electricity')

        LinearTransformer(
            label='powerplantGas',
            inputs={bgas: Flow()},
            outputs={bel: Flow(nominal_value=10e10, variable_costs=50)},
            conversion_factors={bel: 0.58})

        self.compare_lp_files('linear_transformer.lp')

    def test_linear_transformer_invest(self):
        """Constraint test of a LinearTransformer with Investment.
        """

        bgas = Bus(label='gas')

        bel = Bus(label='electricity')

        LinearTransformer(
            label='powerplant_gas',
            inputs={bgas: Flow()},
            outputs={bel: Flow(variable_costs=50,
                               investment=Investment(maximum=1000,
                                                     ep_costs=20))
                     },
            conversion_factors={bel: 0.58})

        self.compare_lp_files('linear_transformer_invest.lp')

    def test_max_source_min_sink(self):
        """
        """
        bel = Bus(label='electricityBus')

        Source(label='wind', outputs={bel: Flow(nominal_value=54,
                                                max=(.85, .95, .61))})

        Sink(label='minDemand', inputs={bel: Flow(
            nominal_value=54, min=(.84, .94, .59), variable_costs=14)})

        self.compare_lp_files('max_source_min_sink.lp')

    def test_fixed_source_variable_sink(self):
        """Constraint test with a fixed source and a variable sink.
        """

        bel = Bus(label='electricityBus')

        Source(label='wind', outputs={bel: Flow(actual_value=[.43, .72, .29],
                                                nominal_value=10e5,
                                                fixed=True, fixed_costs=20)})

        Sink(label='excess', inputs={bel: Flow(variable_costs=40)})

        self.compare_lp_files('fixed_source_variable_sink.lp')

    def test_fixed_source_invest_sink(self):
        """ Wrong constraints for fixed source + invest sink w. `summed_max`.
        """

        bel = Bus(label='electricityBus')

        Source(label='wind', outputs={bel: Flow(actual_value=[12, 16, 14],
                                                nominal_value=1000000,
                                                fixed=True, fixed_costs=20)})

        Sink(label='excess', inputs={bel: Flow(
            summed_max=2.3, variable_costs=25, max=0.8,
            investment=Investment(ep_costs=500, maximum=10e5))})

        self.compare_lp_files('fixed_source_invest_sink.lp')

    def test_invest_source_fixed_sink(self):
        """Constraint test with a fixed sink and a dispatch invest source.
        """

        bel = Bus(label='electricityBus')

        Source(label='pv', outputs={bel: Flow(
            max=[45, 83, 65], fixed_costs=20, variable_costs=13,
            investment=Investment(ep_costs=123))})

        Sink(label='excess', inputs={bel: Flow(
            actual_value=[.5, .8, .3], nominal_value=10e4, fixed=True)})

        self.compare_lp_files('invest_source_fixed_sink.lp')

    def test_storage(self):
        """
        """
        bel = Bus(label='electricityBus')

        Storage(
            label='storage',
            inputs={bel: Flow(variable_costs=56)},
            outputs={bel: Flow(variable_costs=24)},
            nominal_capacity=10e4,
            capacity_loss=0.13,
            nominal_input_capacity_ratio=1/6,
            nominal_output_capacity_ratio=1/6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            fixed_costs=35)

        self.compare_lp_files('storage.lp')

    def test_storage_invest(self):
        """
        """
        bel = Bus(label='electricityBus')

        Storage(
            label='storage',
            inputs={bel: Flow(variable_costs=56)},
            outputs={bel: Flow(variable_costs=24)},
            nominal_capacity=None,
            capacity_loss=0.13,
            capacity_max=0.9,
            capacity_min=0.1,
            nominal_input_capacity_ratio=1 / 6,
            nominal_output_capacity_ratio=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            fixed_costs=35,
            investment=Investment(ep_costs=145, maximum=234))

        self.compare_lp_files('storage_invest.lp')

    def test_linear_n1transformer(self):
        """Constraint test of a LinearN1Transformer without Investment.
        """
        bgas = Bus(label='gasBus')
        bbms = Bus(label='biomassBus')
        bel = Bus(label='electricityBus')

        LinearN1Transformer(
            label='powerplantGasCoal',
            inputs={bbms: Flow(), bgas: Flow()},
            outputs={bel: Flow(nominal_value=10e10, variable_costs=50)},
            conversion_factors={bgas: 0.4, bbms: 0.1})

        self.compare_lp_files('linear_n1_transformer.lp')

    def test_linear_n1transformer_invest(self):
        """Constraint test of a LinearN1Transformer with Investment.
        """

        bgas = Bus(label='gasBus')
        bcoal = Bus(label='coalBus')
        bel = Bus(label='electricityBus')

        LinearN1Transformer(
            label='powerplant_gas_coal',
            inputs={bgas: Flow(), bcoal: Flow()},
            outputs={bel: Flow(variable_costs=50,
                               investment=Investment(maximum=1000,
                                                     ep_costs=20))
                     },
            conversion_factors={bgas: 0.58, bcoal: 0.2})

        self.compare_lp_files('linear_n1_transformer_invest.lp')

    def test_linear_transformer_chp(self):
        """Constraint test of a LinearTransformer without Investment
        (two outputs).
        """
        bgas = Bus(label='gasBus')
        bheat = Bus(label='heatBus')
        bel = Bus(label='electricityBus')

        LinearTransformer(
            label='CHPpowerplantGas',
            inputs={bgas: Flow(nominal_value=10e10, variable_costs=50)},
            outputs={bel: Flow(), bheat: Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5})

        self.compare_lp_files('linear_transformer_chp.lp')

    def test_linear_transformer_chp_invest(self):
        """Constraint test of a LinearTransformer with Investment (two outputs).
        """

        bgas = Bus(label='gasBus')
        bheat = Bus(label='heatBus')
        bel = Bus(label='electricityBus')

        LinearTransformer(
            label='chp_powerplant_gas',
            inputs={bgas: Flow(variable_costs=50,
                               investment=Investment(maximum=1000,
                                                     ep_costs=20))
                    },
            outputs={bel: Flow(), bheat: Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5})

        self.compare_lp_files('linear_transformer_chp_invest.lp')

    def test_variable_chp(self):
        """
        """
        bel = Bus(label='electricityBus')
        bth = Bus(label='heatBus')
        bgas = Bus(label='commodityBus')

        VariableFractionTransformer(
            label='variable_chp_gas',
            inputs={bgas: solph.Flow(nominal_value=100)},
            outputs={bel: solph.Flow(), bth: solph.Flow()},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_single_flow={bel: 0.5})

        self.compare_lp_files('variable_chp.lp')
