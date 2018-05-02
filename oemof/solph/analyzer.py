
"""
This module uses the visitor pattern.
All visited elements either call a default function "analyze" or an
element-specific function "analyze_<element>". Each analyzer must contain
functions for every specified element. If function does not exist, again a
default function is called.
"""

from warnings import warn
from collections import OrderedDict
from oemof.network import Node


def init(results=None, param_results=None):
    Analysis(results, param_results)


def analyze(*args):
    Analysis().analyze(*args)


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
        def __init__(self, results, param_results):
            self.results = results
            self.param_results = param_results
            self.chain = OrderedDict()

        def clean(self):
            self.chain = OrderedDict()

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
        self.analysis.add_to_chain(self)
        self.result = {}
        self.__check_requirements()
        self.__check_dependencies()

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
            raise TypeError(
                'Dependencies are not shortnamed. Consider converting '
                'attribute "depends_on" into dict to support shortnaming '
                'dependencies.'
            )
        try:
            dep = list(self.depends_on.keys())[
                list(self.depends_on.values()).index(shortname)]
        except ValueError:
            raise ValueError(
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

    def __check_requirements(self):
        if self.requires is not None:
            for req in self.requires:
                if getattr(self.analysis, req) is None:
                    raise RequirementError(
                        'Analyzer requires "' + req + '" to perform. ' +
                        'Please initialize analyser with attribute "' + req +
                        '".'
                    )

    def __check_dependencies(self):
        if self.depends_on is not None:
            for dep in self.depends_on:
                if dep.__name__ not in self.analysis.chain:
                    raise DependencyError(
                        'Analyzer "' + self.__class__.__name__ +
                        '" depends on analyzer "' + dep + '". ' +
                        'Please initialize analyzer "' + dep + '" first.'
                    )

    def analyze(self, args):
        pass

    def __str__(self):
        return str(self.result)


class SequenceFlowSumAnalyzer(Analyzer):
    requires = ('results',)

    def analyze(self, *args):
        if self._arg_is_flow(args):
            flow = tuple(args)
            self.result[flow] = (
                self.analysis.results[flow]['sequences']['flow'].sum())


class NodeAnalyzer(Analyzer):
    requires = ('param_results',)
    depends_on = (SequenceFlowSumAnalyzer,)

    def analyze(self, *args):
        if self._arg_is_node(args):
            node = args[0]
            try:
                self.result[node] = (
                    self.analysis.param_results[(node, None)]['scalars']
                    ['conversion_factors_b_el'])
            except KeyError:
                return


class OpexAnalyzer(Analyzer):
    requires = ('param_results',)
    depends_on = {SequenceFlowSumAnalyzer: 'seq'}

    def analyze(self, *args):
        if (
                len(args) == 2 and
                isinstance(args[0], Node) and
                isinstance(args[1], Node)
        ):
            node = args[0]
            try:
                conv_factor = (
                    self.analysis.param_results[(node, None)]['scalars']
                    ['conversion_factors_b_el'])
            except KeyError:
                return

            try:
                flow = self._get_dep('seq')[args]
            except KeyError:
                return

            self.result[node] = flow * conv_factor
