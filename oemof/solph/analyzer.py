
"""
This module uses the visitor pattern.
All visited elements either call a default function "analyze" or an
element-specific function "analyze_<element>". Each analyzer must contain
functions for every specified element. If function does not exist, again a
default function is called.
"""

from warnings import warn
from collections import OrderedDict, abc
from oemof.network import Node
from oemof.outputlib import views


def init(results=None, param_results=None):
    Analysis(results, param_results)


def analyze():
    for element in Analysis():
        Analysis().analyze(*element)


def clean():
    Analysis().clean()


class RequirementError(Exception):
    pass


class DependencyError(Exception):
    pass


class Analysis(object):
    """
    Holds chain for all analyzers. Is implemented as singleton.
    """
    class __Analysis:
        def __init__(self, results, param_results, iterator=None):
            self.results = results
            self.param_results = param_results
            self.iterator = (
                TupleIterator if iterator is None else iterator)
            self.chain = OrderedDict()

        def clean(self):
            self.chain = OrderedDict()

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
            if analyzer.depends_on is not None:
                for dep in analyzer.depends_on:
                    if dep.__name__ not in self.chain:
                        raise DependencyError(
                            'Analyzer "' + analyzer.__class__.__name__ +
                            '" depends on analyzer "' + dep.__name__ + '". ' +
                            'Please initialize analyzer "' + dep.__name__ +
                            '" first.'
                        )

        def add_to_chain(self, analyzer):
            if analyzer.__class__.__name__ in self.chain:
                warn(
                    'Analyzer "' + analyzer.__class__.__name__ +
                    '" already added to analysis. '
                    'Clear analysis if you want to create new analysis.'
                )
            else:
                self.chain[analyzer.__class__.__name__] = analyzer

        def analyze(self, *args):
            for analyzer in self.chain.values():
                analyzer.analyze(*args)

        def __iter__(self):
            return self.iterator(self)

    singleton = None

    def __new__(cls, results=None, param_results=None):
        if not Analysis.singleton:
            Analysis.singleton = Analysis.__Analysis(results, param_results)
        return Analysis.singleton


class Analyzer(object):
    requires = None
    depends_on = None

    def __init__(self):
        self.analysis = Analysis()
        self.analysis.check_requirements(self)
        self.analysis.check_dependencies(self)
        self.analysis.add_to_chain(self)
        self.result = {}

    def _get_dep(self, shortname):
        """
        Returns results of dependent analyzer given its shortname.

        To work properly "depends_on" attribute of analyzer has to be a dict.

        Parameters
        ----------
        shortname: str
            Shortname of dependent analyzer

        Returns
        -------
        dict: Result dictionary of dependent analyzer
        """
        if not isinstance(self.depends_on, dict):
            raise DependencyError(
                'Dependencies are not shortnamed. Consider converting '
                'attribute "depends_on" into dict to support shortnaming '
                'dependencies.'
            )
        try:
            dep = list(self.depends_on.keys())[
                list(self.depends_on.values()).index(shortname)]
        except ValueError:
            raise DependencyError(
                'Dependency shortname "' + shortname +
                '" not found in analyzer "' + self.__class__.__name__ + '".')
        else:
            return self.analysis.chain[dep.__name__].result

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
        pass


class SequenceFlowSumAnalyzer(Analyzer):
    requires = ('results',)

    def analyze(self, *args):
        try:
            self.result[args] = (
                self.analysis.results[args]['sequences']['flow'].sum())
        except KeyError:
            return


class InvestAnalyzer(Analyzer):
    requires = ('results', 'param_results',)

    def analyze(self, *args):
        try:
            invest = (
                self.analysis.param_results[args]['scalars']
                ['investment_ep_costs']
            )
        except KeyError:
            return

        try:
            ep_costs = (
                self.analysis.results[args]['scalars']['invest'])
        except KeyError:
            return
        self.result[args] = invest * ep_costs


class FlowTypeAnalyzer(Analyzer):
    def analyze(self, *args):
        if self._arg_is_node(args):
            self.result[args] = views.get_flow_type(
                args[0], self.analysis.results)


class OpexAnalyzer(Analyzer):
    requires = ('param_results',)
    depends_on = {SequenceFlowSumAnalyzer: 'seq', FlowTypeAnalyzer: 'ft'}

    def analyze(self, *args):
        if not self._arg_is_node(args):
            return

        ft = self._get_dep('ft')
        try:
            conv_factor = (
                self.analysis.param_results[args]['scalars']
                ['conversion_factors_b_el1'])
        except KeyError:
            return

        try:
            flow = self._get_dep('seq')[args]
        except KeyError:
            return

        self.result[args] = flow * conv_factor


class Iterator(abc.Iterator):
    requires = None

    def __init__(self, analysis):
        analysis.check_requirements(self)
        self.index = 0

    def __next__(self):
        try:
            result = self.items[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return result


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
            node1
            for (node1, node2) in analysis.param_results
            if node2 is None
        ]
