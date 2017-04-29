from collections import UserDict, UserList
from itertools import groupby
from ..solph.network import Storage
from ..solph.options import Investment


def result_dict(model):
    """ Returns a nested dictionary of the results of an optimization
    model.

    The dictionary is keyed by the :class:`Entities
    <oemof.core.network.Entity>` of the optimization model, that is
    :meth:`om.results()[s][t] <OptimizationModel.results>`
    holds the time series representing values attached to the edge (i.e.
    the flow) from `s` to `t`, where `s` and `t` are instances of
    :class:`Entity <oemof.core.network.Entity>`.

    Time series belonging only to one object, like e.g. shadow prices of
    commodities on a certain :class:`Bus
    <oemof.core.network.entities.Bus>`, dispatch values of a
    :class:`DispatchSource
    <oemof.core.network.entities.components.sources.DispatchSource>` or
    storage values of a
    :class:`Storage
    <oemof.core.network.entities.components.transformers.Storage>` are
    treated as belonging to an edge looping from the object to itself.
    This means they can be accessed via
    :meth:`om.results()[object][object] <OptimizationModel.results>`.

    Other result from the optimization model can be accessed like
    attributes of the flow, e.g. the invest variable for capacity
    of the storage 'stor' can be accessed like:

    :attr:`om.results()[stor][stor].invest` attribute

    For the investment flow of a 'transformer' trsf to the bus 'bel' this
    can be accessed with:

    :attr:`om.results()[trsf][bel].invest` attribute

    The value of the objective function is stored under the
    :attr:`om.results().objective` attribute.

    Note that the optimization model has to be solved prior to invoking
    this method.
    """
   # TODO: Make the results dictionary a proper object?
    result = UserDict()
    result.objective = model.objective()
    investment = UserDict()
    for i, o in model.flows:

        result[i] = result.get(i, UserDict())
        result[i][o] = UserList([model.flow[i, o, p, t].value
                                 for p, t in model.TIMEINDEX])

        if isinstance(i, Storage):
            if i.investment is None:
                result[i][i] = UserList(
                    [model.Storage.capacity[i, t].value
                     for t in model.TIMESTEPS])
            else:
                result[i][i] = UserList(
                    [model.InvestmentStorage.capacity[i, t].value
                     for t in model.TIMESTEPS])

        if isinstance(model.flows[i, o].investment, Investment):
            setattr(result[i][o], 'invest',
                    model.InvestmentFlow.invest[i, o].value)
            investment[(i, o)] = model.InvestmentFlow.invest[i, o].value
            if isinstance(i, Storage):
                setattr(result[i][i], 'invest',
                        model.InvestmentStorage.invest[i].value)
                investment[(i, i)] = model.InvestmentStorage.invest[i].value
    # add results of dual variables for balanced buses
    if hasattr(model, "dual"):
        # grouped = [(b1, [(b1, 0), (b1, 1)]), (b2, [(b2, 0), (b2, 1)])]
        #import pdb; pdb.set_trace()
        grouped = groupby(sorted(model.Bus.balance.iterkeys()),
                          lambda pair: pair[0])

        for bus, timesteps in grouped:
            result[bus] = result.get(bus, UserDict())
            result[bus][bus] = [model.dual[model.Bus.balance[bus, a, t]]
                                for _, a, t in timesteps]

    result.investment = investment

        return result

    return result
