import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import interp2d
import radmc3dPy as rmc
import os
rad = np.pi / 180.

#reading temperature
#0.1 model
os.chdir('0.1micronmodel')
dat = rmc.analyze.readData(dtemp=True, binary=False)
os.chdir('..')
au = rmc.natconst.au
r = dat.grid.x/au
t = dat.grid.y
mod = dat.dusttemp[:,:,0,0]

#graphing my temperature
# x axis is radius, y axis is theta (90 is midplane)
plt.pcolormesh(r, t/rad, mod.T, norm=colors.LogNorm())
plt.colorbar()
plt.title('0.1 Micron Model')
plt.show()

#1 model
os.chdir('1micronmodel')
dat = rmc.analyze.readData(dtemp=True, binary=False)
os.chdir('..')
au = rmc.natconst.au
r = dat.grid.x/au
t = dat.grid.y
mod = dat.dusttemp[:,:,0,0]

#graphing my temperature
# x axis is radius, y axis is theta (90 is midplane)
plt.pcolormesh(r, t/rad, mod.T, norm=colors.LogNorm())
plt.colorbar()
plt.show()

#10 model
os.chdir('10micronmodel')
dat = rmc.analyze.readData(dtemp=True, binary=False)
os.chdir('..')
au = rmc.natconst.au
r = dat.grid.x/au
t = dat.grid.y
mod = dat.dusttemp[:,:,0,0]

#graphing my temperature
# x axis is radius, y axis is theta (90 is midplane)
plt.pcolormesh(r, t/rad, mod.T, norm=colors.LogNorm())
plt.colorbar()
plt.show()

#100 model
os.chdir('100micronmodel')
dat = rmc.analyze.readData(dtemp=True, binary=False)
os.chdir('..')
au = rmc.natconst.au
r = dat.grid.x/au
t = dat.grid.y
mod = dat.dusttemp[:,:,0,0]

#graphing my temperature
# x axis is radius, y axis is theta (90 is midplane)
plt.pcolormesh(r, t/rad, mod.T, norm=colors.LogNorm())
plt.colorbar()
plt.show()

#Temperature Contours
data = rmc.analyze.readData(dtemp=True, ddens=True, binary=False)
c = plt.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 30)
plt.xlabel('r [AU]')
plt.ylabel(r'$\pi/2-\theta$')
plt.xscale('log')
cb = plt.colorbar(c)
cb.set_label('T [K]', rotation=270.)
c = plt.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 10,  colors='k', linestyles='solid')
plt.clabel(c, inline=1, fontsize=10)
plt.show()
