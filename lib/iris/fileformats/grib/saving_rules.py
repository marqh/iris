# (C) British Crown Copyright 2013, Met Office
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

# DO NOT EDIT: AUTO-GENERATED 

def coordinate_reference_system(cube):
    if cube.CoordinateReferenceSystem(crs_name = "latitude_longitude", semi_major_axis = 6367470, ):
        id = "<http://www.metarelate.net/metOcean/mapping/4a63ee7eb0aec5bbd426fbcf47659439aa059c7d>"
        agrib.gridType = "regular_ll"
        agrib.shapeOfTheEarth = 0

    if cube.CoordinateReferenceSystem(crs_name = "rotated_latitude_longitude", semi_major_axis = 6367470, ):
        id = "<http://www.metarelate.net/metOcean/mapping/e071c625e511e8ecb6717d90835fe621bc216435>"
        agrib.shapeOfTheEarth = 0
        agrib.gridType = "rotated_ll"

    if cube.CoordinateReferenceSystem(semi_major_axis = {<http://www.metarelate.net/metOcean/component/08e0d8ebace2ad7ad8606c74c2392eb7e887d7ce>.semi_major_axis}, crs_name = "latitude_longitude", ):
        id = "<http://www.metarelate.net/metOcean/mapping/efc0fc2ee887a2f35502280d47cf8efdd189dbaa>"
        agrib.gridType = "regular_ll"
        agrib.scaledValueOfRadiusOfSphericalEarth = {<http://def.ecmwf.int/api/grib/keys/scaledValueOfRadiusOfSphericalEarth>} 
        agrib.scaleFactorOfRadiusOfSphericalEarth = {<http://def.ecmwf.int/api/grib/keys/scaleFactorOfRadiusOfSphericalEarth>} 
        agrib.shapeOfTheEarth = 1

    if cube.CoordinateReferenceSystem(semi_major_axis = {<http://www.metarelate.net/metOcean/component/60f88e574dbdc11d4e1f0d438234a187c7fa3f89>.semi_major_axis}, crs_name = "rotated_latitude_longitude", ):
        id = "<http://www.metarelate.net/metOcean/mapping/fb604b57e8346e89b7a00fb4e752fbe161622109>"
        agrib.scaledValueOfRadiusOfSphericalEarth = {<http://def.ecmwf.int/api/grib/keys/scaledValueOfRadiusOfSphericalEarth>} 
        agrib.gridType = "rotated_ll"
        agrib.scaleFactorOfRadiusOfSphericalEarth = {<http://def.ecmwf.int/api/grib/keys/scaleFactorOfRadiusOfSphericalEarth>} 
        agrib.shapeOfTheEarth = 1


def translate(cube):
    if cube.DomainAxis(coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/cd268f108e33e9219e3cdb7db5c6880cde01d3d7>.points}, coordinate_reference_system = coordinate_reference_system(), standard_name = "grid_latitude", ),axis_index = 0, ) and \
       cube.DomainAxis(axis_index = 1, coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/61d853bee6bca3368dd80057970c9d9e310f8c8b>.points}, standard_name = "grid_longitude", CoordinateReferenceSystem = coordinate_reference_system(), circular = {<http://www.metarelate.net/metOcean/component/61d853bee6bca3368dd80057970c9d9e310f8c8b>.circular}, ),):
        id = "<http://www.metarelate.net/metOcean/mapping/2c82220e463af9172cf98bf99df91de2cf58a13b>"
        agrib._x_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_points>} 
        agrib._y_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_y_points>} 
        agrib._x_circular = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_circular>} 
        agrib.gridType = "rotated_ll"
        agrib.jPointsAreConsecutive = 0

    if cube.DomainAxis(coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/4cebe95e7a8711a53ebc0a8a408d9522f6a5e794>.points}, CoordinateReferenceSystem = coordinate_reference_system(), standard_name = "longitude", circular = {<http://www.metarelate.net/metOcean/component/4cebe95e7a8711a53ebc0a8a408d9522f6a5e794>.circular}, ),axis_index = 0, ) and \
       cube.DomainAxis(axis_index = 1, coordinate = DimensionCoordinate(bounds = "None", standard_name = "latitude", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/b7d868f5ea2792afab348ef84ea81e7072509e35>.points}, coordinate_reference_system = coordinate_reference_system(), ),):
        id = "<http://www.metarelate.net/metOcean/mapping/3eaf7221354afd1a3ae9bd43cc5f97ed4ee00dac>"
        agrib.jPointsAreConsecutive = 1
        agrib._x_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_points>} 
        agrib._y_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_y_points>} 
        agrib.gridType = "regular_ll"
        agrib._x_circular = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_circular>} 

    if cube.DomainAxis(axis_index = 1, coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/cd268f108e33e9219e3cdb7db5c6880cde01d3d7>.points}, coordinate_reference_system = coordinate_reference_system(), standard_name = "grid_latitude", ),) and \
       cube.DomainAxis(coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/61d853bee6bca3368dd80057970c9d9e310f8c8b>.points}, standard_name = "grid_longitude", CoordinateReferenceSystem = coordinate_reference_system(), circular = {<http://www.metarelate.net/metOcean/component/61d853bee6bca3368dd80057970c9d9e310f8c8b>.circular}, ),axis_index = 0, ):
        id = "<http://www.metarelate.net/metOcean/mapping/5d3487aa6591dcc980cda057016af2214327d1d5>"
        agrib.jPointsAreConsecutive = 1
        agrib._x_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_points>} 
        agrib._y_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_y_points>} 
        agrib._x_circular = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_circular>} 
        agrib.gridType = "rotated_ll"

    if cube.DomainAxis(coordinate = DimensionCoordinate(bounds = "None", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/4cebe95e7a8711a53ebc0a8a408d9522f6a5e794>.points}, CoordinateReferenceSystem = coordinate_reference_system(), standard_name = "longitude", circular = {<http://www.metarelate.net/metOcean/component/4cebe95e7a8711a53ebc0a8a408d9522f6a5e794>.circular}, ),axis_index = 1, ) and \
       cube.DomainAxis(coordinate = DimensionCoordinate(bounds = "None", standard_name = "latitude", units = "degrees", points = {<http://www.metarelate.net/metOcean/component/b7d868f5ea2792afab348ef84ea81e7072509e35>.points}, coordinate_reference_system = coordinate_reference_system(), ),axis_index = 0, ):
        id = "<http://www.metarelate.net/metOcean/mapping/bc324e3df82fe0191ac7b478242dc0ab484f7f98>"
        agrib._x_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_points>} 
        agrib._y_points = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_y_points>} 
        agrib.gridType = "regular_ll"
        agrib._x_circular = {<http://reference.metoffice.gov.uk/def/grib/computed_value#_x_circular>} 
        agrib.jPointsAreConsecutive = 0


