#residual_temperature_pinte.py
# use this to calculate residuals based on a temperature structure
# compared to the 12co temperature measurements from Pinte et al. 2018
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import interp2d
import radmc3dPy as rmc
import os
rad = np.pi / 180.
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams.update({'font.size': 12})

#This calculates and then shows you the model temperature

# ==== read empiricially measured data ====
# obs[:,0] is the radius
# obs[:,1] is the height
# obs[:,2] is the temperature
fname = 'pinte_12co.txt'
obs = np.loadtxt(fname)

# take a look at the measure observations
fig, axes = plt.subplots(1, 2, squeeze=True)
axes[0].plot(obs[:,0], obs[:,1], color='#00349E')
axes[0].set_xlabel('radius [au]')
axes[0].set_ylabel('height [au]')
axes[1].plot(obs[:,0], obs[:,2], color='#00349E')
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

#reading temperature
#modelname = ['1000denmodel', '10000denmodel', '100000denmodel', '1000000denmodel']
modelname = ['0.1micronmodel', '1micronmodel', '10micronmodel', '100micronmodel', '1millimetermodel', '1centimetermodel']
collect = []
opacs = []
dats = []
for ii in range(len(modelname)):
	os.chdir(modelname[ii])
	dat = rmc.analyze.readData(dtemp=True, ddens=True, binary=False)
	dats.append(dat)
	au = rmc.natconst.au
	r = dat.grid.x/au
	t = dat.grid.y
	mod = dat.dusttemp[:,:,0,0]
	collect.append(mod)
	os.chdir('..')

#graphing my temperature
# x axis is radius, y axis is theta (90 is midplane)

#Midplane Temperature
for ii in range(len(modelname)):
	inx = np.argmin(abs(dats[ii].grid.y - np.pi/2))
	plt.plot(dats[ii].grid.x/au, dats[ii].dusttemp[:, inx, 0, 0])
plt.title('Midplane Temperatures (0 Degrees)')
plt.xlabel('Radius (au)')
plt.ylabel('Temperature (K)')
plt.legend(modelname)
plt.xscale('log')
plt.yscale('log')
plt.show()

#Temperature at 60 degrees (pi/3)
for ii in range(len(modelname)):
        inx = np.argmin(abs(dats[ii].grid.y - np.pi/3))
        plt.plot(dats[ii].grid.x/au, dats[ii].dusttemp[:, inx, 0, 0])
plt.title('Temperatures at 60 Degree Angle')
plt.xlabel('Radius (au)')
plt.ylabel('Temperature (K)')
plt.legend(modelname)
plt.xscale('log')
plt.yscale('log')
plt.show()

# ==== convert cartesian coordinates to spherical coordinates ====
obs_cyr = obs[:,0]
obs_z = obs[:,1]
obs_r = np.sqrt(obs_cyr**2 + obs_z**2)
obs_theta = np.arctan2(obs_r, obs_z)

# ==== interpolate model data points ====
# set up an interpolation object
# be sure to look up 'interp2d' if you don't remember what this means
fn_collect = []
for ii in range(len(modelname)):
	fn_mod = interp2d(r, t, collect[ii].T)
	fn_collect.append(fn_mod)

# now obtain the points from the model with the same radius and theta
mod_points_collect = []
for jj in range(len(modelname)):
	npoints = len(obs_r)
	mod_points = np.zeros([npoints])
	for ii in range(npoints):
		mod_points[ii] = fn_collect[jj](obs_r[ii], obs_theta[ii])
	mod_points_collect.append(mod_points)

# let's compare the measured temperature points to the model points

col = ['#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#225ea8', '#00349E']
#col = ['#d9d9d9', '#bdbdbd', '#969696', '#737373', '#525252', '#252525']
#col = ['#d73027', '#fc8d59', '#fee090', '#542788', '#91bfdb', '#b35806']
graphlabels = ['.1 Micron Model', '1 Micron Model', '10 Micron Model', '100 Micron Model', '1 Millimeter Model', '1 Centimeter Model']
#linestyles = ['-', '--', '-.', ':', '^', 'v']
dashlist = [(0, (1, 10)), 'dotted', 'dashed', 'dashdot', (0, (5, 1)), (0, (3,1,1,1,1,1,))]

reg = obs[:,0] > 200
ax = plt.gca()
ax.plot(obs[:,0][reg], obs[:,2][reg], label='Measured', color='#000000')
for ii in range(len(modelname)):
	reg = obs[:,0] > 200
	ax.plot(obs[:,0][reg], mod_points_collect[ii][reg], label=graphlabels[ii], color=col[ii], linestyle=dashlist[ii])
plt.title('Density Temperature Comparison')
plt.xlabel('Radius (au)')
plt.ylabel('Temperature (K)')
ax.legend(loc=(1.04,0))
#plt.savefig('DensityTemperatureComparison.png')
plt.show()

# ==== residual ====
# finally we can calculate the difference between the observations and model
residual_collect = []
for ii in range(len(modelname)):
	reg = obs[:,0] > 200
	residual = obs[:,2][reg] - mod_points_collect[ii][reg]
	residual_collect.append(residual)
	plt.plot(obs[:,0][reg], residual, label=modelname[ii], color=col[ii])
plt.legend()
plt.title('Density Residuals')
plt.xlabel('Radius (au)')
plt.ylabel('Difference in Temperature (K)')
#plt.savefig('DensityResiduals.png')
plt.show()

# calculate reduced chi square
reducedchi_collect = []
for ii in range(len(modelname)):
	chi = np.sum(residual_collect[ii]**2 / (0.1*obs[:,2][reg]**2))
	dof = len(residual_collect[ii]) - 2
	reducedchi = chi / dof
	reducedchi_collect.append(reducedchi)
	
print(str(reducedchi_collect))
print(str(dof))

