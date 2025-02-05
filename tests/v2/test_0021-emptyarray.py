# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.convert.to_list


def test_getitem():
    a = ak._v2.operations.convert.from_iter(
        [[], [[], []], [[], [], []]], highlevel=False
    )

    assert to_list(a[2]) == [[], [], []]
    assert a.typetracer[2].form == a[2].form

    assert to_list(a[2, 1]) == []
    assert a.typetracer[2, 1].form == a[2, 1].form
    with pytest.raises(ValueError):
        a[2, 1, 0]
    assert to_list(a[2, 1][()]) == []
    assert a.typetracer[2, 1][()].form == a[2, 1][()].form
    with pytest.raises(IndexError):
        a[2, 1][0]
    assert to_list(a[2, 1][100:200]) == []
    assert a.typetracer[2, 1][100:200].form == a[2, 1][100:200].form
    assert to_list(a[2, 1, 100:200]) == []
    assert a.typetracer[2, 1, 100:200].form == a[2, 1, 100:200].form
    assert to_list(a[2, 1][np.array([], dtype=int)]) == []
    assert (
        a.typetracer[2, 1][np.array([], dtype=int)].form
        == a[2, 1][np.array([], dtype=int)].form
    )
    assert to_list(a[2, 1, np.array([], dtype=int)]) == []
    assert (
        a.typetracer[2, 1, np.array([], dtype=int)].form
        == a[2, 1, np.array([], dtype=int)].form
    )
    with pytest.raises(ValueError):
        a[2, 1, np.array([0], dtype=int)]
    with pytest.raises(IndexError):
        a[2, 1][100:200, 0]
    with pytest.raises(IndexError):
        a[2, 1][100:200, 200:300]

    assert to_list(a[2, 1][100:200, np.array([], dtype=int)]) == []
    assert (
        a.typetracer[2, 1][100:200, np.array([], dtype=int)].form
        == a[2, 1][100:200, np.array([], dtype=int)].form
    )

    assert to_list(a[1:, 1:]) == [[[]], [[], []]]
    assert a.typetracer[1:, 1:].form == a[1:, 1:].form
    with pytest.raises(ValueError):
        a[1:, 1:, 0]
