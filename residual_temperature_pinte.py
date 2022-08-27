# residual_temperature_pinte.py
# use this to calculate residuals based on a temperature structure
# compared to the 12co temperature measurements from Pinte et al. 2018
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import interp2d
import radmc3dPy as rmc
rad = np.pi / 180.

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

# ==== model temperature ====
# assume there is a model temperature here 
# this will be set up by hand here
# but the temperature should come from radmc3d
# be sure to set it so that the temperature is a 2D array
r = np.geomspace(1, 400, 20) # [au]
t = np.linspace(45*rad, 90*rad, 30)
rr, tt = np.meshgrid(r, t, indexing='ij')
cyrr = rr * np.sin(tt)
zz = rr * np.cos(tt)

# model temperature as a function of radius and theta 
mod = 10 * (cyrr / 200)**(-0.5)

# == alternate version reading temperature from radmc3d
# dat = rmc.analyze.readData(dtemp=True)
# r = dat.grid.x/au
# t = dat.grid.y
# mod = dat.dusttemp[:,:,0,0]

# let's take a look at the temperature
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

