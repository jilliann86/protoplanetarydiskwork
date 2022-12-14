#
# Import NumPy for array handling
#
import numpy as np
#
# Import plotting libraries (start Python with ipython --matplotlib)
#
#from mpl_toolkits.mplot3d import axes3d
#from matplotlib import pyplot as plt
#
from matplotlib import cm


# Some natural constants
#
au  = 1.49598e13     # Astronomical Unit       [cm]
pc  = 3.08572e18     # Parsec                  [cm]
ms  = 1.98892e33     # Solar mass              [g]
ts  = 5.78e3         # Solar temperature       [K]
ls  = 3.8525e33      # Solar luminosity        [erg/s]
rs  = 6.96e10        # Solar radius            [cm]
#
# Monte Carlo parameters
#
nphot    = 1000000
#
# Grid parameters
#
nr       = 100
ntheta   = 64
nphi     = 1
rin      = 1*au
rout     = 450*au
thetaup  = np.pi*0.5 - 0.7e0
#
# Disk parameters
#
sigmag0  = 25                # Sigma gas at 1 AU
sigmad0  = sigmag0 * 0.01    # Sigma dust at 1 AU
plsig    = -1.0e0            # Powerlaw of the surface density
hr0      = 0.12              # H_p/r at 1 AU
plh      = 0.1               # Powerlaw of flaring
#
# Star parameters
#
mstar    = ms
rstar    = 2.9 * rs
tstar    = 4270
pstar    = np.array([0.,0.,0.])
#
# Make the coordinates
#
ri       = np.logspace(np.log10(rin),np.log10(rout),nr+1)
thetai   = np.linspace(thetaup,0.5e0*np.pi,ntheta+1)
phii     = np.linspace(0.e0,np.pi*2.e0,nphi+1)
rc       = 0.5 * ( ri[0:nr] + ri[1:nr+1] )
thetac   = 0.5 * ( thetai[0:ntheta] + thetai[1:ntheta+1] )
phic     = 0.5 * ( phii[0:nphi] + phii[1:nphi+1] )
#
# Make the grid
#
qq       = np.meshgrid(rc,thetac,phic,indexing='ij')
rr       = qq[0]
tt       = qq[1]
zr       = np.pi/2.e0 - qq[1]
#
# Make the dust density model
#
sigmad   = sigmad0 * (rr/(100*au))**plsig
hhr      = hr0 * (rr/au)**plh
hh       = hhr * rr
rhod     = ( sigmad / (np.sqrt(2.e0*np.pi)*hh) ) * np.exp(-(zr**2/hhr**2)/2.e0)
#
# Write the wavelength_micron.inp file
#
lam1     = 0.1e0
lam2     = 7.0e0
lam3     = 25.e0
lam4     = 1.0e4
n12      = 20
n23      = 100
n34      = 30
lam12    = np.logspace(np.log10(lam1),np.log10(lam2),n12,endpoint=False)
lam23    = np.logspace(np.log10(lam2),np.log10(lam3),n23,endpoint=False)
lam34    = np.logspace(np.log10(lam3),np.log10(lam4),n34,endpoint=True)
lam      = np.concatenate([lam12,lam23,lam34])
nlam     = lam.size
#
# Write the wavelength file
#
with open('wavelength_micron.inp','w+') as f:
    f.write('%d\n'%(nlam))
    for value in lam:
        f.write('%13.6e\n'%(value))
#
#
# Write the stars.inp file
#
with open('stars.inp','w+') as f:
    f.write('2\n')
    f.write('1 %d\n\n'%(nlam))
    f.write('%13.6e %13.6e %13.6e %13.6e %13.6e\n\n'%(rstar,mstar,pstar[0],pstar[1],pstar[2]))
    for value in lam:
        f.write('%13.6e\n'%(value))
    f.write('\n%13.6e\n'%(-tstar))
#
# Write the grid file
#
with open('amr_grid.inp','w+') as f:
    f.write('1\n')                       # iformat
    f.write('0\n')                       # AMR grid style  (0=regular grid, no AMR)
    f.write('100\n')                     # Coordinate system: spherical
    f.write('0\n')                       # gridinfo
    f.write('1 1 0\n')                   # Include r,theta coordinates
    f.write('%d %d %d\n'%(nr,ntheta,1))  # Size of grid
    for value in ri:
        f.write('%13.6e\n'%(value))      # X coordinates (cell walls)
    for value in thetai:
        f.write('%13.6e\n'%(value))      # Y coordinates (cell walls)
    for value in phii:
        f.write('%13.6e\n'%(value))      # Z coordinates (cell walls)
#
# Write the density file
#
with open('dust_density.inp','w+') as f:
    f.write('1\n')                       # Format number
    f.write('%d\n'%(nr*ntheta*nphi))     # Nr of cells
    f.write('1\n')                       # Nr of dust species
    data = rhod.ravel(order='F')         # Create a 1-D view, fortran-style indexing
    data.tofile(f, sep='\n', format="%13.6e")
    f.write('\n')
#
# Dust opacity control file
#
with open('dustopac.inp','w+') as f:
    f.write('2               Format number of this file\n')
    f.write('1               Nr of dust species\n')
    f.write('============================================================================\n')
    f.write('1               Way in which this dust species is read\n')
    f.write('0               0=Thermal grain\n')
    f.write('silicate        Extension of name of dustkappa_***.inp file\n')
    f.write('----------------------------------------------------------------------------\n')
#
# Write the radmc3d.inp control file
#
with open('radmc3d.inp','w+') as f:
    f.write('nphot = %d\n'%(nphot))
    f.write('scattering_mode_max = 1\n')
    f.write('iranfreqmode = 1\n')

exec(open('./problem_opacity.py').read())

#Import the radmc3dPy module
import radmc3dPy
import os
import matplotlib.pyplot as plt
from radmc3dPy import natconst
import numpy as np
os.system('radmc3d mctherm')

#Temperature Contours
data = radmc3dPy.analyze.readData(dtemp=True, ddens=True, binary=False)
c = plt.contourf(data.grid.x/natconst.au, np.pi/2.-data.grid.y, data.dusttemp[:,:,0,0].T, 30, cmap=cm.Blues)
plt.xlabel('r [AU]')
plt.ylabel(r'$\pi/2-\theta$')
plt.xscale('log')
cb = plt.colorbar(c)
cb.set_label('T [K]', rotation=270)
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
inx = np.argmin(abs(data.grid.y - np.pi/2))
plt.plot(data.grid.x/natconst.au, data.rhodust[:, inx, 0, 0])
plt.xscale('log')
plt.yscale('log')
plt.show()

#Temperature Midplane Profile
inx = np.argmin(abs(data.grid.y - np.pi/2))
plt.plot(data.grid.x/natconst.au, data.dusttemp[:, inx, 0, 0])
plt.xscale('log')
plt.yscale('log')
plt.show()

import os
modelname = '10micronmodel'
os.system('mkdir %s'%modelname)
os.system('mv amr_grid.inp dust_density.inp dustopac.inp dustkappa_*.inp radmc3d.inp stars.inp wavelength_micron.inp dust_temperature.dat %s'%modelname)


#formula
import math
from astropy import constants as const 
r = data.grid.x/natconst.au
teff = (0.05 * (4 * math.pi * rstar**2 * const.sigma_sb * tstar**4) / (4 * math.pi * const.sigma_sb  * r**2)**(1/4))
