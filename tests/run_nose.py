import os
import sys

try:
    import nose
except ImportError:
    raise ImportError("Please install nosetest to use this script.")


def nose_oemof():
    """You can just execute this function to run the oemof nosetests and
    doctests. Nosetests has to be installed.
    """
    testdir = os.path.join(os.path.dirname(__file__), os.path.pardir)
    argv = sys.argv[:]
    argv.insert(1, "--with-doctest")
    argv.insert(1, "--logging-clear-handlers")
    argv.insert(1, "-w{0}".format(testdir))
    nose.run(argv=argv)


if __name__ == "__main__":
    nose_oemof()
