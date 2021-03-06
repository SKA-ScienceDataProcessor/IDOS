import matplotlib.pylab as pl
import numpy as np
import scipy.interpolate as spi

d=[[50,48,1.386],
[50,96,0.315],
[50,144,0.448],
[50,192,0.584],
[50,240,0.721],
[50,288,0.847],
[50,336,0.977],
[50,384,1.107],
[50,432,1.245],
[80,48,1.433],
[80,96,0.494],
[80,144,0.703],
[80,192,0.911],
[80,240,1.116],
[80,288,1.327],
[80,336,1.531],
[80,384,1.743],
[80,432,1.952],
[110,48,1.538],
[110,96,0.675],
[110,144,0.961],
[110,192,1.253],
[110,240,1.533],
[110,288,1.823],
[110,336,2.105],
[110,384,2.395],
[110,432,2.685],
[140,48,1.645],
[140,96,0.862],
[140,144,1.224],
[140,192,1.591],
[140,240,1.951],
[140,288,2.326],
[140,336,2.683],
[140,384,3.052],
[140,432,3.410],
[170,48,1.744],
[170,96,1.059],
[170,144,1.495],
[170,192,1.937],
[170,240,2.379],
[170,288,2.823],
[170,336,3.263],
[170,384,3.720],
[170,432,4.166],
[200,48,1.868],
[200,96,1.252],
[200,144,1.771],
[200,192,2.302],
[200,240,2.836],
[200,288,3.365],
[200,336,3.887],
[200,384,4.418],
[200,432,4.941],
[230,48,1.973],
[230,96,1.436],
[230,144,2.038],
[230,192,2.651],
[230,240,3.246],
[230,288,3.855],
[230,336,4.480],
[230,384,5.075],
[230,432,5.673],
[260,48,2.092],
[260,96,1.630],
[260,144,2.314],
[260,192,3.002],
[260,240,3.684],
[260,288,4.382],
[260,336,5.069],
[260,384,5.749],
[260,432,6.444],
[290,48,2.190],
[290,96,1.828],
[290,144,2.594],
[290,192,3.360],
[290,240,4.127],
[290,288,4.908],
[290,336,5.680],
[290,384,6.450],
[290,432,7.221]]

d21=[
[ 50,  48 , 1.406 ],
[ 50,  96 , 0.326 ],
[ 50,  144 , 0.453 ],
[ 50,  192 , 0.586 ],
[ 50,  240 , 0.713 ],
[ 50,  288 , 0.846 ],
[ 50,  336 , 0.979 ],
[ 50,  384 , 1.110 ],
[ 50,  432 , 1.247 ],
[ 80,  48 , 1.438 ],
[ 80,  96 , 0.494 ],
[ 80,  144 , 0.704 ],
[ 80,  192 , 0.913 ],
[ 80,  240 , 1.119 ],
[ 80,  288 , 1.324 ],
[ 80,  336 , 1.532 ],
[ 80,  384 , 1.746 ],
[ 80,  432 , 1.959 ],
[ 110,  48 , 1.549 ],
[ 110,  96 , 0.678 ],
[ 110,  144 , 0.966 ],
[ 110,  192 , 1.253 ],
[ 110,  240 , 1.534 ],
[ 110,  288 , 1.825 ],
[ 110,  336 , 2.118 ],
[ 110,  384 , 2.395 ],
[ 110,  432 , 2.666 ],
[ 140,  48 , 1.662 ],
[ 140,  96 , 0.855 ],
[ 140,  144 , 1.222 ],
[ 140,  192 , 1.578 ],
[ 140,  240 , 1.938 ],
[ 140,  288 , 2.303 ],
[ 140,  336 , 2.666 ],
[ 140,  384 , 3.033 ],
[ 140,  432 , 3.377 ],
[ 170,  48 , 1.747 ],
[ 170,  96 , 1.036 ],
[ 170,  144 , 1.478 ],
[ 170,  192 , 1.918 ],
[ 170,  240 , 2.357 ],
[ 170,  288 , 2.792 ],
[ 170,  336 , 3.231 ],
[ 170,  384 , 3.681 ],
[ 170,  432 , 4.125 ],
[ 200,  48 , 1.858 ],
[ 200,  96 , 1.236 ],
[ 200,  144 , 1.748 ],
[ 200,  192 , 2.275 ],
[ 200,  240 , 2.794 ],
[ 200,  288 , 3.314 ],
[ 200,  336 , 3.844 ],
[ 200,  384 , 4.363 ],
[ 200,  432 , 4.895 ],
[ 230,  48 , 1.976 ],
[ 230,  96 , 1.422 ],
[ 230,  144 , 2.026 ],
[ 230,  192 , 2.630 ],
[ 230,  240 , 3.232 ],
[ 230,  288 , 3.839 ],
[ 230,  336 , 4.449 ],
[ 230,  384 , 5.038 ],
[ 230,  432 , 5.651 ],
[ 260,  48 , 2.090 ],
[ 260,  96 , 1.632 ],
[ 260,  144 , 2.313 ],
[ 260,  192 , 3.001 ],
[ 260,  240 , 3.687 ],
[ 260,  288 , 4.398 ],
[ 260,  336 , 5.098 ],
[ 260,  384 , 5.773 ],
[ 260,  432 , 6.454 ],
[ 290,  48 , 2.221 ],
[ 290,  96 , 1.834 ],
[ 290,  144 , 2.594 ],
[ 290,  192 , 3.367 ],
[ 290,  240 , 4.126 ],
[ 290,  288 , 4.916 ],
[ 290,  336 , 5.690 ],
[ 290,  384 , 6.453 ],
[ 290,  432 , 7.223 ],
]
    
d=np.array(d21)
d2=np.ones([len(np.unique(d.T[0])),len(np.unique(d.T[1])),3])*np.nan

for n in range(9):
  for m in range(9):
    d2[n][m][:]=[d[n*9+m][2],d[n*9+m][0],d[n*9+m][1]]

## For some reason 48 time steps is always very slow!!
## So skipped in following plots

pl.ion()
pl.clf()
#pl.contour(d2.T[1][0].T,d2.T[2].T[0][1:9]*0.9/60.,d2.T[0][1:9]*100./60.,40)
#pl.xlabel('No. Stations')
#pl.ylabel('Minutes (at 0.9s/integration)')
pl.contour(d2.T[2].T[0][1:9].T*0.9/60,d2.T[1][0],d2.T[0][1:9].T*100./60.,np.array(range(1,12)))
pl.ylabel('No. Stations')
pl.xlabel('Minutes (at 0.9s/integration)')
pl.title('Required time for OSKAR-2 completion, per 100 channels')
pl.colorbar()

pl.figure()
d3= d2.T[0][:][:]*100/60/(d2.T[2][:][:]*0.9/60)
#fint=scipy.interpolate.interp1d(d3[1:9][:].flatten(),d2.T[2][1:9][:].flatten(),fill_value='extrapolate')
fint=spi.interp1d(d2.T[1][1:9][:].flatten(),d3[1:9][:].flatten(),bounds_error=False)
nstat=np.array(range(1,13))*50
pl.plot(nstat,fint(nstat)*640,'o-')
pl.axis([45,260,200,1100])
pl.ylabel('Number of Nodes')
pl.xlabel('Number of Stations')
pl.title('Required number of machines')

