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
"""Unit tests for the :class:`iris.coords.CellMeaasure` class."""

from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)  # noqa

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

import numpy as np

from iris.coords import CellMeasure
from iris.tests import mock
from iris.coord_systems import GeogCS


class Test_CellMeasure(tests.IrisTest):
    def setUp(self):
        values = [10., 12., 16., 9.]
        self.measure = CellMeasure(values, units='m^2',
                                   standard_name='cell_area',
                                   long_name='measured_area',
                                   var_name='area',
                                   attributes={'notes': '1m accuracy'},
                                   measure='area')

    def test_no_bounds(self):
        msg = 'CellMeasure instances do not have bounds'
        with self.assertRaisesRegexp(AttributeError, msg):
            self.measure.bounds = np.arange(8).reshape(2, 4)

    def test_no_crs(self):
        msg = 'CellMeasure instances do not have a coord_system'
        with self.assertRaisesRegexp(AttributeError, msg):
            self.measure.coord_system = GeogCS(6371229)

if __name__ == '__main__':
    tests.main()
