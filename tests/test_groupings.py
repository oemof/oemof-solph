""" Specific tests for the `oemof.groupings` module.

Most parts of the `groupings` module are tested via other tests, but certain
code paths don't get covered by those, which is what this module is for.
"""

from nose.tools import assert_raises

from oemof.groupings import Grouping


def test_initialization_argument_checks():
    """ `Grouping` constructor should raise `TypeError` on bad arguments.
    """

    message = "\n`Grouping` constructor did not check mandatory arguments."
    with assert_raises(TypeError, msg=message):
        g = Grouping()

    message = "\n`Grouping` constructor did not check conflicting arguments."
    with assert_raises(TypeError, msg=message):
        g = Grouping(key=lambda x: x, constant_key='key')

