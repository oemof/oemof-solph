# -*- coding: utf-8 -

"""Testing the class NonConvex.

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import numpy as np
import pandas as pd
import pytest

from oemof.solph._plumbing import Apply
from oemof.solph._plumbing import SequenceDict
from oemof.solph._plumbing import _FakeSequence
from oemof.solph._plumbing import sequence
from oemof.solph._plumbing import valid_sequence


def test_fake_sequence_access():
    seq = _FakeSequence(7)
    assert seq[0] == 7
    assert seq[10] == 7


def test_fake_sequence():
    seq = _FakeSequence(42.0)
    assert seq.max() == 42
    assert seq.min() == 42
    assert seq.value == 42

    assert str(seq) == "[42.0, 42.0, ..., 42.0]"


def test_fake_sequence_abs():
    seq = _FakeSequence(-5)
    seq5 = abs(seq)
    assert seq5.value == 5


def test_sequence():
    seq0 = sequence(0)
    assert isinstance(seq0, _FakeSequence)
    assert seq0.value == 0
    sequence(None) is None

    with pytest.raises(ValueError, match="Length mismatch"):
        _ = sequence([1, 3], length=3)
    seq13 = sequence([1, 3])
    assert isinstance(seq13, np.ndarray)
    assert (seq13 == np.array([1, 3])).all()

    with pytest.raises(ValueError, match="Length mismatch"):
        _ = sequence("ab", length=3)
    seq_ab = sequence("this_is_a_string")
    assert isinstance(seq_ab, np.ndarray)
    assert seq_ab == "this_is_a_string"


def test_fake_sequence_slice():
    seq = _FakeSequence(42)
    sliced = seq[2:5]
    assert isinstance(sliced, np.ndarray)
    assert sliced[0] == 42
    assert len(sliced) == 3

    sliced = seq[2:5:2]
    assert isinstance(sliced, np.ndarray)
    assert sliced[0] == 42
    assert len(sliced) == 1

    sliced = seq[2:6:2]
    assert isinstance(sliced, np.ndarray)
    assert sliced[0] == 42
    assert len(sliced) == 2

    sliced = seq[:5]
    assert isinstance(sliced, np.ndarray)
    assert sliced[0] == 42
    assert len(sliced) == 5

    sliced = seq[-8:-5]
    assert isinstance(sliced, np.ndarray)
    assert sliced[0] == 42
    assert len(sliced) == 3

    with pytest.raises(IndexError, match="_FakeSequence has every length."):
        _ = seq[1:-5]


def test_fake_sequence_float():
    seq = _FakeSequence(3.14)
    assert float(seq) == 3.14
    assert isinstance(float(seq), float)

    seq_int = _FakeSequence(42.0)
    assert float(seq_int) == 42.0


def test_sequence_from_fake_sequence_with_length():
    seq = _FakeSequence(42)
    result = sequence(seq, length=5)
    assert isinstance(result, np.ndarray)
    assert len(result) == 5
    assert (result == 42).all()

    # sequence without length
    result_no_len = sequence(seq)
    assert isinstance(result_no_len, _FakeSequence)
    assert result_no_len.value == 42


def test_fake_sequence_compare():
    seq0 = _FakeSequence(42.0)
    seq_lt = _FakeSequence(7)
    seq_gt = _FakeSequence(64)

    for other in [42, np.array([42, 42]), _FakeSequence(42)]:
        assert (seq_lt < other).all()
        assert (seq_lt <= other).all()
        assert (seq0 <= other).all()
        assert (seq0 == other).all()
        assert (seq0 >= other).all()
        assert (seq_gt >= other).all()
        assert (seq_gt > other).all()

        assert (seq_lt < other).any()
        assert (seq_lt <= other).any()
        assert (seq0 <= other).any()
        assert (seq0 == other).any()
        assert (seq0 >= other).any()
        assert (seq_gt >= other).any()
        assert (seq_gt > other).any()

        assert (other > seq_lt).all()
        assert (other >= seq_lt).all()
        assert (other >= seq0).all()
        assert (other == seq0).all()
        assert (other <= seq0).all()
        assert (other <= seq_gt).all()
        assert (other < seq_gt).all()

        assert (other > seq_lt).any()
        assert (other >= seq_lt).any()
        assert (other >= seq0).any()
        assert (other == seq0).any()
        assert (other <= seq0).any()
        assert (other <= seq_gt).any()
        assert (other < seq_gt).any()

    for other in [np.array([1, 42, 100])]:
        assert not (seq_lt < other).all()
        assert not (seq_lt <= other).all()
        assert not (seq0 <= other).all()
        assert not (seq0 == other).all()
        assert not (seq0 >= other).all()
        assert not (seq_gt >= other).all()
        assert not (seq_gt > other).all()

        assert (seq_lt < other).any()
        assert (seq_lt <= other).any()
        assert (seq0 <= other).any()
        assert (seq0 == other).any()
        assert (seq0 >= other).any()
        assert (seq_gt >= other).any()
        assert (seq_gt > other).any()

    other = _FakeSequence(42)
    assert other > seq_lt
    assert other >= seq_lt
    assert other >= seq0
    assert other == seq0
    assert other <= seq0
    assert other <= seq_gt
    assert other < seq_gt


def test_fake_sequence_addition():
    n1 = 12
    seq1_var = _FakeSequence(12)

    n2 = 8
    seq2_var = _FakeSequence(8)

    for s1 in [n1, seq1_var]:
        for s2 in [n2, seq2_var]:
            if isinstance(s1, _FakeSequence) or isinstance(s2, _FakeSequence):
                added = s1 + s2
                assert isinstance(added, _FakeSequence)
                assert added.value == 20

    array12 = np.array([1, 2])
    assert ((array12 + seq1_var) == np.array([13, 14])).all()
    assert ((seq1_var + array12) == np.array([13, 14])).all()


def test_fake_sequence_subtraction():
    n1 = 12
    seq1_var = _FakeSequence(12)

    n2 = 8
    seq2_var = _FakeSequence(8)

    for s1 in [n1, seq1_var]:
        for s2 in [n2, seq2_var]:
            if isinstance(s1, _FakeSequence) or isinstance(s2, _FakeSequence):
                difference = s1 - s2
                assert isinstance(difference, _FakeSequence)
                assert difference.value == 4

    array12 = np.array([1, 2])
    assert ((seq1_var - array12) == np.array([11, 10])).all()


def test_fake_sequence_multiplication_and_division():
    seq_mul = 2 * _FakeSequence(21.0)
    seq_rmul = _FakeSequence(2.0) * 21

    seq_div = _FakeSequence(84.0) / 2
    seq_rdiv = 84 / _FakeSequence(2)
    seq_imul = _FakeSequence(21.0)
    seq_imul *= 2
    seq_idiv = _FakeSequence(84)
    seq_idiv /= 2

    for seq in [seq_mul, seq_rmul, seq_div, seq_rdiv, seq_imul, seq_idiv]:
        assert seq == 42

    seq1 = _FakeSequence(42.0)
    seq2 = seq1 * np.array([1, 2])
    assert (seq2 == np.array([42, 84])).all()

    seq3 = np.array([1, 2]) * seq1
    assert (seq3 == np.array([42, 84])).all()


def test_sequence_dict():
    d0 = SequenceDict()
    d0["a"] = 5
    assert isinstance(d0["a"], _FakeSequence)
    assert d0["a"][0] == 5

    d0.update({"b": 12, "c": 13})
    assert isinstance(d0["a"], _FakeSequence)
    assert isinstance(d0["b"], _FakeSequence)
    assert isinstance(d0["c"], _FakeSequence)
    assert d0["a"][0] == 5
    assert d0["b"][0] == 12
    assert d0["c"][0] == 13

    d1 = SequenceDict({"b": [1, 2, 3], 3: 20})
    assert isinstance(d1["b"], np.ndarray)
    assert isinstance(d1[3], _FakeSequence)
    assert (d1["b"] == [1, 2, 3]).all()
    assert d1[3][0] == 20


def test_Apply_descriptor():
    class TestClass:
        x = Apply(sequence)
        y = Apply(converter=sequence, default="y")

        def __init__(self, x):
            self.x = x
            if x is not None:
                self.y = x

    i0 = TestClass(None)
    assert i0.x is None
    assert i0.y == "y"

    i1 = TestClass(1)
    assert i1.x[0] == 1
    assert i1.y[42] == 1

    i2 = TestClass([1, 2])
    assert (i2.x == [1, 2]).all()
    assert (i2.y == [1, 2]).all()


def test_using_Apply_to_convert_to_numeric():
    class TestClass:
        i = Apply(converter=int)
        f = Apply(converter=float)

        def __init__(self, x):
            self.i = x
            self.f = x

    i1 = TestClass(1)
    assert isinstance(i1.i, int)
    assert isinstance(i1.f, float)
    assert i1.i == 1
    assert i1.f == 1

    i2 = TestClass(2.0)
    assert isinstance(i2.i, int)
    assert isinstance(i2.f, float)
    assert i2.i == 2
    assert i2.f == 2


def test_dimension_is_too_high_to_create_a_sequence():
    df = pd.DataFrame({"epc": 5}, index=["a"])
    with pytest.raises(ValueError, match="Dimension too high"):
        sequence(df)
    n2 = [[4]]
    with pytest.raises(ValueError, match="Dimension too high"):
        sequence(n2)


def test_valid_sequence():
    np_array = np.array([0, 1, 2, 3, 4])
    assert valid_sequence(np_array, 5)

    with pytest.warns(FutureWarning, match="Sequence longer than needed"):
        valid_sequence(np_array, 4)

    # it's not that long
    with pytest.raises(ValueError):
        valid_sequence(np_array, 1337)

    fake_sequence = _FakeSequence(42)
    assert valid_sequence(fake_sequence, 5)

    # _FakeSequence has every length
    assert valid_sequence(fake_sequence, 1337)
