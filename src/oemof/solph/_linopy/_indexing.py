# -*- coding: utf-8 -*-

"""Helpers to build linopy expressions from label arrays.

Every linopy variable carries an integer label per element. A linear
expression is a pair of arrays (coefficients, labels) with a term
dimension ``_term``; a label of -1 means "no term". Building expressions
this way avoids Python loops over elements and the coordinate alignment
of xarray arithmetic, which matters when selections of the same variable
are combined.

SPDX-License-Identifier: MIT
"""

import numpy as np
import xarray as xr
from linopy.expressions import LinearExpression

TERM_DIM = "_term"


def expression(model, terms, dims, coords=None, const=None):
    """Build a LinearExpression from a list of terms.

    Parameters
    ----------
    model : linopy.Model
    terms : list of (labels, coeffs)
        `labels` is an integer array of variable labels (-1 = no term),
        `coeffs` a float array broadcastable to `labels`. All `labels`
        arrays must have the same shape, matching `dims`.
    dims : tuple of str
        Dimension names of the resulting expression.
    coords : dict, optional
        Coordinates for `dims`. Defaults to ranges.
    const : array-like, optional
        Constant part of the expression, broadcastable to the shape.

    Returns
    -------
    linopy.LinearExpression
    """
    if not terms:
        raise ValueError("An expression needs at least one term.")
    shape = np.shape(terms[0][0])
    labels = np.stack(
        [np.asarray(lab, dtype=np.int64) for lab, _ in terms], axis=-1
    )
    coeffs = np.stack(
        [np.broadcast_to(np.asarray(c, dtype=float), shape) for _, c in terms],
        axis=-1,
    )
    coeffs = np.where(labels >= 0, coeffs, np.nan)
    full_dims = tuple(dims) + (TERM_DIM,)
    if coords is None:
        coords = {d: np.arange(n) for d, n in zip(dims, shape)}
    data = {
        "coeffs": (full_dims, coeffs),
        "vars": (full_dims, labels),
    }
    if const is not None:
        data["const"] = (
            tuple(dims),
            np.broadcast_to(np.asarray(const, dtype=float), shape),
        )
    ds = xr.Dataset(data, coords={d: coords[d] for d in dims})
    return LinearExpression(ds, model)


def ragged(rows, width=None):
    """Pad a ragged list of (position, coefficient) rows.

    Parameters
    ----------
    rows : list of list of (int, float)
        One list of terms per row (e.g. per bus: the flow positions and
        their signs).
    width : int, optional
        Number of term columns; defaults to the longest row.

    Returns
    -------
    positions : numpy.ndarray of int, shape (rows, width)
        -1 where a row has fewer terms.
    coefficients : numpy.ndarray of float, shape (rows, width)
    """
    if width is None:
        width = max((len(r) for r in rows), default=0)
    positions = np.full((len(rows), max(width, 1)), -1, dtype=np.int64)
    coefficients = np.zeros((len(rows), max(width, 1)))
    for i, row in enumerate(rows):
        for k, (pos, coef) in enumerate(row):
            positions[i, k] = pos
            coefficients[i, k] = coef
    return positions, coefficients


def take(labels, positions):
    """Take labels along the first axis; position -1 gives label -1.

    `labels` has shape (entities, ...), `positions` any integer array.
    The result has shape positions.shape + labels.shape[1:].
    """
    positions = np.asarray(positions, dtype=np.int64)
    out = labels[np.maximum(positions, 0)]
    missing = positions < 0
    if missing.any():
        out = np.where(
            missing.reshape(missing.shape + (1,) * (out.ndim - missing.ndim)),
            -1,
            out,
        )
    return out


def ragged_sum(
    model,
    var_labels,
    rows,
    row_dim,
    row_coords=None,
    tail_dims=(),
    tail_coords=None,
):
    """Sum of selected entities of one variable per row.

    Parameters
    ----------
    var_labels : numpy.ndarray, shape (entities, *tail)
        Labels of the variable (e.g. the flow variable, (flow, timestep)).
    rows : list of list of (int, float or array)
        Per row the entity positions and their coefficients. A coefficient
        may be an array over the tail dimensions (e.g. per timestep).
    row_dim : str
        Name of the row dimension of the result.
    tail_dims : tuple of str
        Names of the remaining dimensions of `var_labels`.
    """
    width = max((len(r) for r in rows), default=0)
    tail_shape = var_labels.shape[1:]
    terms = []
    for k in range(max(width, 1)):
        pos = np.array(
            [r[k][0] if k < len(r) else -1 for r in rows], dtype=np.int64
        )
        coef = np.zeros((len(rows),) + tail_shape)
        for i, r in enumerate(rows):
            if k < len(r):
                coef[i] = np.broadcast_to(
                    np.asarray(r[k][1], dtype=float), tail_shape
                )
        terms.append((take(var_labels, pos), coef))
    coords = {}
    if row_coords is not None:
        coords[row_dim] = row_coords
    else:
        coords[row_dim] = np.arange(len(rows))
    for d, n in zip(tail_dims, tail_shape):
        coords[d] = (
            tail_coords[d]
            if tail_coords and d in tail_coords
            else np.arange(n)
        )
    return expression(model, terms, (row_dim,) + tuple(tail_dims), coords)
