# Computes temperature, DT/dz for US standard atmosphere conditions from Z = 0 to 50 km geopotential height.
import numpy as np
import matplotlib.pyplot as plt
from numpy import pi,sin,cos,exp

def lapse_rate(z):
    if z<=11:
       T=288.15-6.5*z
       dTdz=-6.5e-3
    elif (z>11) & (z<=20):
       T=216.65
       dTdz=0
    elif (z>20) & (z<=32):
       T=216.65+(z-20)
       dTdz=1.0e-3
    elif (z>32) & (z<=47):
       T=228.65+2.8*(z-32)
       dTdz=2.8e-3
    elif (z>47) & (z<=51):
       T=270.65
       dTdz=0
    return T,dTdz

def hydro_stat(z,i):
    H=(R/2*g)*(lapse_rate(z[i])[0]+lapse_rate(z[i+1])[0])
    p[i+1]=p[i]*exp(-(z[i+1]-z[i])*1.0e3/H)
    return p[i+1]

g = 9.81
R = 287
cp=1004
nl = 101         # number of levels above ground
ztop = 50        # upper boundary in km
nlm = nl-1
dz = ztop/nlm
T0,p0 = [288.15,1013.25]
z = np.linspace(0,ztop,nlm)
T,dTdz=np.array([]),np.array([])
p=np.zeros(len(z))
p[0]=p0
for i,h in enumerate(sorted(z)):
    temp=lapse_rate(h)
    T=np.append(T,temp[0])
    dTdz=np.append(dTdz,temp[1])
    if i==99:
       pass
    else:
       p[i+1]=hydro_stat(z,i)
#plotting
pot=T*(p0/p)**(R/cp)
print(len(z),len(T),len(dTdz),len(p),len(pot))
fig,axes=plt.subplots(2,2,figsize=(10,6))
plt.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.3, hspace=0.3)
axes = axes.flatten()
for ax,var,xleb in zip(axes,[T,dTdz*1.e3,p,pot],['Temperature  [K]','Lapse rate [K/km]','Pressure [hPa]','Potential Temperature [K]']):
    ax.plot(var,z)
    ax.set(xlabel=xleb,ylabel='Height [km]')
plt.show()
