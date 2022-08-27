# Import the radmc3dPy module
import radmc3dPy
import os
import matplotlib.pyplot as plt
from radmc3dPy import natconst
import numpy as ny

# Dust model setup with ascii input files
radmc3dPy.setup.problemSetupDust('ppdisk', binary=False, mdisk='1e-5*ms')

# Copy the dust opacity 
os.system('cp -v ../datafiles/dustkappa_silicate.inp .')

# Calculate the dust temperature
os.system('radmc3d mctherm')

# Gas model setup with ascii input files
radmc3dPy.setup.problemSetupGas('ppdisk', binary=False)

# Copy the dust opacity and co data files from the datafiles directory
os.system('cp -v ../datafiles/molecule_co.inp .')

#Temperature Contours
data = radmc3dPy.analyze.readData(dtemp=True, ddens=True, binary=False)
c = plt.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 30)
plt.xlabel('r [AU]')
plt.ylabel(r'$\pi/2-\theta$')
plt.xscale('log')
cb = plt.colorbar(c)
cb.set_label('T [K]', rotation=270.)
c = plt.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 10,  colors='k', linestyles='solid')
plt.clabel(c, inline=1, fontsize=10)
plt.show()

#Density
c = plt.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.rhodust[:,:,0,0].T, 30)
plt.xlabel('r [AU]')
plt.ylabel(r'$\pi/2-\theta$')
plt.xscale('log')
cb = plt.colorbar(c)
cb.set_label('T [K]', rotation=270.)
c = plt.contour(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.rhodust[:,:,0,0].T, 10,  colors='k', linestyles='solid')
plt.clabel(c, inline=1, fontsize=10)
plt.show()

#Density Midplane Profile
plt.plot(data.grid.x/natconst.au, data.rhodust[:,data.grid.ny//2, 0, 0])
plt.xscale('log')
plt.yscale('log')
plt.show()

#Temperature Midplane Profile
plt.plot(data.grid.x/natconst.au, data.dusttemp[:,data.grid.ny//2, 0, 0])
plt.xscale('log')
plt.yscale('log')
plt.show()

#Command to run this whole thing
#exec(open('./mysetup_model.py').read())
