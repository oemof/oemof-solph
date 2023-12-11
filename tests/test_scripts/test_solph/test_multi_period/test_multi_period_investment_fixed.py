from test_investment_model import set_up_multi_period_investment_model


def test_multi_period_investment_fixed(solver="cbc"):
    """test fixing investments in a repeated solve"""
    for approach in ["oemof", "DLR", "DIW"]:
        om = set_up_multi_period_investment_model(approach)
        om.receive_duals()
        om.solve(solver=solver)

        assert om.solver_results is not None
        om.fix_investments()
        om.solve(solver=solver)
        for i, o in om.InvestmentFlowBlock.INVESTFLOWS:
            for p in om.PERIODS:
                assert om.InvestmentFlowBlock.invest[i, o, p].fixed
                assert om.InvestmentFlowBlock.total[i, o, p].fixed
                assert om.InvestmentFlowBlock.old[i, o, p].fixed
                assert om.InvestmentFlowBlock.old_end[i, o, p].fixed
                assert om.InvestmentFlowBlock.old_exo[i, o, p].fixed
