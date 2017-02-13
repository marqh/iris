# (C) British Crown Copyright 2017, Met Office
#
# This file is part of Iris.
#
# Iris is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Iris is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Iris.  If not, see <http://www.gnu.org/licenses/>.
"""Test :meth:`iris._lazy data.as_lazy_data` method."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests


import numpy as np
import dask.array as da

from iris._lazy_data import as_lazy_data, as_concrete_data, is_lazy_data


class Test_as_lazy_data(tests.IrisTest):
    def test_lazy(self):
        lazy_values = np.arange(30).reshape((2, 5, 3))
        lazy_array = da.from_array(lazy_values, 1e6)
        result = as_lazy_data(lazy_array)
        self.assertTrue(is_lazy_data(result))
        self.assertIs(result, lazy_array)

    def test_real(self):
        real_array = np.arange(24).reshape((2, 3, 4))
        result = as_lazy_data(real_array)
        self.assertTrue(is_lazy_data(result))
        self.assertArrayAllClose(as_concrete_data(result),
                                 real_array)


if __name__ == '__main__':
    tests.main()
