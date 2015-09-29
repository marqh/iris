# (C) British Crown Copyright 2015, Met Office
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
"""Unit tests for the `iris.fileformats.pp.sixtyfour_bit_headers_and_data`
function."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

import iris.fileformats.pp as pp
import iris.tests.stock as stock


class TestSixyfourBit(tests.IrisTest):
    def setUp(self):
        self.cube = stock.realistic_3d()
        self.ppf = list(pp.as_fields(self.cube))[0]

    def test_sixtyfour_bit_headers_and_data(self):
        ird = self.ppf.sixtyfour_bit_headers_and_data(-9999)
        (int_headers, real_headers, data) = ird
        self.assertEqual(int_headers.dtype, np.dtype('>u8'))
        self.assertEqual(real_headers.dtype, np.dtype('>f8'))
        self.assertEqual(data.dtype, np.dtype('>i8'))


if __name__ == "__main__":
    tests.main()
