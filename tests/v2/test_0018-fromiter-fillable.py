# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

pytestmark = pytest.mark.skipif(
    ak._util.py27, reason="No Python 2.7 support in Awkward 2.x"
)

to_list = ak._v2.operations.convert.to_list


def test_types():
    t0 = ak.types.UnknownType()
    t1 = ak.types.PrimitiveType("int32")
    t2 = ak.types.OptionType(t1)
    t3 = ak.types.UnionType((t1, ak.types.PrimitiveType("float64")))
    t4 = ak.types.ListType(t1)
    t4b = ak.types.ListType(ak.types.PrimitiveType("int32"))
    t5 = ak.types.ListType(t4)
    t6 = ak.types.OptionType(t4)
    assert repr(t0) == "unknown"
    assert repr(t1) == "int32"
    assert repr(t2) == "?int32"
    assert repr(t3) == "union[int32, float64]"
    assert repr(t4) == "var * int32"
    assert repr(t4b) == "var * int32"
    assert repr(t5) == "var * var * int32"
    assert repr(t6) == "option[var * int32]"
    assert repr(t2.type) == "int32"
    assert t3.numtypes == 2
    assert repr(t3.type(0)) == "int32"
    assert repr(t3.type(1)) == "float64"
    assert [repr(x) for x in t3.types] == ["int32", "float64"]
    assert repr(t4.type) == "int32"
    assert repr(t4b.type) == "int32"
    assert repr(t5.type) == "var * int32"


def test_boolean():
    a = ak._v2.highlevel.ArrayBuilder()
    a.boolean(True)
    a.boolean(True)
    a.boolean(False)
    a.boolean(True)
    assert to_list(a.snapshot()) == [True, True, False, True]
    assert to_list(a) == [True, True, False, True]
    # FIXME: TypeError: 'ArrayBuilder' object is not subscriptable
    assert to_list(a.snapshot()[1:-1]) == [True, False]


def test_big():
    a = ak._v2.highlevel.ArrayBuilder(initial=90)
    for i in range(2000):
        if i == 200:
            tmp = a.snapshot()
        a.boolean(i % 2 == 0)
    assert to_list(a) == [True, False] * 1000
    assert to_list(tmp) == [True, False] * 100


def test_integer():
    a = ak._v2.highlevel.ArrayBuilder()
    a.integer(10)
    a.integer(9)
    a.integer(8)
    a.integer(7)
    a.integer(6)
    assert to_list(a.snapshot()) == [10, 9, 8, 7, 6]
    assert to_list(a) == [10, 9, 8, 7, 6]
    assert to_list(a.snapshot()[1:-1]) == [9, 8, 7]


def test_real():
    a = ak._v2.highlevel.ArrayBuilder()
    a.real(1.1)
    a.real(2.2)
    a.real(3.3)
    a.real(4.4)
    a.real(5.5)
    assert to_list(a.snapshot()) == [1.1, 2.2, 3.3, 4.4, 5.5]
    assert to_list(a) == [1.1, 2.2, 3.3, 4.4, 5.5]
    assert to_list(a.snapshot()[1:-1]) == [2.2, 3.3, 4.4]


def test_integer_real():
    a = ak._v2.highlevel.ArrayBuilder()
    a.integer(1)
    a.integer(2)
    a.real(3.3)
    a.integer(4)
    a.integer(5)
    assert to_list(a.snapshot()) == [1.0, 2.0, 3.3, 4.0, 5.0]
    assert to_list(a) == [1.0, 2.0, 3.3, 4.0, 5.0]
    assert to_list(a.snapshot()[1:-1]) == [2.0, 3.3, 4.0]


def test_real_integer():
    a = ak._v2.highlevel.ArrayBuilder()
    a.real(1.1)
    a.real(2.2)
    a.integer(3)
    a.real(4.4)
    a.real(5.5)
    assert to_list(a.snapshot()) == [1.1, 2.2, 3.0, 4.4, 5.5]
    assert to_list(a) == [1.1, 2.2, 3.0, 4.4, 5.5]
    assert to_list(a.snapshot()[1:-1]) == [2.2, 3.0, 4.4]


def test_list_real():
    a = ak._v2.highlevel.ArrayBuilder()
    a.begin_list()
    a.real(1.1)
    a.real(2.2)
    a.real(3.3)
    a.end_list()
    a.begin_list()
    a.end_list()
    a.begin_list()
    a.real(4.4)
    a.real(5.5)
    a.end_list()
    assert to_list(a.snapshot()) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
    assert to_list(a) == [[1.1, 2.2, 3.3], [], [4.4, 5.5]]
    assert to_list(a.snapshot()[1:-1]) == [[]]
    assert to_list(a.snapshot()[1:]) == [[], [4.4, 5.5]]


def test_list_list_real():
    a = ak._v2.highlevel.ArrayBuilder()
    a.begin_list()
    a.begin_list()
    a.real(1.1)
    a.real(2.2)
    a.real(3.3)
    a.end_list()
    a.begin_list()
    a.end_list()
    a.begin_list()
    a.real(4.4)
    a.real(5.5)
    a.end_list()
    a.end_list()
    a.begin_list()
    a.end_list()
    a.begin_list()
    a.begin_list()
    a.real(6.6)
    a.real(7.7)
    a.end_list()
    a.begin_list()
    a.real(8.8)
    a.real(9.9)
    a.end_list()
    a.end_list()
    assert to_list(a.snapshot()) == [
        [[1.1, 2.2, 3.3], [], [4.4, 5.5]],
        [],
        [[6.6, 7.7], [8.8, 9.9]],
    ]
    assert to_list(a) == [
        [[1.1, 2.2, 3.3], [], [4.4, 5.5]],
        [],
        [[6.6, 7.7], [8.8, 9.9]],
    ]
    assert to_list(a.snapshot()[1:]) == [[], [[6.6, 7.7], [8.8, 9.9]]]


def test_list_errors():
    with pytest.raises(ValueError):
        a = ak._v2.highlevel.ArrayBuilder()
        a.end_list()

    with pytest.raises(ValueError):
        a = ak._v2.highlevel.ArrayBuilder()
        a.real(3.14)
        a.end_list()

    with pytest.raises(ValueError):
        a = ak._v2.highlevel.ArrayBuilder()
        a.begin_list()
        a.real(3.14)
        a.end_list()
        a.end_list()

    with pytest.raises(ValueError):
        a = ak._v2.highlevel.ArrayBuilder()
        a.begin_list()
        a.begin_list()
        a.real(3.14)
        a.end_list()
        a.end_list()
        a.end_list()

    a = ak._v2.highlevel.ArrayBuilder()
    a.begin_list()
    a.real(1.1)
    a.real(2.2)
    a.real(3.3)
    a.end_list()
    a.begin_list()
    a.real(4.4)
    a.real(5.5)
    assert to_list(a.snapshot()) == [[1.1, 2.2, 3.3]]
    assert to_list(a) == [[1.1, 2.2, 3.3]]
    assert to_list(a.snapshot()[1:]) == []
