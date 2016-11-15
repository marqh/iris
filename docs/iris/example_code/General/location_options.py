import cartopy
import iris
import iris.plot as iplt
import math
from matplotlib import pyplot as plt
import numpy as np

fname = iris.sample_data_path('A1B.2098.pp')
cube = iris.load_cube(fname)
cube.coord('latitude').guess_bounds()
cube.coord('longitude').guess_bounds()

lims = [4, 10, 57.5, 63.5]

fig = plt.figure(figsize=(16, 9))




prj = cartopy.crs.PlateCarree(globe=cartopy.crs.Globe(datum='WGS84', ellipse='WGS84'))

ax1 = plt.subplot(1, 2, 1, projection=prj)
iplt.pcolormesh(cube)
iplt.points(cube)
ax1.coastlines(resolution='10m')
ax1.set_extent(lims)

new_cube = cube.copy()

ax2 = plt.subplot(1, 2, 2, projection=prj)

x, y = np.broadcast_arrays(new_cube.coord('longitude').points.reshape(1, len(new_cube.coord('longitude').points)),
                           new_cube.coord('latitude').points.reshape(len(new_cube.coord('latitude').points), 1))

xl = x - (x[0, 2] - x[0, 1]) / 2.
yb = y - (y[2, 0] - y[1, 0]) / 2.

# x = math.pi / 180 * (x - (x[0, 2] - x[0, 1]) / 2.)
# y = math.pi / 180 * (y - (y[2, 0] - y[1, 0]) / 2.)


trans_crs = new_cube.coord('latitude').coord_system.as_cartopy_projection()

trans_crs = cartopy.crs.PlateCarree(globe=cartopy.crs.Globe(datum='WGS84', ellipse='WGS84'))
trans_crs = cartopy.crs.PlateCarree()
# trans_crs = cartopy.crs.PlateCarree(globe=cartopy.crs.Globe(semimajor_axis=math.degrees(1),
#                                                             towgs84=(0, 0, 0)))

print(prj.proj4_params)
print(trans_crs.proj4_params)

plt.pcolormesh(xl, yb, new_cube.data, transform=trans_crs)
plt.scatter(x, y, transform=trans_crs)
ax2.coastlines(resolution='10m')
ax2.set_extent(lims)

plt.show()
