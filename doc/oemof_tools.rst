.. _oemof_tools_label:

~~~~~~~~~~~~~~~~~~~~~~
oemof-tools
~~~~~~~~~~~~~~~~~~~~~~

The oemof tools package contains little helpers to create your own application. You can use a configuration file in the ini-format to define computer specific parameters such as paths, addresses etc.. Furthermore a logging module helps you creating log files for your application.

.. contents:: List of oemof tools
    :depth: 1
    :local:
    :backlinks: top

Economics
---------

Calculate the annuity. See the API-doc of :py:func:`~oemof.tools.economics.annuity` for all details.


Helpers
-------

Excess oemof's default path. See the API-doc of :py:mod:`~oemof.tools.helpers` for all details.


Logger
-------

The main purpose of this function is to provide a logger with well set default values but with the opportunity to change the most important parameters if you know what you want after a while. This is what most new users (or users who do not want to care about loggers) need.
If you are an advanced user with your own ideas it might be easier to copy the whole function to your application and adapt it to your own wishes.

.. code-block:: python

    define_logging(logpath=None, logfile='oemof.log', file_format=None,
                   screen_format=None, file_datefmt=None, screen_datefmt=None,
                   screen_level=logging.INFO, file_level=logging.DEBUG,
                   log_version=True, log_path=True, timed_rotating=None):

By default down to INFO all messages are written on the screen and down to DEBUG all messages are written in the file. The file is placed in $HOME/.oemof/log_files as oemof.log. But you can easily pass your own path and your own filename. You can also change the logging level (screen/file) by changing the screen_level or the file_level to logging.DEBUG, logging.INFO, logging.WARNING.... . You can stop the logger from logging the oemof version or commit with *log_version=False* and the path of the file with *log_path=False*. Furthermore, you can change the format on the screen and in the file according to the python logging documentation. You can also change the used time format according to this documentation.

.. code-block:: python

    file_format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    file_datefmt = "%x - %X"
    screen_format = "%(asctime)s-%(levelname)s-%(message)s"
    screen_datefmt = "%H:%M:%S"

You can also change the behaviour of the file handling (TimedRotatingFileHandler) by passing a dictionary with your own options (timed_rotating).

See the API-doc of :py:func:`~oemof.tools.logger.define_logging` for all details.
