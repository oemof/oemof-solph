# -*- coding: utf-8 -

"""Testing the class NonConvex.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""
import pytest

from oemof.solph._plumbing import sequence


def test_sequence():
    seq0 = sequence(0)
    assert seq0[0] == 0
    assert len(seq0) == 1

    assert seq0[10] == 0
    assert len(seq0) == 11

    assert max(seq0) == 0

    seq10 = sequence(10)
    assert max(seq10) == 10

    assert seq10[0] == 10
    assert len(seq10) == 1

    assert seq10[10] == 10
    assert len(seq10) == 11

    seq12 = sequence([1, 3])
    assert max(seq12) == 3
    assert seq12[0] == 1
    assert seq12[1] == 3

    with pytest.raises(IndexError):
        _ = seq12[2]
