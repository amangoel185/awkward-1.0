# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

from __future__ import absolute_import

import pytest  # noqa: F401
import numpy as np  # noqa: F401
import awkward as ak  # noqa: F401

to_list = ak._v2.operations.convert.to_list


def test():
    array = ak._v2.contents.NumpyArray(np.zeros((3, 0), dtype=np.int32))
    buffs = ak._v2.operations.convert.to_buffers(array)
    new_array = ak._v2.operations.convert.from_buffers(*buffs)

    assert to_list(new_array) == [[], [], []]
