import pandas as pd
import pytest

from oemof import solph


def test_special():
    date_time_index = pd.date_range("1/1/2012", periods=5, freq="H")
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    bel = solph.Bus(label="electricityBus")
    flow1 = solph.Flow(nominal_value=100, my_factor=0.8)
    flow2 = solph.Flow(nominal_value=50)
    src1 = solph.Source(label="source1", outputs={bel: flow1})
    src2 = solph.Source(label="source2", outputs={bel: flow2})
    energysystem.add(bel, src1, src2)
    model = solph.Model(energysystem)
    flow_with_keyword = {
        (src1, bel): flow1,
    }
    solph.constraints.generic_integral_limit(
        model, "my_factor", flow_with_keyword, limit=777
    )


def test_something_else():
    date_time_index = pd.date_range("1/1/2012", periods=5, freq="H")
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    bel1 = solph.Bus(label="electricity1")
    bel2 = solph.Bus(label="electricity2")
    energysystem.add(bel1, bel2)
    energysystem.add(
        solph.Transformer(
            label="powerline_1_2",
            inputs={bel1: solph.Flow()},
            outputs={
                bel2: solph.Flow(investment=solph.Investment(ep_costs=20))
            },
        )
    )
    energysystem.add(
        solph.Transformer(
            label="powerline_2_1",
            inputs={bel2: solph.Flow()},
            outputs={
                bel1: solph.Flow(investment=solph.Investment(ep_costs=20))
            },
        )
    )
    om = solph.Model(energysystem)
    line12 = energysystem.groups["powerline_1_2"]
    line21 = energysystem.groups["powerline_2_1"]
    solph.constraints.equate_variables(
        om,
        om.InvestmentFlow.invest[line12, bel2],
        om.InvestmentFlow.invest[line21, bel1],
        name="my_name",
    )


def test_multiperiodinvestment_limit_error1():
    """Test errors getting thrown."""
    msg1 = "multiperiodinvestment_limit is only applicable"
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    om = solph.models.Model(es)
    with pytest.raises(ValueError, match=msg1):
        solph.constraints.multiperiodinvestment_limit(om, limit=10)


def test_multiperiodinvestment_limit_error2():
    """Test errors getting thrown."""
    msg2 = "multiperiodinvestment_limit_per_period is only applicable"
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    om = solph.models.Model(es)
    with pytest.raises(ValueError, match=msg2):
        solph.constraints.multiperiodinvestment_limit_per_period(om, limit=10)


def test_multiperiodinvestment_limit_error3():
    """Test errors getting thrown."""
    msg3 = "You have to provide an investment limit for each period!"
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    om = solph.models.MultiPeriodModel(es)
    with pytest.raises(ValueError, match=msg3):
        solph.constraints.multiperiodinvestment_limit_per_period(
            om, limit=None)


def test_integral_limit_error():
    """Test errors getting thrown"""
    msg = "has no attribute "
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    bel = solph.Bus()
    s1 = solph.Source(inputs={bel: solph.Flow()})
    es.add(bel, s1)
    om = solph.models.Model(es)
    with pytest.raises(AttributeError, match=msg):
        solph.constraints.generic_integral_limit(
            om, flows=om.flows, keyword="emission_factor", limit=100)


def test_integral_limit_error1():
    """Test errors getting thrown"""
    msg1 = "has no attribute "
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    bel = solph.Bus(multiperiod=True)
    s1 = solph.Source(inputs={bel: solph.Flow(multiperiod=True)})
    es.add(bel, s1)
    om = solph.models.MultiPeriodModel(es)
    with pytest.raises(AttributeError, match=msg1):
        solph.constraints.generic_periodical_integral_limit(
            om, flows=om.flows, keyword="emission_factor", limit=100)


def test_integral_limit_error2():
    """Test errors getting thrown"""
    msg2 = "generic_periodical_integral_limit is only applicable"
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    bel = solph.Bus()
    s1 = solph.Source(inputs={bel: solph.Flow(emission_factor=0.8)})
    es.add(bel, s1)
    om = solph.models.Model(es)
    with pytest.raises(ValueError, match=msg2):
        solph.constraints.generic_periodical_integral_limit(
            om, keyword="emission_factor", limit=100)


def test_integral_limit_error3():
    """Test errors getting thrown"""
    msg3 = "You have to provide a limit for each period!"
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")
    es = solph.EnergySystem(timeindex=date_time_index)
    bel = solph.Bus(multiperiod=True)
    s1 = solph.Source(inputs={bel: solph.Flow(emission_factor=0.8,
                                              multiperiod=True)})
    es.add(bel, s1)
    om = solph.models.MultiPeriodModel(es)
    with pytest.raises(ValueError, match=msg3):
        solph.constraints.generic_periodical_integral_limit(
            om, keyword="emission_factor", limit=None)
