from nose.tools import ok_, eq_

import pandas as pd
import logging
import filecmp
import os.path as ospath

from oemof.core.network.entities.components import transformers as transformer
from oemof.solph import predefined_objectives as predefined_objectives
from oemof.core import energy_system as es
from oemof.core.network import Entity
from oemof.core.network.entities import Bus
from oemof.solph import optimization_model as om
from oemof.core.network.entities.components import sources as source


class EnergySystem_Tests:

    @classmethod
    def setUpClass(self):
        time_index = pd.date_range('1/1/2012', periods=5, freq='H')

        self.simulation = es.Simulation(timesteps=range(len(time_index)))

    def test_entity_registration(self):
        logging.info(Entity.registry)
#        ok_(Entity.registry is None)
        ensys = es.EnergySystem()
        eq_(Entity.registry, ensys)
        bus = Bus(uid='bus-uid', type='bus-type')
        eq_(ensys.entities[0], bus)
        bus2 = Bus(uid='bus-uid2', type='bus-type')
        transformer.Simple(uid='pp_gas', inputs=[bus], outputs=[bus2])
        ok_(isinstance(ensys.entities[2], transformer.Simple))
        ensys.simulation = self.simulation
        ok_(len(ensys.simulation.timesteps) == 5)


class Constraint_Tests:

    @classmethod
    def setUpClass(self):

        self.time_index = pd.date_range('1/1/2012', periods=3, freq='H')

        self.sim = es.Simulation(
            timesteps=range(len(self.time_index)), solver='glpk',
            objective_options={
                'function': predefined_objectives.minimize_cost})

        self.energysystem = es.EnergySystem(time_idx=self.time_index,
                                            simulation=self.sim)

    def compare_lp_files(self, energysystem, filename):
        self.opt_model = om.OptimizationModel(energysystem=energysystem)
        self.opt_model.write_lp_file(
            path=ospath.join("tests", "lp_files"), filename="tmp.lp")
        logging.info("Comparing with file: {0}".format(filename))
        ok_(filecmp.cmp(ospath.join("tests", "lp_files", "tmp.lp"),
                        ospath.join("tests", "lp_files", filename)))

    def test_Transformer_Simple(self):
        "Test transformer.Simple with and without investment."
        self.energysystem.entities = []

        bgas = Bus(uid="bgas",
                   type="gas",
                   price=70,
                   balanced=True,
                   excess=False)

        # create electricity bus
        bel = Bus(uid="bel",
                  type="el",
                  excess=True)

        transformer.Simple(
            uid='pp_gas',
            inputs=[bgas],
            outputs=[bel],
            opex_var=50,
            out_max=[10e10],
            eta=[0.58])

        self.compare_lp_files(self.energysystem, "transformer_simp.lp")

        transformer.Simple.optimization_options.update({'investment': True})

        del self.energysystem.entities[-1]

        transformer.Simple(
            uid='pp_gas',
            inputs=[bgas],
            outputs=[bel],
            opex_var=50,
            out_max=[10e10],
            eta=[0.58])

        self.compare_lp_files(self.energysystem, "transformer_simp_invest.lp")

    def test_source_fixed(self):
        self.energysystem.entities = []

        # create electricity bus
        bel = Bus(uid="bel",
                  type="el",
                  excess=True)

        source.FixedSource(uid="wind",
                           outputs=[bel],
                           val=[50, 80, 30],
                           out_max=[1000000],
                           add_out_limit=0,
                           capex=1000,
                           opex_fix=20,
                           lifetime=25,
                           crf=0.08)

        self.compare_lp_files(self.energysystem, "source_fixed.lp")

        source.FixedSource.optimization_options.update({'investment': True})

        del self.energysystem.entities[-1]

        source.FixedSource(uid="wind",
                           outputs=[bel],
                           val=[50, 80, 30],
                           out_max=[1000000],
                           add_out_limit=0,
                           capex=1000,
                           opex_fix=20,
                           lifetime=25,
                           crf=0.08)

        self.compare_lp_files(self.energysystem, "source_fixed_invest.lp")
