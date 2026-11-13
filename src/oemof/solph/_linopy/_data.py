# -*- coding: utf-8 -*-

"""Conversion of solph parameters to plain numpy arrays.

solph stores most parameters as sequences (numpy arrays or
:class:`~oemof.solph._plumbing._FakeSequence` for scalars). The linopy
builders work on dense arrays, which this module produces.

SPDX-License-Identifier: MIT
"""

import numpy as np

from oemof.solph._plumbing import _FakeSequence


def to_array(seq, length, name="parameter"):
    """Return `seq` as a float array of `length` values.

    Parameters
    ----------
    seq : sequence, _FakeSequence, scalar or None
        The solph parameter.
    length : int
        Number of values needed (e.g. the number of timesteps).
    name : str
        Used in the error message.

    Returns
    -------
    numpy.ndarray or None
        None if `seq` is None.

    Raises
    ------
    ValueError
        If `seq` has fewer than `length` values. Longer sequences are cut,
        as the Pyomo backend only reads the first `length` values.
    """
    if seq is None:
        return None
    if isinstance(seq, _FakeSequence):
        return np.full(length, float(seq.value))
    arr = np.asarray(seq, dtype=float)
    if arr.ndim == 0:
        return np.full(length, float(arr))
    if len(arr) < length:
        msg = f"{name} has {len(arr)} values, but {length} are needed."
        raise ValueError(msg)
    return arr[:length]


def stack(rows, length, fill=np.nan, name="parameter"):
    """Stack per-entity sequences into an array of shape (entities, length).

    Entries that are None are filled with `fill`.
    """
    out = np.full((len(rows), length), fill, dtype=float)
    for k, seq in enumerate(rows):
        arr = to_array(seq, length, name=name)
        if arr is not None:
            out[k] = arr
    return out


def per_timestep(seq, period_of_timestep, name="parameter"):
    """Expand a per-period sequence to timesteps.

    `period_of_timestep[t]` is the capacity period of timestep `t`.
    """
    n_periods = (
        int(period_of_timestep.max()) + 1 if period_of_timestep.size else 1
    )
    arr = to_array(seq, n_periods, name=name)
    if arr is None:
        return None
    return arr[period_of_timestep]
