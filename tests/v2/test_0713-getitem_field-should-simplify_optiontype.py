# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.convert.to_list


@pytest.mark.skip(reason="FIXME: ak.is_none not implemented")
def test():
    arr1 = ak._v2.highlevel.Array({"a": [1, 2], "b": [1, None]})
    arr2 = ak._v2.operations.structure.mask(arr1, [True, True])
    assert isinstance(arr2.layout, ak._v2.contents.ByteMaskedArray)
    assert isinstance(arr2.layout.content, ak._v2.contents.RecordArray)
    assert isinstance(arr2.layout.content["b"], ak._v2.contents.IndexedOptionArray)

    assert isinstance(arr2.b.layout, ak._v2.contents.IndexedOptionArray)
    assert isinstance(arr2.b.layout.content, ak._v2.contents.NumpyArray)

    assert ak.is_none(arr2.b).tolist() == [False, True]

    arr3 = ak.virtual(lambda: arr2, form=arr2.layout.form, length=len(arr2))
    assert ak.is_none(arr3.b).tolist() == [False, True]
