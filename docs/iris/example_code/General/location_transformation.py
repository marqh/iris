"""
Coordinate Reference System Transforms
======================================

There are many complexities and assumptions involved in transforming coordinates
between coordinate reference systems, such as differently shaped ellipsoids.

This example shows two different outcomes of CRS transforms using different
methods.  Both are valid results, but depending on the purpose of the transform,
one must choose which is most appropriate.
"""

import itertools

import cartopy.crs as ccrs
import iris
import iris.quickplot as qplt
import matplotlib.pyplot as plt

import numpy as np

# Load cube containing data in GeogCRS
fname = iris.sample_data_path('A1B.2098.pp')
cube = iris.load_cube(fname)

# Create WGS84 Iris coordinate system
wgs84_cs = iris.coord_systems.GeogCS(semi_major_axis=6371229.0,
                                        inverse_flattening=298.25722356)

# Create WGS84 Cartopy projection
wgs84_proj = ccrs.PlateCarree(central_longitude=0.,
                             globe=ccrs.Globe(datum='WGS84',
                                              ellipse='WGS84'))

# Create WGS84 Cartopy projection specifying parameters directly
wgs84_proj2 =  ccrs.PlateCarree(central_longitude=0.,
                             globe=ccrs.Globe(semimajor_axis=6371229.0,
                                        inverse_flattening=298.25722356))
print cube.coord_system()
print cube.coord_system().as_cartopy_crs().proj4_params

# Null transform: Assign a WGS84 coordinate system to the cube, effectively
# treating the coordinates from the sphere as if they are on an ellipse
cube_nt = cube.copy()
cube_nt.coord('latitude').coord_system = wgs84_cs
cube_nt.coord('longitude').coord_system = wgs84_cs

###############################################################################
# The following section is my attempt to transform the points directly, since #
# the plotting code doesn't seem to be doing that. I got some very strange    #
# results here.                                                               #
###############################################################################
lons, lats = iris.analysis.cartography.get_xy_grids(cube)

def trans(src_crs, target_crs, x, y):
    for sx, sy in itertools.product(x, y):
        tx, ty = target_crs.transform_point(sx, sy, src_crs)
        # Some of the numbers for tx/ty are very large, so I've applied
        # modulus functions to see if they are anything close to sensible
        print sx, sy, '--->', tx % 360, ((ty + 90) % 180) - 90

print wgs84_cs.as_cartopy_crs().proj4_params
print wgs84_proj.proj4_params
trans(wgs84_cs.as_cartopy_crs(), wgs84_proj,
      [0, 45, 90, 180, 270], [-90, -45, 0, 45, 90])
###############################################################################

# I define a plot() function so that I can run the code under python -i and
# inspect the objects without having to wait for the data to plot
def plot():
    global cube, cube_nt
    # Extract a region from the cubes
    cube = cube.intersection(longitude=(4, 10), latitude=(56, 65))
    cube_nt = cube_nt.intersection(longitude=(4, 10), latitude=(56, 65))

    ax1 = plt.axes(projection=wgs84_proj)

    qplt.pcolor(cube, edgecolors='black', axes=ax1)
    p1 = qplt.points(cube)
    ax1 = plt.gca()
    ax1.coastlines(resolution='10m')

    plt.draw()

    plt.figure()
    ax2 = plt.axes(projection=wgs84_proj)
    qplt.pcolor(cube_nt, edgecolors='black', axes=ax2)
    p2 = qplt.points(cube_nt)
    ax2 = plt.gca()
    ax2.coastlines(resolution='10m')
    plt.draw()
    # If a transform took place this assert should fail
    assert(np.all(p1.get_paths()[0].vertices == p2.get_paths()[0].vertices))
    plt.show()

