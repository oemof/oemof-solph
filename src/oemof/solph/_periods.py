"""
solph class defining periods for a multi-period model

SPDX-FileCopyrightText: Johannes Kochems

SPDX-License-Identifier: MIT

"""
import pandas as pd


class Period:
    """Periods for a multi-period optimization model

    Periods are defined on an annual basis.
    Thus, it is not (yet) allowed to consider sub-annual periods
    """

    def __init__(self, start=None, end=None):
        """Initialize a Period object

        Parameters
        ----------
        start : str
            String representation for the starting timestamp of a period
        end : str
            String representation for the last timestamp of a period
        """
        e1 = (
            "Please define a valid {} time.\n"
            "It has to be of type str and a valid date string representation."
        )
        if start is None or not isinstance(start, str):
            raise ValueError(e1.format("start"))
        if end is None or not isinstance(start, str):
            raise ValueError(e1.format("end"))

        e2 = (
            "You did not specify a valid date string representation which"
            " is needed for converting {} time to a pandas.Timestamp object.\n"
            "Please refer to the pandas date and time documentation."
        )
        try:
            self.start = pd.Timestamp(start)
        except ValueError:
            raise ValueError(e2.format("start"))
        try:
            self.end = pd.Timestamp(end)
        except ValueError:
            raise ValueError(e2.format("end"))

    def _extract_periods_length(self):
        """Extracts the periods length in full years"""
        return self.end.year - self.start.year + 1

    @property
    def periods_length(self):
        return self._extract_periods_length()
