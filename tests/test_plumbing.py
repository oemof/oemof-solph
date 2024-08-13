# -*- coding: utf-8 -

"""Testing the class NonConvex.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""
import numpy as np
import pytest

from oemof.solph._plumbing import _FakeSequence
from oemof.solph._plumbing import sequence


def test_fake_sequence():
    seq0 = _FakeSequence(42)
    assert seq0[0] == 42
    assert seq0.size is None

    assert seq0[10] == 42
    assert seq0.size is None

    assert seq0.max() == 42
    assert seq0.min() == 42
    assert seq0.value == 42
    assert seq0.sum() == np.inf

    assert str(seq0) == "[42, 42, ..., 42]"

    with pytest.raises(TypeError):
        seq0.to_numpy()
    assert (seq0.to_numpy(length=5) == np.array(5 * [42])).all()

    with pytest.raises(TypeError):
        len(seq0)

    seq0.size = 2
    assert seq0.size == 2
    assert len(seq0) == 2

    assert seq0.max() == 42
    assert seq0.min() == 42
    assert seq0.value == 42
    assert seq0.sum() == 84

    assert str(seq0) == "[42, 42]"

    assert (seq0.to_numpy() == np.array(2 * [42])).all()
    assert (seq0.to_numpy(length=5) == np.array(5 * [42])).all()


def test_sequence():
    seq0 = sequence(0)
    assert isinstance(seq0, _FakeSequence)
    assert seq0.value == 0
    assert seq0.size is None

    seq13 = sequence([1, 3])
    assert isinstance(seq13, np.ndarray)
    assert (seq13 == np.array([1, 3])).all()

    seq_ab = sequence("ab")
    assert isinstance(seq_ab, str)
    assert seq_ab == "ab"
