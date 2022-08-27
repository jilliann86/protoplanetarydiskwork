import radmc3dPy
import os
import matplotlib.pyplot as plt
from radmc3dPy import natconst
import numpy as np

os.chdir('model1')
data1 = radmc3dPy.analyze.readData(dtemp=True, ddens=True, binary=False)
os.chdir('..')

os.chdir('model2')
data2 = radmc3dPy.analyze.readData(dtemp=True, ddens=True, binary=False)
os.chdir('..')

#Temperature Midplane Profile
#inx = np.argmin(abs(data.grid.y - np.pi/2))
#plt.plot(data1.grid.x/natconst.au, data1.dusttemp[:, inx, 0, 0], label='model1')
#plt.plot(data2.grid.x/natconst.au, data2.dusttemp[:, inx, 0, 0], label='model2')
#plt.xscale('log')
#plt.yscale('log')
#plt.legend()
#plt.show()

modelname = ['0.1micronmodel', '1micronmodel', '10micronmodel', '100micronmodel']

collect = []
opacs = []
for ii in range(len(modelname)):
	os.chdir(modelname[ii])
	data  = radmc3dPy.analyze.readData(dtemp=True, ddens=True, binary=False)
	collect.append(data)
	opac = radmc3dPy.dustopac.radmc3dDustOpac()
	mopac = opac.readMasterOpac()
	opac.readOpac(ext=mopac['ext'])
	opacs.append(opac)
	os.chdir('..')
 
#Temperature Midplane Profile
for ii in range(len(modelname)):
	inx = np.argmin(abs(collect[ii].grid.y - np.pi/2))
	plt.plot(collect[ii].grid.x/natconst.au, collect[ii].dusttemp[:, inx, 0, 0], label=modelname[ii])
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()


#Temperature along theta at 20
for ii in range(len(modelname)):
        inx = np.argmin(abs(collect[ii].grid.x - 20))
        plt.plot(collect[ii].grid.y, collect[ii].dusttemp[inx, :, 0, 0], label=modelname[ii])
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()

#opactiy Model
for ii in range(len(modelname)):
	inx = 0
	plt.plot(opacs[ii].wav[inx], opacs[ii].kabs[inx], label=modelname[ii])
	plt.plot(opacs[ii].wav[inx], opacs[ii].ksca[inx], label=modelname[ii], linestyle='--')
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()
