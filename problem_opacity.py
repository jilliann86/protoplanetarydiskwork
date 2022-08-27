# problem_opacity.py
# calculate the opacity of the grain 
import numpy as np
import matplotlib.pyplot as plt
import radmc3dPy as rmc
import dsharp_opac as dso

# ==== load the opacity ====
d      = np.load(dso.get_datafile('default_opacities_smooth.npz'))
agrid      = d['a']
wgrid    = d['lam']
k_abs  = d['k_abs']
k_sca  = d['k_sca']
gsca   = d['g']

# ==== pick out the desired sizes ====
a = [0.001]
name = ['small']
ngsize = len(a)

# organize it into radmc3dPy format 
opac = rmc.dustopac.radmc3dDustOpac()
for ii in range(ngsize):
    opac.wav.append(wgrid)
    opac.nwav.append(len(opac.wav[ii]))
    inx = np.argmin(abs(a[ii] - agrid))
    opac.kabs.append(k_abs[inx,:])
    opac.ksca.append(k_sca[inx,:])
    opac.phase_g.append(gsca[inx,:])

# write out the file
for ii in range(ngsize):
    opac.writeOpac(ext=name[ii], idust=ii)
opac.writeMasterOpac(ext=name, scattering_mode_max=2)

#plot1,10,100microns
plt.loglog(wgrid, k_abs[28, :], label='1micronabs')
plt.loglog(wgrid, k_sca[28, :], '--', label='1micronsca')
plt.loglog(wgrid, k_abs[57, :], label='10micronabs')
plt.loglog(wgrid, k_sca[57, :], '--', label='10micronsca')
plt.loglog(wgrid, k_abs[85, :], label='100micronabs')
plt.loglog(wgrid, k_sca[85, :], '--', label='100micronsca')
plt.legend()
plt.show()

#plot1,10,100microns switching x and y
plt.loglog(agrid, k_abs[:, 28], label='1micronabs')
plt.loglog(agrid, k_sca[:, 28], '--', label='1micronsca')
plt.loglog(agrid, k_abs[:, 57], label='10micronabs')
plt.loglog(agrid, k_sca[:, 57], '--', label='10micronsca')
plt.loglog(agrid, k_abs[:, 85], label='100micronabs')
plt.loglog(agrid, k_sca[:, 85], '--', label='100micronsca')
plt.loglog(agrid, k_abs[:, 139], label='1millimeterabs')
plt.loglog(agrid, k_sca[:, 139], '--', label='1millimetersca')
plt.legend()
plt.show()

