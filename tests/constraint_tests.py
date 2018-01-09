# -*- coding: utf-8 -

"""Test the created constraints against approved constraints.
"""

__copyright__ = "oemof developer group"
__license__ = "GPLv3"

from difflib import unified_diff
import logging
import os.path as ospath
import re

from nose.tools import eq_, assert_raises
import pandas as pd

from oemof.network import Node
from oemof.tools import helpers
import oemof.solph as solph

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
        self.energysystem = solph.EnergySystem(groupings=solph.GROUPINGS,
                                               timeindex=self.date_time_index)
        Node.registry = self.energysystem

    def get_om(self):
        return solph.Model(self.energysystem,
                           timeindex=self.energysystem.timeindex)

    def compare_lp_files(self, filename, ignored=None, my_om=None):
        if my_om is None:
            om = self.get_om()
        else:
            om = my_om
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

                def normalize_to_positive_results(lines):
                    negative_result_indices = [n
                        for n, line in enumerate(lines)
                        if re.match("^= -", line)]
                    equation_start_indices = [
                        [n for n in reversed(range(0, nri))
                           if re.match('.*:$', lines[n])][0]+1
                        for nri in negative_result_indices]
                    for (start, end) in zip(
                            equation_start_indices,
                            negative_result_indices):
                        for n in range(start, end):
                            lines[n] = ('-'
                                if lines[n] and lines[n][0] == '+'
                                else '+' if lines[n]
                                         else lines[n]) + lines[n][1:]
                        lines[end] = '= ' + lines[end][3:]
                    return lines

                expected = normalize_to_positive_results(expected)
                generated = normalize_to_positive_results(generated)

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
        bgas = solph.Bus(label='gas')

        bel = solph.Bus(label='electricity')

        solph.Transformer(
            label='powerplantGas',
            inputs={bgas: solph.Flow()},
            outputs={bel: solph.Flow(nominal_value=10e10, variable_costs=50)},
            conversion_factors={bel: 0.58})

        self.compare_lp_files('linear_transformer.lp')

    def test_linear_transformer_invest(self):
        """Constraint test of a LinearTransformer with Investment.
        """

        bgas = solph.Bus(label='gas')

        bel = solph.Bus(label='electricity')

        solph.Transformer(
            label='powerplant_gas',
            inputs={bgas: solph.Flow()},
            outputs={bel: solph.Flow(variable_costs=50,
                                     investment=solph.Investment(maximum=1000,
                                                                 ep_costs=20))
                     },
            conversion_factors={bel: 0.58})

        self.compare_lp_files('linear_transformer_invest.lp')

    def test_max_source_min_sink(self):
        """
        """
        bel = solph.Bus(label='electricityBus')

        solph.Source(label='wind', outputs={
            bel: solph.Flow(nominal_value=54, max=(.85, .95, .61))})

        solph.Sink(label='minDemand', inputs={bel: solph.Flow(
            nominal_value=54, min=(.84, .94, .59), variable_costs=14)})

        self.compare_lp_files('max_source_min_sink.lp')

    def test_fixed_source_variable_sink(self):
        """Constraint test with a fixed source and a variable sink.
        """

        bel = solph.Bus(label='electricityBus')

        solph.Source(label='wind', outputs={bel: solph.Flow(
            actual_value=[.43, .72, .29], nominal_value=10e5, fixed=True)})

        solph.Sink(label='excess', inputs={bel: solph.Flow(variable_costs=40)})

        self.compare_lp_files('fixed_source_variable_sink.lp')

    def test_nominal_value_to_zero(self):
        """If the nominal value is set to zero nothing should happen.
        """
        bel = solph.Bus(label='electricityBus')

        solph.Source(label='s1', outputs={bel: solph.Flow(nominal_value=0)})
        self.compare_lp_files('nominal_value_to_zero.lp')

    def test_fixed_source_invest_sink(self):
        """ Wrong constraints for fixed source + invest sink w. `summed_max`.
        """

        bel = solph.Bus(label='electricityBus')

        solph.Source(label='wind', outputs={bel: solph.Flow(
            actual_value=[12, 16, 14], nominal_value=1000000, fixed=True)})

        solph.Sink(label='excess', inputs={bel: solph.Flow(
            summed_max=2.3, variable_costs=25, max=0.8,
            investment=solph.Investment(ep_costs=500, maximum=10e5))})

        self.compare_lp_files('fixed_source_invest_sink.lp')

    def test_invest_source_fixed_sink(self):
        """Constraint test with a fixed sink and a dispatch invest source.
        """

        bel = solph.Bus(label='electricityBus')

        solph.Source(label='pv', outputs={bel: solph.Flow(
            max=[45, 83, 65], variable_costs=13,
            investment=solph.Investment(ep_costs=123))})

        solph.Sink(label='excess', inputs={bel: solph.Flow(
            actual_value=[.5, .8, .3], nominal_value=10e4, fixed=True)})

        self.compare_lp_files('invest_source_fixed_sink.lp')

    def test_storage(self):
        """
        """
        bel = solph.Bus(label='electricityBus')

        solph.components.GenericStorage(
            label='storage',
            inputs={bel: solph.Flow(variable_costs=56)},
            outputs={bel: solph.Flow(variable_costs=24)},
            nominal_capacity=10e4,
            capacity_loss=0.13,
            nominal_input_capacity_ratio=1/6,
            nominal_output_capacity_ratio=1/6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86)

        self.compare_lp_files('storage.lp')

    def test_storage_invest(self):
        """
        """
        bel = solph.Bus(label='electricityBus')

        solph.components.GenericStorage(
            label='storage',
            inputs={bel: solph.Flow(variable_costs=56)},
            outputs={bel: solph.Flow(variable_costs=24)},
            nominal_capacity=None,
            capacity_loss=0.13,
            capacity_max=0.9,
            capacity_min=0.1,
            nominal_input_capacity_ratio=1 / 6,
            nominal_output_capacity_ratio=1 / 6,
            inflow_conversion_factor=0.97,
            outflow_conversion_factor=0.86,
            investment=solph.Investment(ep_costs=145, maximum=234))

        self.compare_lp_files('storage_invest.lp')

    def test_transformer(self):
        """Constraint test of a LinearN1Transformer without Investment.
        """
        bgas = solph.Bus(label='gasBus')
        bbms = solph.Bus(label='biomassBus')
        bel = solph.Bus(label='electricityBus')
        bth = solph.Bus(label='thermalBus')

        solph.Transformer(
            label='powerplantGasCoal',
            inputs={bbms: solph.Flow(), bgas: solph.Flow()},
            outputs={bel: solph.Flow(variable_costs=50),
                     bth: solph.Flow(nominal_value=5e10, variable_costs=20)},
            conversion_factors={bgas: 0.4, bbms: 0.1,
                                bel: 0.3, bth: 0.5})

        self.compare_lp_files('transformer.lp')

    def test_transformer_invest(self):
        """Constraint test of a LinearN1Transformer with Investment.
        """

        bgas = solph.Bus(label='gasBus')
        bcoal = solph.Bus(label='coalBus')
        bel = solph.Bus(label='electricityBus')
        bth = solph.Bus(label='thermalBus')

        solph.Transformer(
            label='powerplant_gas_coal',
            inputs={bgas: solph.Flow(), bcoal: solph.Flow()},
            outputs={bel: solph.Flow(variable_costs=50,
                                     investment=solph.Investment(maximum=1000,
                                                                 ep_costs=20)),
                     bth: solph.Flow(variable_costs=20)
                     },
            conversion_factors={bgas: 0.58, bcoal: 0.2,
                                bel: 0.3, bth: 0.5})

        self.compare_lp_files('transformer_invest.lp')

    def test_linear_transformer_chp(self):
        """Constraint test of a LinearTransformer without Investment (two outputs).
        """
        bgas = solph.Bus(label='gasBus')
        bheat = solph.Bus(label='heatBus')
        bel = solph.Bus(label='electricityBus')

        solph.Transformer(
            label='CHPpowerplantGas',
            inputs={bgas: solph.Flow(nominal_value=10e10, variable_costs=50)},
            outputs={bel: solph.Flow(), bheat: solph.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5})

        self.compare_lp_files('linear_transformer_chp.lp')

    def test_linear_transformer_chp_invest(self):
        """Constraint test of a LinearTransformer with Investment (two outputs).
        """

        bgas = solph.Bus(label='gasBus')
        bheat = solph.Bus(label='heatBus')
        bel = solph.Bus(label='electricityBus')

        solph.Transformer(
            label='chp_powerplant_gas',
            inputs={bgas: solph.Flow(variable_costs=50,
                                     investment=solph.Investment(maximum=1000,
                                                                 ep_costs=20))
                    },
            outputs={bel: solph.Flow(), bheat: solph.Flow()},
            conversion_factors={bel: 0.4, bheat: 0.5})

        self.compare_lp_files('linear_transformer_chp_invest.lp')

    def test_variable_chp(self):
        """
        """
        bel = solph.Bus(label='electricityBus')
        bth = solph.Bus(label='heatBus')
        bgas = solph.Bus(label='commodityBus')

        solph.components.ExtractionTurbineCHP(
            label='variable_chp_gas',
            inputs={bgas: solph.Flow(nominal_value=100)},
            outputs={bel: solph.Flow(), bth: solph.Flow()},
            conversion_factors={bel: 0.3, bth: 0.5},
            conversion_factor_full_condensation={bel: 0.5})

        self.compare_lp_files('variable_chp.lp')

    def test_emission_constraints(self):
        """
        """
        bel = solph.Bus(label='electricityBus')

        solph.Source(label='source1', outputs={bel: solph.Flow(
            nominal_value=100, emission=0.5)})
        solph.Source(label='source2', outputs={bel: solph.Flow(
            nominal_value=100, emission=0.8)})

        # Should be ignored because the emission attribute is not defined.
        solph.Source(label='source3', outputs={bel: solph.Flow(
            nominal_value=100)})

        om = self.get_om()

        solph.constraints.emission_limit(om, limit=777)

        self.compare_lp_files('emission_limit.lp', my_om=om)

    def test_flow_without_emission_for_emission_constraint(self):
        """
        """
        def define_emission_limit():
            bel = solph.Bus(label='electricityBus')
            solph.Source(label='source1', outputs={bel: solph.Flow(
                nominal_value=100, emission=0.8)})
            solph.Source(label='source2', outputs={bel: solph.Flow(
                nominal_value=100)})
            om = self.get_om()
            solph.constraints.emission_limit(om, om.flows, limit=777)
        assert_raises(ValueError, define_emission_limit)

    def test_flow_without_emission_for_emission_constraint_no_error(self):
        """
        """
        bel = solph.Bus(label='electricityBus')
        solph.Source(label='source1', outputs={bel: solph.Flow(
            nominal_value=100, emission=0.8)})
        solph.Source(label='source2', outputs={bel: solph.Flow(
            nominal_value=100)})
        om = self.get_om()
        solph.constraints.emission_limit(om, limit=777)

    def test_equate_variables_constraint(self):
        """Testing the equate_variables function in the constraint module.
        """
        bus1 = solph.Bus(label='Bus1')
        storage = solph.components.GenericStorage(
            label='storage',
            nominal_input_capacity_ratio=0.2,
            nominal_output_capacity_ratio=0.2,
            inputs={bus1: solph.Flow()},
            outputs={bus1: solph.Flow()},
            investment=solph.Investment(ep_costs=145))
        sink = solph.Sink(label='Sink', inputs={bus1: solph.Flow(
            investment=solph.Investment(ep_costs=500))})
        source = solph.Source(label='Source', outputs={bus1: solph.Flow(
            investment=solph.Investment(ep_costs=123))})
        om = self.get_om()
        solph.constraints.equate_variables(
            om, om.InvestmentFlow.invest[source, bus1],
            om.InvestmentFlow.invest[bus1, sink], 2)
        solph.constraints.equate_variables(
            om, om.InvestmentFlow.invest[source, bus1],
            om.GenericInvestmentStorageBlock.invest[storage])

        self.compare_lp_files('connect_investment.lp', my_om=om)

    def test_gradient(self):
        """
        """
        bel = solph.Bus(label='electricityBus')

        solph.Source(label='powerplant', outputs={bel: solph.Flow(
            nominal_value=999, variable_costs=23,
            positive_gradient={'ub': 0.03, 'costs': 7},
            negative_gradient={'ub': 0.05, 'costs': 8})})

        self.compare_lp_files('source_with_gradient.lp')

    def test_investment_limit(self):
        """Testing the investment_limit function in the constraint module.
        """
        bus1 = solph.Bus(label='Bus1')
        solph.components.GenericStorage(
            label='storage',
            nominal_input_capacity_ratio=0.2,
            nominal_output_capacity_ratio=0.2,
            inputs={bus1: solph.Flow()},
            outputs={bus1: solph.Flow()},
            investment=solph.Investment(ep_costs=145))
        solph.Source(label='Source', outputs={bus1: solph.Flow(
            investment=solph.Investment(ep_costs=123))})
        om = self.get_om()
        solph.constraints.investment_limit(om, limit=900)

        self.compare_lp_files('investment_limit.lp', my_om=om)