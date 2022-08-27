# residual_temperature_pinte.py
# use this to calculate residuals based on a temperature structure
# compared to the 12co temperature measurements from Pinte et al. 2018
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import interp2d
import radmc3dPy as rmc
import os
rad = np.pi / 180.

#This calculates and then shows you the model temperature

# ==== read empiricially measured data ====
# obs[:,0] is the radius
# obs[:,1] is the height
# obs[:,2] is the temperature
fname = 'pinte_12co.txt'
obs = np.loadtxt(fname)

# take a look at the measure observations
fig, axes = plt.subplots(1, 2, squeeze=True)
axes[0].plot(obs[:,0], obs[:,1])
axes[0].set_xlabel('radius [au]')
axes[0].set_ylabel('height [au]')
axes[1].plot(obs[:,0], obs[:,2])
axes[1].set_xlabel('radius [au]')
axes[1].set_ylabel('Temperature [K]')
fig.tight_layout()
plt.show()

#The temperature of my model

#reading temperature
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
plt.show()

# ==== convert cartesian coordinates to spherical coordinates ====
obs_cyr = obs[:,0]
obs_z = obs[:,1]
obs_r = np.sqrt(obs_cyr**2 + obs_z**2)
obs_theta = np.arctan2(obs_r, obs_z)

# ==== interpolate model data points ====
# set up an interpolation object
# be sure to look up 'interp2d' if you don't remember what this means
fn_mod = interp2d(r, t, mod.T)

# now obtain the points from the model with the same radius and theta
npoints = len(obs_r)
mod_points = np.zeros([npoints])
for ii in range(npoints):
    mod_points[ii] = fn_mod(obs_r[ii], obs_theta[ii])

# let's compare the measured temperature points to the model points
ax = plt.gca()
ax.plot(obs[:,0], obs[:,2], label='Measured')
ax.plot(obs[:,0], mod_points, label='Model')
ax.legend()
plt.show()

# ==== residual ====
# finally we can calculate the difference between the observations and model
residual = obs[:,2] - mod_points

plt.plot(obs[:,0], residual)
plt.show()

# calculate reduced chi square
chi = np.sum(residual**2 / (0.1*obs[:,2]**2))
dof = len(residual) - 1
reducedchi = chi / dof
print(str(reducedchi))


