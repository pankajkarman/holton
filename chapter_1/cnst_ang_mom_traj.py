import numpy as np
from numpy import pi,sin,cos,zeros
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def coriolis(x,rad,omega):
    ind = 1.0
    u_part=(2.0*omega+ind*x[0]/(rad*cos(x[3])))*sin(x[3])
    xprime = [u_part*x[1],-1.0*u_part*x[0],x[0]/(rad*cos(x[3])),x[1]/rad]
    return xprime
    
def init():
    line.set_data([],[])
    return line,
    
def update(num,lon,lat,line):
    line.set_data(lon[:num],lat[:num])
    #line.axes.axis([-180, 180, -90, 90])
    return line,

rad= 6.37e6
omega=7.292e-5
print('Initial longitude is zero. Specify latitude and speed when asked. ')
init_lat = float(input('Specify an initial latitude in degrees  '))
u0 = float(input('Specify a zonal wind in m/s ' ))
v0 = float(input('Specify a meridional wind in m/s '))
runtime = float(input('Specify integration time in days  '))
time = runtime*24.0*3600.0
lat0 = pi*init_lat/180.0
x=[u0,v0,0,lat0]
xprimn = coriolis(x,rad,omega)
xprim1 = xprimn
xprim2 = xprim1
dt = 60
dt12 = dt/12
time=np.arange(0,time,dt)
lon,lat=[],[]
for t in time:
    for i in np.arange(len(x)):
        x[i]=x[i]+dt12*(23*xprimn[i] -16*xprim1[i] +5*xprim2[i])
    xprim2 = xprim1
    xprim1 = xprimn
    xprimn = coriolis(x,rad,omega)
    if x[2] > pi:
            x[2]= -2.0*pi+x[2]
    elif x[2] < -pi:
        x[2] = 2.0*pi+x[2]
    lon.append(float(x[2])*180.0/pi)
    lat.append(float(x[3])*180.0/pi)
#print('Lat ='+str(lat))
#print('Lon ='+str(lon))
fig,ax=plt.subplots()
ax.axis('equal')
line, =plt.plot(lon,lat,color='k')
anim=FuncAnimation(fig,update,len(lon), fargs=[lon, lat, line],interval=10, blit=True,repeat=False)
plt.show()    
anim.save('MovWave.mp4', codec='h264', fps=30)
#anim.save('test.gif',writer='imagemagick')
