# coriolis.py
import numpy as np
from numpy import pi,sin,cos,zeros
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def coriolis1(x,t,rad,omega):
    ind = 1.0
    u_part=(2.0*omega+ind*x[0]/(rad*cos(x[3])))*sin(x[3])
    xprime = [u_part*x[1],-1.0*u_part*x[0],x[0]/(rad*cos(x[3])),x[1]/rad]
    return xprime

def coriolis2(x,t,rad,omega):
    ind = 1.0
    u_part=(2.0*omega)*sin(x[3])
    xprime = [u_part*x[1],-1.0*u_part*x[0],x[0]/(rad*cos(x[3])),x[1]/rad]
    return xprime

def plot_trajectory(ax,model,x0,t,rad,omega):
    x = odeint(model,x0,t,args=(rad, omega))
    lon = x[:,2]*180.0/pi;      # converts longitude to degrees
    lat = x[:,3]*180.0/pi;      # converts latitude to degrees
    ax.plot(lon,lat)
    ax.plot(lon[0],lat[0],'d')
    ax.plot(lon[-1],lat[-1],'d')
    ax.set_xlim([-1+np.min(lon),1+np.max(lon)])
    ax.set_ylim([-1+np.min(lat),1+np.max(lat)])
    ax.set(xlabel='Longitude',ylabel='Latitude')
    return ax,x   

print('Initial longitude is zero. Specify latitude and speed when asked.')
init_lat = float(input('Specify an initial latitude in degrees  '))
u0 = float(input('Specify a zonal wind in m/s ' ))
v0 = float(input('Specify a meridional wind in m/s '))
rad= 6.37e6
omega=7.292e-5
lat0 = pi*init_lat/180.0
runtime = float(input('Specify integration time in days  '))
time = runtime*24.0*3600.0
x0=[u0,v0,0,lat0]
t=np.linspace(0,time)

#plotting
fig, axes = plt.subplots(1, 2)
ax1,x1=plot_trajectory(axes[0],coriolis1,x0,t,rad,omega)
ax1.set_title('Trajectory with curvature terms')
ax2,x2=plot_trajectory(axes[1],coriolis2,x0,t,rad,omega)
ax2.set_title('Trajectory without curvature terms')
plt.show(fig)


