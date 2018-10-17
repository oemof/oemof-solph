
"""
This module uses the visitor pattern.
All visited elements either call a default function "analyze" or an
element-specific function "analyze_<element>". Each analyzer must contain
functions for every specified element. If function does not exist, again a
default function is called.
"""

from warnings import warn
from collections import OrderedDict, abc, namedtuple
from oemof.network import Node, Bus
from oemof.outputlib import views


class RequirementError(Exception):
    pass


class DependencyError(Exception):
    pass


class FormerDependencyError(DependencyError):
    pass


class Analysis(object):
    def __init__(self, results, param_results, iterator=None):
        self.results = results
        self.param_results = param_results
        self.__iterator = (
            FlowNodeIterator if iterator is None else iterator)
        self.__later = []
        self.__chain = OrderedDict()
        self.__former_chain = OrderedDict()

    def clean(self):
        self.__chain = OrderedDict()
        self.__former_chain = OrderedDict()

    def check_iterator(self, analyzer):
        if analyzer.required_iterator is None:
            return
        if not issubclass(self.__iterator, analyzer.required_iterator):
            raise RequirementError(
                'Analyzer "' + analyzer.__class__.__name__ +
                '" requires iterator "' +
                analyzer.required_iterator.__name__ +
                '" to work correctly. Please initialize analysis object '
                'with iterator "' + analyzer.required_iterator.__name__ +
                '".'
            )

    def check_requirements(self, component):
        """
        Checks if requirements are fullfilled

        Function can be used by Analyzer and Iterator objects
        """
        if component.requires is not None:
            for req in component.requires:
                if getattr(self, req) is None:
                    raise RequirementError(
                        'Component "' + component.__class__.__name__ +
                        '" requires "' + req + '" to perform. Please '
                        'initialize it with attribute "' + req + '".'
                    )

    def check_dependencies(self, analyzer):
        error_str = (
            'Analyzer "{an}" depends on analyzer "{dep}". '
            'Please initialize analyzer "{dep}" first.'
        )

        def check_deps():
            for dep in dependencies:
                if dep.__name__ not in chain_keys:
                    raise DependencyError(
                        error_str.format(
                            an=analyzer.__class__.__name__,
                            dep=dep
                        )
                    )

        if analyzer.depends_on is not None:
            dependencies = analyzer.depends_on
            chain_keys = list(self.__former_chain) + list(self.__chain)
            check_deps()

        chain_keys = list(self.__former_chain)
        if analyzer.depends_on_former is not None:
            dependencies = analyzer.depends_on_former
            try:
                check_deps()
            except DependencyError:
                return False
        return True

    def add_analyzer(self, analyzer):
        added_to_chain = True
        if not isinstance(analyzer, Analyzer):
            raise TypeError('Analyzer has to be an instance of '
                            '"analyzer.Analyzer" or its subclass')
        if analyzer.__class__.__name__ in self.__chain:
            warn(
                'Analyzer "' + analyzer.__class__.__name__ +
                '" already added to analysis. '
                'Clear analysis if you want to create new analysis.'
            )
        self.check_requirements(analyzer)
        self.check_iterator(analyzer)
        no_dependecies = self.check_dependencies(analyzer)
        if no_dependecies:
            self.__chain[analyzer.__class__.__name__] = analyzer
            analyzer.analysis = self
        else:
            self.__later.append(analyzer)
            added_to_chain = False
        return added_to_chain

    def __analyze_chain(self):
        for analyzer in self.__chain.values():
            analyzer.init_analyzer()
        for element in self:
            for analyzer in self.__chain.values():
                analyzer.analyze(*element)

    def __prepare_next_chain(self):
        done = False
        if not self.__later:
            return True
        added_analyzer = False
        later = self.__later
        self.__later = []
        for i, analyzer in enumerate(later):
            result = self.add_analyzer(analyzer)
            if result:
                added_analyzer = True
        if not added_analyzer:
            raise FormerDependencyError(
                'Could not iterate over all Analyzers. '
                'Maybe some analyzers are missing for former dependencies? '
                'Analyzers that could not be performed are: ' +
                ','.join(map(lambda x: x.__class__.__name__, self.__later))
            )
        return done

    def analyze(self):
        while True:
            self.__analyze_chain()
            self.__store_results()
            if self.__prepare_next_chain():
                break

    def get_analyzer(self, analyzer):
        try:
            return self.__chain[analyzer.__name__]
        except KeyError:
            try:
                return self.__former_chain[analyzer.__name__]
            except KeyError:
                raise KeyError('Analyzer "' + analyzer.__name__ +
                               '" not found.')

    def __store_results(self):
        self.__former_chain.update(self.__chain)
        self.__chain = OrderedDict()

    def set_iterator(self, iterator):
        if not issubclass(iterator, Iterator):
            raise TypeError('Invalid iterator type')
        else:
            self.__iterator = iterator

    def __iter__(self):
        return self.__iterator(self)


class Iterator(abc.Iterator):
    """
    Iterator for Analysis (uses Iterator Pattern)
    """
    requires = None

    def __init__(self, analysis):
        analysis.check_requirements(self)
        self.items = None
        self.index = 0

    def __next__(self):
        try:
            result = self.items[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


class FlowNodeIterator(Iterator):
    def __init__(self, analysis):
        super(FlowNodeIterator, self).__init__(analysis)
        self.items = [
            node
            for node in analysis.param_results
            if node[1] is not None
        ] + [
            node
            for node in analysis.param_results
            if node[1] is None
        ]


class TupleIterator(Iterator):
    def __init__(self, analysis):
        super(TupleIterator, self).__init__(analysis)
        self.items = [
            node
            for node in analysis.param_results
        ]


class NodeIterator(Iterator):
    def __init__(self, analysis):
        super(NodeIterator, self).__init__(analysis)
        self.items = [
            node
            for node in analysis.param_results
            if node[1] is None
        ]


class Analyzer(object):
    requires = None
    required_iterator = None
    depends_on = None
    depends_on_former = None

    def __init__(self):
        self.analysis = None
        self.result = {}
        self.total = 0.0

    def init_analyzer(self):
        """This function is called after adding analyzer to analysis"""
        pass

    def _get_dep_result(self, analyzer):
        """
        Returns results of dependent analyzer.
        """
        return self.analysis.get_analyzer(analyzer).result

    def rsc(self, args):
        return self.analysis.results[args]['scalars']

    def rsq(self, args):
        return self.analysis.results[args]['sequences']

    def psc(self, args):
        return self.analysis.param_results[args]['scalars']

    def psq(self, args):
        return self.analysis.param_results[args]['sequences']

    @staticmethod
    def _arg_is_flow(args):
        return (
            len(args) == 2 and
            isinstance(args[0], Node) and
            isinstance(args[1], Node)
        )

    @staticmethod
    def _arg_is_node(args):
        return (
                len(args) == 2 and
                isinstance(args[0], Node) and
                args[1] is None
        )

    def analyze(self, *args):
        if self.analysis is None:
            raise AttributeError(
                'Analyzer is not connected to analysis object.'
                'Maybe you forgot to add analyzer to analysis?'
            )


class SequenceFlowSumAnalyzer(Analyzer):
    requires = ('results',)

    def analyze(self, *args):
        super(SequenceFlowSumAnalyzer, self).analyze(*args)
        try:
            rsq = self.rsq(args)
            result = rsq['flow'].sum()
        except KeyError:
            return
        self.result[args] = result
        self.total += result


class SizeAnalyzer(Analyzer):
    requires = ('results',)

    def analyze(self, *args):
        super(SizeAnalyzer, self).analyze(*args)
        try:
            rsc = self.rsc(args)
            result = rsc['invest']
        except KeyError:
            return
        self.result[args] = result
        self.total += result


class InvestAnalyzer(Analyzer):
    requires = ('results', 'param_results')
    depends_on = (SizeAnalyzer,)

    def analyze(self, *args):
        super(InvestAnalyzer, self).analyze(*args)
        seq_result = self._get_dep_result(SizeAnalyzer)
        try:
            psc = self.psc(args)
            size = seq_result[args]
            invest = psc['investment_ep_costs']
        except KeyError:
            return
        result = invest * size
        self.result[args] = result
        self.total += result


class VariableCostAnalyzer(Analyzer):
    requires = ('results', 'param_results')
    depends_on = (SequenceFlowSumAnalyzer,)

    def analyze(self, *args):
        super(VariableCostAnalyzer, self).analyze(*args)
        seq_result = self._get_dep_result(SequenceFlowSumAnalyzer)
        try:
            psc = self.psc(args)
            variable_cost = psc['variable_costs']
            flow_sum = seq_result[args]
        except KeyError:
            return
        result = variable_cost * flow_sum
        self.result[args] = result
        self.total += result


class FlowTypeAnalyzer(Analyzer):
    requires = ('results',)

    def analyze(self, *args):
        super(FlowTypeAnalyzer, self).analyze(*args)
        if self._arg_is_node(args):
            self.result[args] = views.get_flow_type(
                args[0], self.analysis.results)


class NodeBalanceAnalyzer(Analyzer):
    requires = ('results', 'param_results')
    required_iterator = FlowNodeIterator
    depends_on = (SequenceFlowSumAnalyzer, FlowTypeAnalyzer)

    node_type = Node

    def analyze(self, *args):
        super(NodeBalanceAnalyzer, self).analyze(*args)
        if not (isinstance(args[0], self.node_type) and args[1] is None):
            return

        seq_result = self._get_dep_result(SequenceFlowSumAnalyzer)
        ft_result = self._get_dep_result(FlowTypeAnalyzer)
        try:
            current_flow_types = ft_result[args]
        except KeyError:
            return
        self.result[args[0]] = {}
        f_types = (views.FlowType.Input, views.FlowType.Output)
        for i, ft in enumerate(f_types):
            self.result[args[0]][ft] = {}
            for flow in current_flow_types[ft]:
                try:
                    self.result[args[0]][ft][flow[i]] = seq_result[flow]
                except KeyError:
                    pass


class BusBalanceAnalyzer(NodeBalanceAnalyzer):
    node_type = Bus

    # TODO: Check if NodeBalanceAnalyzer already exists
    # If so, BusBalanceAnalyzer could simply filter results to


LCOEResult = namedtuple('LCOEResult', ['investment', 'variable_costs'])


class LCOEAnalyzer(Analyzer):
    depends_on = (
        SequenceFlowSumAnalyzer, VariableCostAnalyzer, InvestAnalyzer)
    depends_on_former = (NodeBalanceAnalyzer,)

    def __init__(self, load_sinks):
        super(LCOEAnalyzer, self).__init__()
        self.load_sinks = load_sinks
        self.total_load = 0.0

    def init_analyzer(self):
        """
        Initializes total load by iterating flows to all _load_sinks_

        Parameters
        ----------
        load_sinks: list-of-Node
            List of all loads which are relevant for calculating total load
        """
        seq_result = self._get_dep_result(SequenceFlowSumAnalyzer)
        nb_result = self._get_dep_result(NodeBalanceAnalyzer)
        for to_node in self.load_sinks:
            for from_node in nb_result[to_node]['input']:
                self.total_load += seq_result[(from_node, to_node)]

    def analyze(self, *args):
        super(LCOEAnalyzer, self).analyze(*args)
        vc_result = self._get_dep_result(VariableCostAnalyzer)
        inv_result = self._get_dep_result(InvestAnalyzer)

        error = False
        try:
            vc = vc_result[args]
        except KeyError:
            vc = 0.0
            error = True
        try:
            inv = inv_result[args]
        except KeyError:
            if error:
                return
            inv = 0.0

        result = LCOEResult(inv / self.total_load, vc / self.total_load)
        self.result[args] = result
        self.total += result.investment + result.variable_costs


class OperatingHoursAnalyzer(Analyzer):
    """
    Returns amount of operating hours
    """
    requires = ('results',)

    def analyze(self, *args):
        super(OperatingHoursAnalyzer, self).analyze(*args)
        try:
            rsq = self.rsq(args)
            result = (rsq['flow'] > 0).sum()
        except KeyError:
            return
        self.result[args] = result
        self.total += result


ProductionResult = namedtuple(
    'ProductionResult', ['sum', 'mean', 'max', 'min'])


class ProductionAnalyzer(Analyzer):
    """
    Returns power during operating hours
    """
    requires = ('results',)

    def analyze(self, *args):
        super(ProductionAnalyzer, self).analyze(*args)
        try:
            rsq = self.rsq(args)
            production = rsq['flow'][rsq['flow'] > 0]
        except KeyError:
            return
        result = ProductionResult(
            production.sum(),
            production.mean(),
            production.min(),
            production.max()
        )
        self.result[args] = result
        self.total += result.sum
